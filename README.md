# 📄 Resume Q&A Chatbot (Flask + Gemini API)

This project is a lightweight and production-ready AI chatbot that answers questions based on my resume. It is built with **Flask** and powered by the **Google Gemini API**. The app is designed with key features like rate limiting, streaming responses, and multiple system roles to provide a versatile and scalable solution.

---
## ✨ Key Features

* **RESTful API:** A single `/chat` endpoint for all interactions.
* **Flexible Roles:** Switch between different system roles to get tailored responses:
    * `recruiter`: Provides concise, resume-only answers.
    * `career_coach`: Offers supportive and realistic career guidance.
    * `detailed`: Gives thorough explanations with examples.
* **Streaming & Non-Streaming:** Supports both JSON (non-streaming) and plain-text (streaming) responses.
* **Built for Production:** Includes **CORS** support and **rate limiting** to prevent abuse.
* **Easy Deployment:** Designed for minimal setup on platforms like **Render**.

---

### 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **LLM API:** Google Gemini
* **Deployment:** Render

### ⚙️ Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Gojer16/Orlando-AI-Assistant
    cd Orlando-AI-Assistant
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set your environment variable:**
    ```bash
    export GEMINI_API_KEY=your_api_key
    ```
4.  **Run the application:**
    ```bash
    flask run --host=0.0.0.0 --port=5000
    ```

---

### `POST /chat`

This endpoint processes user questions and returns an AI-generated answer.

#### Request Body
```json
{
  "question": "What is Orlando's strongest skill?",
  "role": "recruiter",     // Optional, default = 'detailed'
  "stream": false          // Optional, default = false
}
```
### 🧭 Next Steps & Future Enhancements
1. **RAG (Retrieval-Augmented Generation):** Add RAG to ground the model on longer documents, enabling it to answer questions on more than just a single resume.

2. **LangChain Integration:** Use LangChain for creating more structured pipelines and persistent memory, allowing for multi-turn conversations.

3. **Expand Roles:** Develop more advanced and specialized prompts for new system roles.

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

---

## 📜 License

This project is licensed under the MIT License.
