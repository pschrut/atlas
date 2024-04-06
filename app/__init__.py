from flask import Flask
from flask_cors import CORS
from app.config import DevelopmentConfig
from app.seed import seed_database
from app.extensions import db, bcrypt, migrate, login_manager
import logging

logging.basicConfig(filename='atlas.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def create_app():
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    with app.app_context():
        from app.models import User, Transaction, Period, Role
        from app.routes import transactions_bp, user_bp
        
        db.create_all()
        seed_database()

        CORS(user_bp, supports_credentials=True)
        CORS(transactions_bp, supports_credentials=True)

        app.register_blueprint(transactions_bp)
        app.register_blueprint(user_bp)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    return app
