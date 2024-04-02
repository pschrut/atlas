from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import DevelopmentConfig
import logging

logging.basicConfig(filename='atlas.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)

def create_app():
    app.config.from_object(DevelopmentConfig)

    login_manager = LoginManager()
    
    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        from app.models import User, Transaction, Period
        from app.routes import transactions_bp, user_bp
        
        db.create_all()

        CORS(user_bp, supports_credentials=True)
        CORS(transactions_bp, supports_credentials=True)

        app.register_blueprint(transactions_bp)
        app.register_blueprint(user_bp)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    return app
