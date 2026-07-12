from fastapi import FastAPI
from backend.routes.upload import router as upload_router
from backend.routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(
    title="AI Document Assistant",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return{
        "message":"Welcome to AI Document Assistant"
    }