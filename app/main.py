import os
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="AI Interview Coach")
ROOT = Path(__file__).parent


class QuestionRequest(BaseModel):
    role: str = Field(min_length=2, max_length=80)
    topic: str = Field(min_length=2, max_length=80)
    level: str = Field(default="Intermediate", max_length=30)


class FeedbackRequest(QuestionRequest):
    question: str = Field(min_length=5, max_length=1000)
    answer: str = Field(min_length=10, max_length=4000)


def ask_model(instruction: str, user_text: str) -> str:
    model_id = os.getenv("BEDROCK_MODEL_ID")
    if not model_id:
        raise HTTPException(503, "BEDROCK_MODEL_ID is not configured")
    try:
        response = boto3.client("bedrock-runtime").converse(
            modelId=model_id,
            system=[{"text": instruction}],
            messages=[{"role": "user", "content": [{"text": user_text}]}],
            inferenceConfig={"maxTokens": 600, "temperature": 0.4},
        )
        return "\n".join(
            part["text"] for part in response["output"]["message"]["content"]
            if "text" in part
        )
    except (ClientError, BotoCoreError) as exc:
        # Avoid leaking provider or account details into the browser.
        raise HTTPException(502, "AI service unavailable. Check server logs and AWS permissions.") from exc


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/question")
def question(request: QuestionRequest):
    text = ask_model(
        "You are a practical technical interviewer. Return exactly one concise interview question. No answer.",
        f"Role: {request.role}\nTopic: {request.topic}\nLevel: {request.level}",
    )
    return {"question": text}


@app.post("/api/feedback")
def feedback(request: FeedbackRequest):
    text = ask_model(
        "You are a supportive technical interview coach. Give concise feedback with: strengths, missing points, and a stronger sample answer. Do not invent user experience.",
        f"Role: {request.role}\nTopic: {request.topic}\nLevel: {request.level}\nQuestion: {request.question}\nCandidate answer: {request.answer}",
    )
    return {"feedback": text}


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")
