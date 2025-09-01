from flask import Flask
from routes.chat import chat_bp
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    """
    Create and configure the Flask app.
    We register the chat blueprint so the app
    is a thin bootstrapper and routes live in routes/.
    """
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "https://react-basic-resume.vercel.app"}}) # URL

    limiter = Limiter(
        key_func=get_remote_address,   # identifies clients by IP
        app=app,    
        default_limits=["20 per minute"]  # global fallback
    )

    app.register_blueprint(chat_bp) # attach chat API

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)