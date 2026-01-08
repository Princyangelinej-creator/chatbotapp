from django.urls import path
from .views import home, new_chat, delete_chat

urlpatterns = [
    path("", home, name="home"),
    path("new-chat/", new_chat, name="new_chat"),
    path("delete-chat/<uuid:conversation_id>/", delete_chat, name="delete_chat"),
]
