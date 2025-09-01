📄 Resume Q&A Chatbot (Flask + Gemini API)

This project is a resume-based AI chatbot powered by Google Gemini API.

The app is designed to be lightweight, structured, and production-ready, with features such as rate limiting, streaming responses, and multiple system roles.

🚀 Features

Flask API with a single /chat endpoint.

Google Gemini API for natural language understanding.

System roles for different interaction modes:

recruiter: concise, resume-only answers.

career_coach: supportive but realistic career guidance.

detailed: thorough explanations with examples.

Multiple prompts for flexible use cases.

Streaming & non-streaming responses:

stream=false → returns a JSON object.

stream=true → streams plain text chunks.

CORS enabled for cross-origin requests.

Rate limiting to prevent abuse.

Deployable on Render with minimal setup.

📡 API Usage
Endpoint
POST /chat

Request Body (JSON)
{
  "question": "What is Orlando's strongest skill?",
  "role": "recruiter",    // recruiter | career_coach | detailed
  "stream": false         // optional, default = false
}

Response (non-streaming)
{
  "answer": "Orlando's strongest skill is building clean, scalable applications..."
}

Response (streaming)

Plain text chunks are streamed progressively.

🛠️ Tech Stack

Backend: Flask (Python)

LLM API: Google Gemini

Infra: Render (deployment)

Other:

CORS

Rate limiting


⚙️ Setup

Clone repo

git clone https://github.com/your-username/resume-chatbot.git
cd resume-chatbot


Install dependencies

pip install -r requirements.txt


Set environment variables

export GEMINI_API_KEY=your_api_key


Run locally

flask run --host=0.0.0.0 --port=5000


Deploy to Render

Add GEMINI_API_KEY in Render’s environment settings.

Use gunicorn "app:create_app()" as the start command.

🧭 Next Steps

Add RAG (Retrieval-Augmented Generation) for grounding on longer documents.

Integrate LangChain for structured pipelines and memory.

Expand roles with more advanced prompts.

