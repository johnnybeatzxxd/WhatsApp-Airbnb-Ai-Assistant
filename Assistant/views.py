from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
#from pymongo import MongoClient
import telebot
import datetime
import os
import time
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.environ.get("TelegramBotToken"))


# Create your views here.

class TelegramWebhookView(View):
    print(os.environ.get("TelegramBotToken"))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    
    @bot.add_message_handler(func=lambda x:True)
    def start(message):
        bot.reply_to(message,"👀 Sorry friend! Didn't understand that one.")


    def post(self, request):        
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
        return HttpResponse("!", status=200)