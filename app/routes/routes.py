from flask import Blueprint
from app.routes.xml_process import upload_transactions, test_endpoint
from app.routes.data_process import transactions, balance
from app.routes.user import login, logout, register
from flask_cors import CORS

transactions_bp = Blueprint('transactions', __name__)
transactions_bp.add_url_rule('/upload_transactions', 'upload_transactions', upload_transactions, methods=['POST'])
transactions_bp.add_url_rule('/transactions', 'transactions', transactions)
transactions_bp.add_url_rule('/balance', 'balance', balance)
transactions_bp.add_url_rule('/test', 'test', test_endpoint)

user_bp = Blueprint('user', __name__)
user_bp.add_url_rule('/login', 'login', login, methods=['POST'])
user_bp.add_url_rule('/logout', 'logout', logout, methods=['POST'])
user_bp.add_url_rule('/register', 'register', register, methods=['POST'])
