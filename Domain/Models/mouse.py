from database import db

class Mouse(db.Model):
    __tablename__ = 'mice'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    dpi = db.Column(db.Integer, nullable=False)
    sensor = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    wireless = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)