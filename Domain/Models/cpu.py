from database import db

class CPU(db.Model):
    __tablename__ = 'cpus'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    socket = db.Column(db.String(50), nullable=False)
    cores = db.Column(db.Integer, nullable=False)
    threads = db.Column(db.Integer, nullable=False)
    clock = db.Column(db.Float, nullable=False)
    tdp = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cpu_mark = db.Column(db.Integer, default=15000)