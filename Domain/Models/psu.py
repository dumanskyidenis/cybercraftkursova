from database import db

class PSU(db.Model):
    __tablename__ = 'psus'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    watts = db.Column(db.Integer, nullable=False)
    eff = db.Column(db.String(20), nullable=False)
    modular = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)