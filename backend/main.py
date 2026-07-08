from fastapi import FastAPI
from backend.routes.upload import router as upload_router
from backend.routes.chat import router as chat_router

app=FastAPI(
    title="AI Document Assistant",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return{
        "message":"Welcome to AI Document Assistant"
    }