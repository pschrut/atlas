from flask import request, jsonify
from flask_login import login_required, logout_user, login_user
from app.models import User

def login():
    user = request.form.get('user')
    password = request.form.get('password')

    user = User.query.filter(User.username == user).first()
    if user is None:
        return jsonify({ 'error': 'User not found' }), 404
    else:
        if user.password != password:
            return jsonify({ 'error': 'Invalid password' }), 401
        else:
            login_user(user)

    return jsonify({ 'message': 'Logged in' }), 200

@login_required
def logout():
    logout_user()
    return jsonify({ 'message': 'Logged out' }), 200