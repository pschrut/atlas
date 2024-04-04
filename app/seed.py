import os
from dotenv import load_dotenv

load_dotenv()

def seed_database():
    from app.models import User, Role
    from app import db, bcrypt

    if db.session.query(Role).count() == 0:
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()

    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username=os.getenv('ADMIN_USERNAME'),
            email=os.getenv('ADMIN_EMAIL'),
            password=bcrypt.generate_password_hash(os.getenv('ADMIN_PASSWORD')).decode('utf-8'),
            role_id=Role.query.filter_by(name='admin').first().id
        )
        
        db.session.add(admin_user)
        db.session.commit()