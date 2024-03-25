from flask import request, jsonify
from flask_login import login_required, logout_user, login_user
from app.models import User
from app import bcrypt
from app import db

def login():
    user = request.form.get('user')
    password = request.form.get('password')

    user = User.query.filter(User.username == user).first()
    if user is None:
        return jsonify({ 'error': 'User not found' }), 404
    else:
        if bcrypt.check_password_hash(user.password, password) == False:
            return jsonify({ 'error': 'Invalid password' }), 401
        else:
            login_user(user)

    return jsonify({ 'message': 'Logged in' }), 200

def register():    
    user = request.form.get('user')
    email = request.form.get('email')
    password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')

    user = User(username=user, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({ 'message': 'User created' }), 201

@login_required
def logout():
    logout_user()
    return jsonify({ 'message': 'Logged out' }), 200