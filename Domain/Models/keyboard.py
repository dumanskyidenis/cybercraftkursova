from database import db

class Keyboard(db.Model):
    __tablename__ = 'keyboards'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    switches = db.Column(db.String(50), nullable=False)
    layout = db.Column(db.String(20), nullable=False)
    rgb = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)