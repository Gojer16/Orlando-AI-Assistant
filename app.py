from flask import Flask
from routes.chat import chat_bp
from flask_cors import CORS

def create_app():
    """
    Create and configure the Flask app.
    We register the chat blueprint so the app
    is a thin bootstrapper and routes live in routes/.
    """
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173"])
    app.register_blueprint(chat_bp) # attach chat API

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)