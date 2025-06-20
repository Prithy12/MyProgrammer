from dotenv import load_dotenv
import os
import json

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
import openai

from db import engine, init_db, get_session
from models import Conversation

# ─── Load environment variables ─────────────────────────
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ─── Initialize database ────────────────────────────────
init_db()

app = FastAPI()

# ─── CORS Configuration ────────────────────────────────
origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Request Schemas ───────────────────────────────────
class IdeaIn(BaseModel):
    text: str

class SummaryIn(BaseModel):
    summary: str

class DraftIn(BaseModel):
    summary: str
    context: str
    draft: dict  # full draft JSON for saving

class RefineIn(BaseModel):
    id: str
    subdomain: str
    text: str

class SaveIn(BaseModel):
    name: str
    summary: str
    context: str
    draft: dict

# ─── Endpoint #1: Summarize Raw Idea ───────────────────
@app.post("/ideate/start")
async def start_ideation(payload: IdeaIn):
    prompt = (
        "You are an assistant that transforms raw project ideas into structured summaries.\n"
        f"Input: {payload.text}\n"
        "Task: Provide a 1–2 sentence summary of the idea for confirmation."
    )
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.2,
            max_tokens=150,
        )
        return {"summary": resp.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Endpoint #2: Enrich Context ───────────────────────
@app.post("/ideate/enrich")
async def enrich_context(payload: SummaryIn):
    prompt = (
        "Given this project summary:\n"
        f"{payload.summary}\n"
        "List three missing pieces of context (target user, pain-point, value proposition)."
    )
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.2,
            max_tokens=200,
        )
        return {"context": resp.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Endpoint #3: Draft Requirements ───────────────────
@app.post("/ideate/draft")
async def draft_requirements(payload: DraftIn):
    prompt = (
        "Using the following summary and context, generate 5–10 high-level requirements grouped into subdomains.\n\n"
        f"Summary:\n{payload.summary}\n\n"
        f"Context:\n{payload.context}\n\n"
        "Return strictly JSON in this format:\n"
        "{\n"
        "  \"subdomains\": [\"SubdomainA\",\"SubdomainB\"],\n"
        "  \"requirements\": [\n"
        "    {\"id\":\"R1\",\"subdomain\":\"SubdomainA\",\"text\":\"First requirement\"},\n"
        "    ...\n"
        "  ]\n"
        "}\n"
    )
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.2,
            max_tokens=500,
        )
        body = resp.choices[0].message.content.strip()
        data = json.loads(body)
        return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON returned:\n" + body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Endpoint #4: Refine Requirement ───────────────────
@app.post("/ideate/refine")
async def refine_requirement(payload: RefineIn):
    prompt = (
        "You are refining one requirement. Original requirement text:\n"
        f"{payload.text}\n\n"
        "Return **only** the improved requirement text. Do not include any metadata (ID or subdomain labels)."
    )
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.2,
            max_tokens=200,
        )
        refined_text = resp.choices[0].message.content.strip()
        return {"id": payload.id, "subdomain": payload.subdomain, "text": refined_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Endpoint #5: Save Conversation ───────────────────
@app.post("/ideate/save")
async def save_conversation(payload: SaveIn, session: Session = Depends(get_session)):
    convo = Conversation(
        name=payload.name,
        summary=payload.summary,
        context=payload.context,
        draft=payload.draft
    )
    session.add(convo)
    session.commit()
    session.refresh(convo)
    return {"id": convo.id}

# ─── Endpoint #6: List Conversations ──────────────────
@app.get("/ideate/list")
async def list_conversations(session: Session = Depends(get_session)):
    results = session.exec(select(Conversation.id, Conversation.name, Conversation.created_at)).all()
    return [{"id": id_, "name": name, "created_at": created_at.isoformat()} for id_, name, created_at in results]

# ─── Endpoint #7: Load Conversation ──────────────────
@app.get("/ideate/load/{convo_id}")
async def load_conversation(convo_id: int, session: Session = Depends(get_session)):
    convo = session.get(Conversation, convo_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {
        "summary": convo.summary,
        "context": convo.context,
        "draft": convo.draft
    }