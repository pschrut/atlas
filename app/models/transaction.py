from app import db

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.String(6), db.ForeignKey('periods.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    comments = db.Column(db.String(100))
    period = db.relationship('Period', backref=db.backref('transactions', lazy=True))
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return '<Transaction %r>' % self.id
    
    def to_json(self):
        return {
            'id': self.id,
            'period_id': self.period_id,
            'user_id': self.user_id,
            'date': self.date,
            'description': self.description,
            'value': self.value,
            'type': self.type,
            'comments': self.comments
        }