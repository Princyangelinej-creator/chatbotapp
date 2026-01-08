"""Database models for the chatbot app."""

# pylint: disable=no-member,unsubscriptable-object

import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatMessage(models.Model):
    """Model to store chat messages and AI responses for each conversation."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation_id = models.UUIDField(default=uuid.uuid4, db_index=True)

    user_message = models.TextField()
    bot_reply = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable string representation of a chat message."""
        return f"{self.user.username} - {self.user_message[:30]}"


class UserMemory(models.Model):
    """Model to store long-term memory information for each user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    memory = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable string representation of user memory."""
        return f"Memory of {self.user.username}"
        