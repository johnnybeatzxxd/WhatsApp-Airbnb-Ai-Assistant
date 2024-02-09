from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
#from pymongo import MongoClient
import telebot
import openai
import datetime
import os
import time
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.environ.get("TelegramBotToken"))
openai.api_key = os.environ.get('OpenAiKey')

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
    def start(message):
        bot.reply_to(message,"👀 Sorry friend! Didn't understand that one.",reply_markup=markups())


    def post(self, request):        
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
        return HttpResponse("!", status=200)