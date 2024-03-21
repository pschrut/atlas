from flask import Flask, session, g
from api.routes.routes import transactions_bp

api = Flask(__name__)

api.register_blueprint(transactions_bp)