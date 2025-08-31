from flask import Blueprint, request, Response, jsonify, stream_with_context
from services.llm_services import (
    ask_gemini, stream_gemini,
    ask_deepseek, stream_deepseek
)

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    Unified /chat endpoint.

    Body JSON:
      {
        "question": "What is Orlando's strongest skill?",
        "model": "gemini" | "deepseek",   # default gemini
        "stream": true | false            # default false
      }

    Returns:
      - If stream==false -> JSON { "answer": "..." }
      - If stream==true  -> chunked plain text streaming (client reads chunks)
    """
    payload = request.get_json(silent=True) or {}
    question = payload.get("question") or payload.get("prompt") or ""
    model = payload.get("model", "gemini").lower()
    stream_flag = bool(payload.get("stream", False))

    if not question:
        return jsonify({"error": "question is required"}), 400

    # Non-streaming responses
    if not stream_flag:
        if model == "gemini":
            answer = ask_gemini(question)
        elif model == "deepseek":
            answer = ask_deepseek(question)
        else:
            return jsonify({"error": f"unknown model '{model}'"}), 400
        # For non-stream, always return JSON
        return jsonify({"answer": answer})

    # Streaming response generator
    def generator():
        if model == "gemini":
            yield from stream_gemini(question)
        elif model == "deepseek":
            yield from stream_deepseek(question)
        else:
            yield f"Unknown model: {model}"

    # stream_with_context ensures the request context lives during streaming
    return Response(stream_with_context(generator()), content_type="text/plain; charset=utf-8")
