from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

import os

# LOAD ENV
load_dotenv()

# INIT APP
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OPENAI CLIENT
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# REQUEST MODEL
class ChatRequest(BaseModel):
    message: str

# ROOT
@app.get("/")
async def root():

    return {
        "status": "JARVIS backend online"
    }

# CHAT ENDPOINT
@app.post("/chat")
async def chat(req: ChatRequest):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content":
                    """
                    You are JARVIS,
                    a futuristic AI assistant.

                    Speak intelligently,
                    concisely,
                    and naturally.
                    """
            },

            {
                "role": "user",
                "content": req.message
            }
        ]
    )

    return {
        "reply":
            response
            .choices[0]
            .message
            .content
    }