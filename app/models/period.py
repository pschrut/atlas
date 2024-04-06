from app import db

class Period(db.Model):
    __tablename__ = 'periods'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), nullable=False)
    description = db.Column(db.String(100))
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Period %r>' % self.id
    
    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'startDate': self.startDate,
            'endDate': self.endDate
        }