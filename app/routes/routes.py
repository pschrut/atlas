from flask import Blueprint
from app.routes.xml_process import upload_transactions
from app.routes.data_process import transactions, balance

transactions_bp = Blueprint('transactions', __name__)
transactions_bp.add_url_rule('/upload_transactions', 'upload_transactions', upload_transactions, methods=['POST'])
transactions_bp.add_url_rule('/transactions', 'transactions', transactions)
transactions_bp.add_url_rule('/balance', 'balance', balance)
