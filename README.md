🤖 chatbotapp – Django AI Chatbot with RAG

chatbotapp is a Django-based AI chatbot application designed to provide intelligent conversational responses through both text-based interaction and document-based question answering using a Retrieval-Augmented Generation (RAG) approach.

The application allows users to upload documents (PDF/TXT), ask questions related to the uploaded content, and receive accurate, context-aware responses. Each chat maintains its own document memory, ensuring reliable answers across multiple conversations.

🚀 Features :

💬 Text-based AI chatbot

📄 Document-based Question Answering (RAG)

🧠 Per-chat document memory

🔄 Multi-chat conversation support

🔐 User authentication (Login / Signup)

🗂 Upload and query PDF or text documents

🧹 Clean, modular Django architecture

📊 High code quality validated using Pylint

🛠 Tech Stack :

Framework: Django 5.x

Language: Python 3.11

AI Integration: LLM API (Gemini / OpenAI compatible)

Vector Store: FAISS

Embeddings: HuggingFace (all-MiniLM-L6-v2)

Database: SQLite

Model : openai/gpt-oss-120b

Frontend: HTML, CSS, JavaScript

📁 Project Structure :
chatbotapp/
│
├── chatbot/
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── loader.py
│   │   ├── rag_pipeline.py
│   │   └── vectorstore.py
│   ├── templates/
│   ├── views.py
│   ├── models.py
│   └── urls.py
│
├── chatbotapp/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── .gitignore
├── .pylintrc
└── README.md

⚙️ Installation & Setup :
1️⃣ Clone the repository
git clone https://github.com/Princyangelinej-creator/chatbotapp.git
cd chatbotapp

2️⃣ Create and activate virtual environment
python -m venv myvenv
myvenv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start the server
python manage.py runserver


Access the app at:
👉 http://127.0.0.1:8000

🧪 Code Quality (Pylint) :

Tool: pylint + pylint-django

Score: ⭐ 9.95 / 10

Max line length: 120 characters

Virtual environments & cache ignored

This score reflects strong adherence to Python and Django best practices.

📄 Use Cases :

Academic project submission

Internship evaluation

Portfolio demonstration

AI + Django learning reference

👩‍💻 Developer

Princy Angeline J
Django | Python | AI Chatbot Development

📜 License :

This project is for educational and demonstration purposes.
