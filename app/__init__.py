from flask import Flask, session, g
from app.routes.routes import transactions_bp

app = Flask(__name__)

# def inject_user():
#     if 'user_id' in session:
#         user_id = session['user_id']
#         user = 'pablo'
#         return dict(user=user)
    
#     return dict(user=None) 

# @app.route('/')
# def index():
#     if g.user:
#         return f'Hello, {g.user["username"]}!'
#     else:
#         return 'Hello, guest!'

app.register_blueprint(transactions_bp)