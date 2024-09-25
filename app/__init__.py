from flask import Flask
from app.database import init_db, close_db
from app.routes.posts import post_bp
from app.routes.users import user_bp
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    init_db(app)
    app.register_blueprint(post_bp)
    app.register_blueprint(user_bp)
    app.teardown_appcontext(close_db)
    return app
