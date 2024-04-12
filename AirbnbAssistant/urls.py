from django.contrib import admin
from django.urls import path
from Assistant import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('telegram/chat/', views.TelegramWebhookView.as_view()),
    
]
