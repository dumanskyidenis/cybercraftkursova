from database import db

class Motherboard(db.Model):
    __tablename__ = 'motherboards'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    socket = db.Column(db.String(50), nullable=False)
    chipset = db.Column(db.String(20), nullable=False)
    form = db.Column(db.String(20), nullable=False)
    slots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    memory_type = db.Column(db.String(20), default='DDR4')

    