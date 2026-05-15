from database import db

class RAM(db.Model):
    __tablename__ = 'rams'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    cap = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    r_type = db.Column(db.String(10), nullable=False)
    modules = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)