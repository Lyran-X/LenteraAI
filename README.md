# LenteraAI — AI-Powered Smart Learning Companion

LenteraAI is an AI-powered smart learning companion designed to help students learn more personally through AI Tutor, document-based question answering with RAG, personalized study planning, quiz generation, learning analytics, saved notes, and profile settings.

This project is developed as a functional local prototype for a 2026 capstone project.

---

## Key Features

### AI Tutor
Interactive learning assistant with multiple tutor modes, such as simple explanation, step-by-step guidance, Socratic learning, examples, and practice questions.

### Document Lab with RAG and ChromaDB
Users can upload learning documents, ask questions based on the document content, and receive grounded answers with citations. The system parses the document, splits it into chunks, generates embeddings, stores vectors in ChromaDB, retrieves relevant chunks, and sends the context to the LLM.

### Personalized Study Plan
Generate personalized study plans based on learning goals, topic, level, deadline, study duration, and weak topics.

### Quiz Arena
Generate quizzes from a topic or uploaded document, submit answers, view scores, review explanations, and identify weak topics.

### Learning Analytics
Track score trends, topic mastery, weak topics, recent quiz performance, completed study plans, and retention insights.

### Saved Notes
Save AI Tutor answers or create manual notes with search, filters, pin/unpin, edit, and delete support.

### Profile Settings
Manage profile information, avatar, learning preferences, AI tutor settings, password, and learning data export.

### JWT Authentication
Secure user registration, login, protected routes, and authenticated API access.

---

## Tech Stack

### Frontend
- Vue.js 3
- Vue Router
- Pinia
- Axios
- Tailwind CSS
- Vite
- SweetAlert2
- Lottie-web
- Markdown-it

### Backend
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL / Neon
- JWT Authentication
- Passlib / bcrypt
- Pydantic
- Uvicorn
- Gemini API
- ChromaDB local persistent vector database

---

## System Architecture

```mermaid
flowchart LR
    U[User] --> FE[Vue.js Frontend]
    FE --> API[FastAPI Backend]
    API --> AUTH[JWT Auth]
    API --> DB[(PostgreSQL / Neon)]
    API --> LLM[Gemini API]
    API --> RAG[RAG Pipeline]
    RAG --> PARSER[Document Parser]
    RAG --> CHUNKER[Text Chunker]
    RAG --> EMB[Embedding Service]
    RAG --> VDB[(ChromaDB Local Vector DB)]
    RAG --> LLM
    API --> FE
```
## Folder Structure
project-root/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── router.py
│   ├── auth/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── rag/
│   ├── schemas/
│   └── services/
├── frontend/
│   └── src/
│       ├── assets/
│       ├── components/
│       ├── landing_project/
│       ├── layouts/
│       ├── router/
│       ├── services/
│       ├── stores/
│       └── views/
├── alembic/
├── storage/
│   └── chroma/
├── uploads/
├── requirements.txt
├── .env.example
├── main.py
└── README.md

## Important Directories
frontend/src/views — main dashboard pages.
frontend/src/services — frontend API client modules.
frontend/src/components — reusable UI components.
app/api — FastAPI router and API route modules.
app/services — backend business logic.
app/rag — document parsing, chunking, embedding, vector search, and RAG answer generation.
app/models — SQLAlchemy database models.
app/schemas — Pydantic request and response schemas.
app/core — backend configuration.
app/auth — authentication dependencies and JWT utilities.
storage/chroma — local ChromaDB vector database storage.

## Alembic uses alembic.ini for migration configuration. The dummy sqlalchemy.url in alembic.ini is overridden by alembic/env.py using DATABASE_URL from the environment configuration.

## Environment Variables

Create a .env file based on .env.example.
APP_NAME="LenteraAI API"
APP_VERSION="0.1.0"
APP_ENV="development"
API_V1_PREFIX="/api"

DATABASE_URL="postgresql://USER:PASSWORD@HOST.neon.tech/DBNAME?sslmode=require"

JWT_SECRET_KEY="replace-with-a-long-random-secret"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]

UPLOAD_DIR="uploads/documents"

VECTOR_STORE="chroma"
CHROMA_PERSIST_DIR="./storage/chroma"
VECTOR_COLLECTION="edupath_documents"
EMBEDDING_MODEL="local-hash-embedding-v1"

LLM_PROVIDER="gemini"
LLM_MODEL="models/gemini-2.5-flash"
LLM_API_KEY=""

GEMINI_API_KEY=""
GEMINI_MODEL="models/gemini-2.5-flash"

## Backend Installation
Recommended Python version: Python 3.11
cd D:\Git\dashboard

py -3.11 -m venv .venv
.\.venv\Scripts\activate

python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

alembic upgrade head
uvicorn main:app --reload

Backend API:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

## Frontend Installation
cd D:\Git\dashboard\frontend

npm install
npm run dev

http://localhost:5173

## API Documentation

Swagger is available at:

http://127.0.0.1:8000/docs

Main API modules:

/api/auth
/api/users
/api/ai-tutor
/api/documents
/api/study-plans
/api/quizzes
/api/analytics
/api/notes

## Demo Flow
Register or login.
Open the dashboard overview.
Ask a learning question using AI Tutor.
Upload a learning document in Document Lab.
Ask a document-based question and view citations.
Generate a personalized study plan.
Generate and submit a quiz.
View learning analytics.
Save important notes.
Update profile settings.

## Project Status

Prototype / Capstone Project 2026.

The project is implemented as a functional local prototype. Production deployment, large-scale load testing, and cloud vector database deployment are outside the current scope.

## Author

Radinal Aly
S1 Informatika
Universitas Amikom Yogyakarta

Radinal Aly is a 3rd year undergraduate student in Informatics at Universitas Amikom Yogyakarta. He is currently participating in the Last Mile program, with interests in web development, artificial intelligence, and educational technology.

License

Educational use / capstone project.
