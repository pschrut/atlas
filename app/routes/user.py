from flask import request, jsonify
from flask_login import login_required, logout_user, login_user, current_user
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
        if bcrypt.check_password_hash(user.password, password) is False:
            return jsonify({ 'error': 'Invalid password' }), 401
        else:
            login_user(user)

    return jsonify({ 'logged_in_user': { 'id': user.id, 'username': user.username } }), 200

def register():    
    user = request.form.get('user')
    email = request.form.get('email')
    password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')

    user = User(username=user, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({ 'message': { 'created_user': user.id } }), 201

@login_required
def logout():
    logout_user()
    return jsonify({ 'message': { 'status': 'logged_out' } }), 200

def check_session():    
    return jsonify({'isAuthenticated': current_user.is_authenticated}), 200