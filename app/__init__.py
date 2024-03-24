from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager
import os
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_ALCHEMY_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager = LoginManager()
    login_manager.init_app(app)
    
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        from app.models import User, Transaction, Period
        from app.routes.routes import transactions_bp, user_bp
        
        db.create_all()
        app.register_blueprint(transactions_bp)
        app.register_blueprint(user_bp)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    return app
