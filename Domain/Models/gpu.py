from database import db

class GPU(db.Model):
    __tablename__ = 'gpus'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    vram = db.Column(db.String(20), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    psu_req = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    gpu_mark = db.Column(db.Integer, default=20000)