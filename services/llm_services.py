import os
import json
from typing import Generator
import google.generativeai as genai
from utils.loader import load_resume
from typing import Any

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_ROLES = {
    "recruiter": (
        "You are a professional assistant representing Orlando. "
        "Use ONLY the resume data provided to answer recruiter questions. "
        "If the answer is not in the resume, say you don't have that info "
        "and suggest next steps. Answer concisely in 2–4 sentences."
    ),
    "career_coach": (
        "You are an experienced career coach advising Orlando. "
        "You can interpret the resume data and suggest ways to present "
        "strengths, weaknesses, and growth opportunities. Be supportive but realistic."
    ),
    "detailed": (
        "You are a detailed career assistant. "
        "Answer questions thoroughly, expand with context, and give examples when possible."
    )
}

def _build_full_prompt(user_question: str, role: str) -> list[dict[str, str]]:
    """
    Build structured prompt for resume-based Q&A.
    Returns messages in OpenAI chat format.
    """
    if not user_question or not user_question.strip():
        raise ValueError("Question cannot be empty.")
    
    resume: dict[str, Any] = load_resume()
    if not resume:
        raise RuntimeError("Resume data missing or invalid.")
    
    # Stable, compact JSON representation
    resume_text = json.dumps(resume, separators=(",", ":"), sort_keys=True)
    
    system_message = SYSTEM_ROLES.get(role, SYSTEM_ROLES["recruiter"])

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"RESUME:\n{resume_text}\n\nQUESTION: {user_question}"}
    ]


def ask_gemini(user_question: str, model_name: str = "gemini-2.5-flash-lite", role: str = "recruiter") -> str:
    """One-shot Gemini response (non-stream)."""

    full_prompt = _build_full_prompt(user_question, role)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(full_prompt)

    if response and response.candidates:
        try:
            return response.candidates[0].content.parts[0].text.strip()
        except Exception:
            return "⚠️ Gemini returned an unexpected shape."
    return "⚠️ Gemini couldn't generate a response."


def stream_gemini(user_question: str, model_name: str = "gemini-2.5-flash-lite") -> Generator[str, None, None]:
    """
    Stream Gemini responses. 
    The SDK emits chunks; we iterate and yield text pieces.
    """
    full_prompt = _build_full_prompt(user_question)
    model = genai.GenerativeModel(model_name)

    stream_iter = model.generate_content(full_prompt, stream=True)

    for chunk in stream_iter:
        if not getattr(chunk, "candidates", None):
            continue
        try:
            text = chunk.candidates[0].content.parts[0].text
            if text:
                yield text
        except Exception:
            continue
