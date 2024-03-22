from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:edifier793@localhost/atlas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        from app.models import User, Transaction, Period
        from app.routes.routes import transactions_bp
        
        db.create_all()
        app.register_blueprint(transactions_bp)

    return app
