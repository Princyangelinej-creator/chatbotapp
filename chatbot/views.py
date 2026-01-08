"""Views for chatbot app"""

import uuid
import re
from typing import Optional   

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.db.models import Min
from django.views.decorators.http import require_POST

from .models import ChatMessage, UserMemory
from .openai_client import get_ai_reply
from .rag.loader import extract_text
from .rag.rag_pipeline import process_document, get_relevant_context
from .rag.vectorstore import list_documents



def extract_word_limit(message):
    match = re.search(r"\b(\d+)\s*words\b", message.lower())
    return int(match.group(1)) if match else None



def save_user_name(user, message):
    match = re.search(r"my name is ([a-zA-Z ]+)", message.lower())
    if match:
        name = match.group(1).strip().title()
        memory, _ = UserMemory.objects.get_or_create(user=user)
        memory.memory = f"User name is {name}"
        memory.save()


def get_user_name(user):
    try:
        memory = UserMemory.objects.get(user=user)
        if memory.memory.lower().startswith("user name is"):
            return memory.memory.replace("User name is", "").strip()
    except UserMemory.DoesNotExist:
        pass
    return None





def extract_doc_index(message: str) -> Optional[int]:
    msg = message.lower()

    if "first document" in msg:
        return 0
    if "second document" in msg:
        return 1
    if "third document" in msg:
        return 2

    if "document" in msg or "file" in msg or "pdf" in msg:
        return -1  

    return None



@login_required
def home(request):
    user = request.user

    conversation_id = (
        request.GET.get("conversation")
        or request.session.get("conversation_id")
        or str(uuid.uuid4())
    )
    request.session["conversation_id"] = conversation_id

    messages = ChatMessage.objects.filter(
        user=user,
        conversation_id=conversation_id
    ).order_by("created_at")

    chat_list = (
        ChatMessage.objects
        .filter(user=user)
        .values("conversation_id")
        .annotate(first_time=Min("created_at"))
        .order_by("-first_time")
    )

    for chat in chat_list:
        first_msg = ChatMessage.objects.filter(
            user=user,
            conversation_id=chat["conversation_id"]
        ).order_by("created_at").first()

        chat["title"] = (
            first_msg.user_message[:40]
            if first_msg and first_msg.user_message
            else "New chat"
        )

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        uploaded_files = request.FILES.getlist("document")

        
        for uploaded_file in uploaded_files:
            existing_docs = list_documents(conversation_id)
            doc_id = f"doc{len(existing_docs) + 1}"  

            text = extract_text(uploaded_file)
            process_document(conversation_id, doc_id, text)

            ChatMessage.objects.create(
                user=user,
                conversation_id=conversation_id,
                user_message=f"📎 Uploaded ({doc_id}): {uploaded_file.name}",
                bot_reply="Document uploaded successfully."
            )

        
        if user_message:
            save_user_name(user, user_message)

            if "what is my name" in user_message.lower():
                name = get_user_name(user)
                ai_reply = f"Your name is {name}." if name else "I don't know your name yet."

            else:
                recent = messages.order_by("-created_at")[:8][::-1]
                history = ""

                for m in recent:
                    history += f"User: {m.user_message}\nAI: {m.bot_reply}\n"

                word_limit = extract_word_limit(user_message)
                instruction = (
                    f"\n\nAnswer in EXACTLY {word_limit} words."
                    if word_limit else ""
                )

               
                doc_keys = list_documents(conversation_id)
                doc_index = extract_doc_index(user_message)
                selected_doc = None

                if doc_index is not None and doc_keys:
                    if doc_index == -1:
                        selected_doc = doc_keys[-1]
                    elif 0 <= doc_index < len(doc_keys):
                        selected_doc = doc_keys[doc_index]

                if selected_doc:
                    context = get_relevant_context(
                        conversation_id,
                        selected_doc,
                        user_message
                    )

                    prompt = f"""
Answer ONLY using the selected document ({selected_doc}).
If not found, say:
"I couldn't find this information in the selected document."

DOCUMENT:
{context or "NO MATCH"}

QUESTION:
{user_message}
{instruction}
"""
                else:
                    prompt = history + f"\nUser: {user_message}{instruction}"

                ai_reply = get_ai_reply(prompt)

            ChatMessage.objects.create(
                user=user,
                conversation_id=conversation_id,
                user_message=user_message,
                bot_reply=ai_reply
            )

        return redirect(f"/?conversation={conversation_id}")

    return render(
        request,
        "chatbot/index.html",
        {
            "messages": messages,
            "chat_list": chat_list,
            "active_conversation": conversation_id,
        }
    )



@login_required
def new_chat(request):
    request.session["conversation_id"] = str(uuid.uuid4())
    return redirect("home")



@login_required
@require_POST
def delete_chat(request, conversation_id):
    ChatMessage.objects.filter(
        user=request.user,
        conversation_id=conversation_id
    ).delete()
    return redirect("home")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})
