from database import db

class Headset(db.Model):
    __tablename__ = 'headsets'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    conn = db.Column(db.String(50), nullable=False)
    mic = db.Column(db.Boolean, nullable=False)
    wireless = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)