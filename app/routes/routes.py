from flask import Blueprint
from app.routes.xml_process import upload_transactions
from app.routes.data_process import transactions, balance
from app.routes.user import login, logout, register, check_session
from flask_cors import CORS

transactions_bp = Blueprint('transactions', __name__)
transactions_bp.add_url_rule('/upload_transactions', 'upload_transactions', upload_transactions, methods=['POST'])
transactions_bp.add_url_rule('/transactions', 'transactions', transactions)
transactions_bp.add_url_rule('/balance', 'balance', balance)

user_bp = Blueprint('user', __name__)
user_bp.add_url_rule('/login', 'login', login, methods=['POST'])
user_bp.add_url_rule('/logout', 'logout', logout, methods=['POST'])
user_bp.add_url_rule('/register', 'register', register, methods=['POST'])
user_bp.add_url_rule('/check_session', 'check_session', check_session, methods=['GET'])
