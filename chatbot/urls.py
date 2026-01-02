"""URL configuration for the chatbot app."""

from django.urls import path

from .views import chatbot_view, new_chat

urlpatterns = [
    path("", chatbot_view, name="home"),  # index.html
    path("new-chat/", new_chat, name="new_chat"),
]
