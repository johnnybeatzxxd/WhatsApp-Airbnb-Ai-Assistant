from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from . import database
from . import ai
import telebot
import openai
import datetime
import os
import time
import base64
import io  # Import the io module
from . import md2tgmd
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.environ.get("TelegramBotToken"))


# Create your views here.
def markups():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)   
    reset = telebot.types.KeyboardButton('💁‍♂ Reset')   
    markup.add(reset)
    return markup
class TelegramWebhookView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    
    @bot.message_handler(content_types=['text', 'photo'])
    def chat(customer):
        if customer.content_type == "photo":
            caption = customer.caption
            bot.send_chat_action(customer.chat.id, 'typing')
            prompt = []
            photo = customer.photo[-1]
            raw = photo.file_id  # Get the file_id of the photo
            print("id",raw)
            file_info = bot.get_file(raw)
            print(file_info)  # Get the File object
            downloaded_file = bot.download_file(file_info.file_path)
            print("passed")
            # Use BytesIO to handle the image data in memory
            image_stream = io.BytesIO(downloaded_file)
            image_data = base64.b64encode(image_stream.getvalue()).decode('utf-8')
            print(image_data)
            if caption != None:
                prompt.append({"text": caption},)
            prompt.append({
                "inlineData": {
                    "mimeType": "image/png",
                    "data": image_data
                }
            })
        if customer.content_type == "text":
            prompt = [
                {"text": customer.text},  
            ]

        first_name = customer.from_user.first_name
        username = customer.from_user.username
        id_ = customer.chat.id
        
        if prompt[0]["text"] == '💁‍♂ Reset':
            database.reset_conversation(id_)

        else:
            database.register(id_,first_name,username)
            conversation = database.add_message(id_,prompt,"user")
            required_user_info = database.required_user_info(id_)
            llm = ai.llm()
            response = llm.generate_response(id_,conversation,required_user_info)
            escaped_response = md2tgmd.escape(response) 
            response = [
                {"text": escaped_response},  
            ] 
            database.add_message(id_,response,"model")
            images = []
            if llm.responseType == 'image':
                for i in llm.random_imgs:
                    images.append(llm.imgs[i])            
                media_group = []
                for image in images:
                    media_group.append(telebot.types.InputMediaPhoto(image,escaped_response))

                #bot.send_media_group(id_, media_group)
                print(escaped_response)
                bot.send_photo(id_, images[0], caption=escaped_response, parse_mode='MarkdownV2')

            else:
                print(escaped_response)
                bot.send_message(id_, escaped_response, reply_markup=markups(), parse_mode='MarkdownV2')


        

    def post(self, request):        
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
        return HttpResponse("!", status=200)