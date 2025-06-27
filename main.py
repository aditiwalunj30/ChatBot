from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.lang_agent import respond

app = FastAPI()

# Optional: Allow frontend (like Streamlit or browser) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class MessageRequest(BaseModel):
    message: str

# Root route
@app.get("/")
def root():
    return {"message": "TailorTalk API is running."}

# Chat endpoint
@app.post("/chat")
def chat(request: MessageRequest):
    reply = respond(request.message)
    return {"reply": reply}
