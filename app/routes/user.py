from flask import request, jsonify
from flask_login import login_required, logout_user, login_user, current_user
from app.models import User
from app import bcrypt
from app import db
from app.decorators import require_admin
from app.enums import Roles

def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).first()
    if user is None:
        return jsonify({ 'error': 'User not found' }), 404
    else:
        if bcrypt.check_password_hash(user.password, password) is False:
            return jsonify({ 'error': 'Invalid password' }), 401
        else:
            login_user(user)

    return jsonify({ 'logged_in_user': { 'id': user.id, 'username': user.username, 'isAdmin': user.role.id ==  Roles.ADMIN.value } }), 200

@login_required
@require_admin
def register():    
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')

    user = User(username=username, email=email, password=password, role_id=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({ 'message': { 'created_user': user.id } }), 201

@login_required
@require_admin
def users():
    query = User.query.all()
    users_list = [user.to_json() for user in query]

    return jsonify({ 'users': users_list })

@login_required
def roles():
    from app.models import Role

    query = Role.query.all()
    roles_list = [role.to_json() for role in query]

    return jsonify({ 'roles': roles_list })

@login_required
def logout():
    logout_user()
    return jsonify({ 'message': { 'status': 'logged_out' } }), 200

def check_session():    
    return jsonify({'isAuthenticated': current_user.is_authenticated}), 200