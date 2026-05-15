from database import db

class Cooler(db.Model):
    __tablename__ = 'coolers'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    c_type = db.Column(db.String(20), nullable=False)
    tdp = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    socket = db.Column(db.String(100), default='AM4, AM5, LGA1700')