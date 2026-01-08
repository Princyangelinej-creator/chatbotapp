"""Admin configuration for the chatbot app."""

from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)

class ChatMessageAdmin(admin.ModelAdmin):
    """Admin class for chatmessages."""

    list_display = ("user", "user_message", "bot_reply", "created_at")
    