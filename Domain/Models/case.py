from database import db

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    form = db.Column(db.String(20), nullable=False)
    gpu_m = db.Column(db.Integer, nullable=False)
    cool_m = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)