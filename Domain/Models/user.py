from database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True, default="")
    
    # Зв'язок один-до-багатьох: один користувач може мати багато збережених збірок
    saved_builds = db.relationship('SavedBuild', backref='owner', lazy=True, cascade="all, delete-orphan")