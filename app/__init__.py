from flask import Flask
from .routes.xml_uploader import xml_uploader_bp

app = Flask(__name__)
app.register_blueprint(xml_uploader_bp)