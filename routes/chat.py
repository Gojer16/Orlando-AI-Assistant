from flask import Blueprint, request, Response, jsonify, stream_with_context
from services.llm_services import ask_gemini, stream_gemini

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """
    /chat endpoint for Gemini.

    Body JSON:
      {
        "question": "What is Orlando's strongest skill?",
        "stream": true | false    # default false
      }

    Returns:
      - If stream==false -> JSON { "answer": "..." }
      - If stream==true  -> plain text streaming (chunked)
    """
    payload = request.get_json(silent=True) or {}
    question = payload.get("question") or payload.get("prompt") or ""
    stream_flag = bool(payload.get("stream", False))

    if not question:
        return jsonify({"error": "question is required"}), 400

    if not stream_flag:
        # Non-streaming response
        answer = ask_gemini(question)
        return jsonify({"answer": answer})

    # Streaming response
    def generator():
        yield from stream_gemini(question)

    return Response(
        stream_with_context(generator()),
        content_type="text/plain; charset=utf-8"
    )
