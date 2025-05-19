from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

# Load your API key into OPENAI_API_KEY env var before running
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()


class IdeaIn(BaseModel):
    text: str


@app.post("/ideate/start")
async def start_ideation(payload: IdeaIn):
    prompt = (
        "You are an assistant that transforms raw project ideas into structured summaries.\n"
        f"Input: {payload.text}\n"
        "Task: Provide a 1–2 sentence summary of the idea for confirmation."
    )

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.2,
            max_tokens=150,
        )
        summary = resp.choices[0].message.content.strip()
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
