import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()  # read .env if present

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
    max_mb = int(os.environ.get('MAX_CONTENT_MB', '30'))
    app.config['MAX_CONTENT_LENGTH'] = max_mb * 1024 * 1024

    # register blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
