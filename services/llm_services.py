import os
import json
import requests
from typing import Generator, Optional
import google.generativeai as genai
from utils.loader import load_resume

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def _build_full_prompt(user_question: str) -> str:
    """
    Combine resume JSON and user question into a single prompt.
    Keep prompt compact but explicit: system role + resume + question.
    """
    resume = load_resume()
    resume_text = json.dumps(resume, indent=2)
    return (
        "You are a professional assistant representing Orlando. "
        "Use ONLY the resume data provided to answer recruiter questions. "
        "If the answer is not in the resume, say you don't have that info and offer next steps.\n\n"
        f"RESUME_JSON:\n{resume_text}\n\n"
        f"QUESTION: {user_question}\n\n"
        "Answer concisely in 2-4 sentences."
    )

def ask_gemini(user_question: str, model_name: str = "gemini-2.5-flash-lite") -> str:
    """One-shot Gemini response (non-stream)."""
    full_prompt = _build_full_prompt(user_question)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(full_prompt)
    if response and response.candidates:
        try:
            return response.candidates[0].content.parts[0].text.strip()
        except Exception:
            return "Gemini returned an unexpected shape."
    return "Gemini couldn't generate a response."

def stream_gemini(user_question: str, model_name: str = "gemini-2.5-flash-lite") -> Generator[str, None, None]:
    """
    Stream Gemini responses. The SDK emits chunks; we iterate and yield text pieces.
    The Flask Response will stream these directly to the client.
    """
    full_prompt = _build_full_prompt(user_question)
    model = genai.GenerativeModel(model_name)

    stream_iter = model.generate_content(full_prompt, stream=True)

    for chunk in stream_iter:
        # each chunk can contain .candidates -> .content.parts -> .text
        if not getattr(chunk, "candidates", None):
            continue
        try:
            text = chunk.candidates[0].content.parts[0].text
            if text:
                yield text
        except Exception:
            # skip silently but log in real use
            continue


DEEPSEEK_URL = os.getenv("https://api.deepseek.com/v1/chat/completions")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

def ask_deepseek(user_question: str, model_name: str = "deepseek-chat") -> str:
    """One-shot DeepSeek call (non-stream)."""
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {DEEPSEEK_KEY}"}
    prompt = _build_full_prompt(user_question)
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are Orlando's resume assistant. Answer based on the resume JSON."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    resp = requests.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Try multiple possible shapes to be robust
    try:
        # Common format
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        try:
            # Some providers wrap in choices->text
            return data["choices"][0]["text"].strip()
        except Exception:
            return "DeepSeek returned an unexpected shape."

def stream_deepseek(user_question: str, model_name: str = "deepseek-chat") -> Generator[str, None, None]:
    """
    Stream DeepSeek using requests streaming.
    """
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {DEEPSEEK_KEY}"}
    prompt = _build_full_prompt(user_question)
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are Orlando's resume assistant. Answer based on the resume JSON."},
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }

    with requests.post(DEEPSEEK_URL, json=payload, headers=headers, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        # iterate over lines; many servers emit SSE: "data: {...}\n\n"
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            # SSE style "data: ..."; some servers might not include prefix
            if line.startswith("data:"):
                line = line[len("data:"):].strip()

            # finished signal
            if line == "[DONE]":
                break

            # try parse JSON payload
            try:
                obj = json.loads(line)
            except Exception:
                # not JSON; yield raw line as fallback
                yield line
                continue

            # robustly extract content from possible shapes
            # try delta.content -> message.content -> choices[*].text
            text_piece = None
            try:
                text_piece = obj.get("choices", [])[0].get("delta", {}).get("content")
            except Exception:
                text_piece = None
            if not text_piece:
                try:
                    text_piece = obj.get("choices", [])[0].get("message", {}).get("content")
                except Exception:
                    text_piece = None
            if not text_piece:
                try:
                    text_piece = obj.get("choices", [])[0].get("text")
                except Exception:
                    text_piece = None

            if text_piece:
                yield text_piece
