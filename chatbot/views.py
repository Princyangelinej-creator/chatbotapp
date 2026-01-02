"""Views for chatbot app."""

# pylint: disable=no-member

import uuid

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.db.models import Min

from .models import ChatMessage
from .openai_client import get_ai_reply
from .rag.loader import extract_text
from .rag.rag_pipeline import process_document, get_relevant_context
from .rag.vectorstore import has_documents


# ----------------------------------------
# Detect personal / memory questions
# ----------------------------------------
def is_personal_question(message: str) -> bool:
    """Check whether the user message asks about personal or remembered data."""
    keywords = [
        "my name",
        "my friend",
        "friend name",
        "who is my",
        "what is my",
        "do you remember",
    ]
    return any(k in message.lower() for k in keywords)


@login_required
def chatbot_view(request):
    """Render chatbot page and handle chat messages and document uploads."""
    conversation_id = request.GET.get("conversation") or request.session.get("conversation_id")
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
    request.session["conversation_id"] = conversation_id

    messages = ChatMessage.objects.filter(
        user=request.user,
        conversation_id=conversation_id
    ).order_by("created_at")

    chat_list = (
        ChatMessage.objects
        .filter(user=request.user)
        .values("conversation_id")
        .annotate(first_time=Min("created_at"))
        .order_by("-first_time")
    )

    for chat in chat_list:
        first_msg = ChatMessage.objects.filter(
            user=request.user,
            conversation_id=chat["conversation_id"]
        ).order_by("created_at").first()
        chat["title"] = first_msg.user_message if first_msg else "New Chat"

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        uploaded_file = request.FILES.get("document")

        if uploaded_file:
            text = extract_text(uploaded_file)
            process_document(conversation_id, text)

            ChatMessage.objects.create(
                user=request.user,
                conversation_id=conversation_id,
                user_message=f"📎 Uploaded file: {uploaded_file.name}",
                bot_reply="Document received. You can now ask questions from it."
            )

        recent_messages = messages.order_by("-created_at")[:10][::-1]
        conversation_context = ""

        for msg in recent_messages:
            conversation_context += f"User: {msg.user_message}\n"
            conversation_context += f"AI: {msg.bot_reply}\n"

        if user_message:
            if is_personal_question(user_message):
                prompt = conversation_context + f"\nUser: {user_message}"

            elif has_documents(conversation_id):
                context_from_docs = get_relevant_context(conversation_id, user_message)
                prompt = f"""
Answer ONLY using the document below.
If the answer is not present, say exactly:
"I couldn't find this information in the uploaded document."

Context:
{context_from_docs or "NO RELEVANT CONTENT FOUND"}

Question:
{user_message}
"""

            else:
                prompt = conversation_context + f"\nUser: {user_message}"

            ai_reply = get_ai_reply(prompt)

            ChatMessage.objects.create(
                user=request.user,
                conversation_id=conversation_id,
                user_message=user_message,
                bot_reply=ai_reply
            )

        return redirect(f"/?conversation={conversation_id}")

    return render(request, "chatbot/index.html", {
        "messages": messages,
        "chat_list": chat_list,
        "active_conversation": conversation_id
    })


@login_required
def new_chat(request):
    """Start a new chat by creating a new conversation ID."""
    request.session["conversation_id"] = str(uuid.uuid4())
    return redirect("home")


def signup_view(request):
    """Register a new user account."""
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
    """Authenticate and log in an existing user."""
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
