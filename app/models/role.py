from app import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role(name={self.name})>"

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }