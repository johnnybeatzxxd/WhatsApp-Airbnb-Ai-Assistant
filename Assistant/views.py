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

    
    @bot.message_handler(func=lambda x:True)
    def chat(customer):
        prompt = customer.text
        first_name = customer.from_user.first_name
        username = customer.from_user.username
        id_ = customer.chat.id

        if prompt == '💁‍♂ Reset':
            database.reset_conversation(id_)

        else:
            print("message received!")
            database.register(id_,first_name,username)
            print("adding users message")
            database.add_message(id_,"user")
            print("done adding user messages")
            required_user_info = database.required_user_info()
            print("generating answer")
            response = ai.generate_response(prompt,required_user_info)
            
            images = []
            if ai.responseType == 'image':
                for i in ai.random_imgs:
                    images.append(ai.imgs[i])
                
                media_group = []
                for image in images:
                    media_group.append(telebot.types.InputMediaPhoto(image,response))

                #bot.send_media_group(id_, media_group)
                bot.send_photo(id_,images[0],caption=response)

            else:
                bot.send_message(id_,response,reply_markup=markups())


        

    def post(self, request):        
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
        return HttpResponse("!", status=200)