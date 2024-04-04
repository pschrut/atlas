from app import db
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('roles', lazy=True))
    periods = db.relationship('Period', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.email
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': {
                'id': self.role.id,
                'name': self.role.name
            }
        }