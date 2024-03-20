from flask import Blueprint
from .xml_process import upload_transactions

xml_uploader_bp = Blueprint('xml_uploader', __name__)
xml_uploader_bp.add_url_rule('/upload_transactions', 'upload_transactions', upload_transactions, methods=['POST'])
