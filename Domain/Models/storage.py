from database import db

class Storage(db.Model):
    __tablename__ = 'storages'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    s_type = db.Column(db.String(20), nullable=False)
    cap = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    interface = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)