from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("API KEY:", os.getenv("OPENAI_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        if "stress" in req.message.lower():
            return {"reply": "It sounds like you're stressed. Want to try a short breathing exercise?"}

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful mental wellness assistant. Keep responses short and supportive."
                },
                {
                    "role": "user",
                    "content": req.message
                }
            ]
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        print("AI ERROR:", e)

        # 👇 FALLBACK RESPONSE
        return {
            "reply": "I'm here for you 💚 Even if I can't fully respond right now, you're not alone."
        }