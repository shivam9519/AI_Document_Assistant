from fastapi import FastAPI
from backend.routes.upload import router as upload_router
from backend.routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from backend.services.store import load_all_documents   # 👈 add this

app = FastAPI(
    title="AI Document Assistant",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-document-assistant-edca.vercel.app",
        "https://shiku-ai-document-assistant.onrender.com"
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)

@app.on_event("startup")           # 👈 add this block
def startup_event():
    load_all_documents()
    print("✅ Loaded saved documents from disk into memory")

@app.get("/")
def home():
    return {"message": "Welcome to AI Document Assistant"}