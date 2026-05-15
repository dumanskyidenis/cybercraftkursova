from database import db

class SavedBuild(db.Model):
    __tablename__ = 'saved_builds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    build_name = db.Column(db.String(100), default="Моя збірка")
    
    # === ОСНОВНІ КОМПЛЕКТУЮЧІ ===
    cpu_id = db.Column(db.Integer, db.ForeignKey('cpus.id'), nullable=True)
    gpu_id = db.Column(db.Integer, db.ForeignKey('gpus.id'), nullable=True)
    motherboard_id = db.Column(db.Integer, db.ForeignKey('motherboards.id'), nullable=True)
    ram_id = db.Column(db.Integer, db.ForeignKey('rams.id'), nullable=True)
    storage_id = db.Column(db.Integer, db.ForeignKey('storages.id'), nullable=True)
    psu_id = db.Column(db.Integer, db.ForeignKey('psus.id'), nullable=True)
    cooler_id = db.Column(db.Integer, db.ForeignKey('coolers.id'), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    
    # === ПЕРИФЕРІЯ ===
    mouse_id = db.Column(db.Integer, db.ForeignKey('mice.id'), nullable=True) 
    keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboards.id'), nullable=True)
    headset_id = db.Column(db.Integer, db.ForeignKey('headsets.id'), nullable=True)