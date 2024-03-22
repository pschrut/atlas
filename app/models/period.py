from app import db

class Period(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    description = db.Column(db.String(100))
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)

    def __repr__(self):
        return '<Period %r>' % self.id