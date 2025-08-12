# app/models.py
# Mendefinisikan struktur tabel database menggunakan model SQLAlchemy.

from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    """Fungsi yang dibutuhkan oleh Flask-Login untuk memuat user dari sesi."""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """Model untuk tabel pengguna."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # Relasi ke tabel Analysis: satu pengguna bisa memiliki banyak analisis
    analyses = db.relationship('Analysis', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Analysis(db.Model):
    """Model untuk menyimpan setiap hasil analisis."""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Data profil
    profile1_name = db.Column(db.String(100), nullable=False)
    profile2_name = db.Column(db.String(100), nullable=False)
    
    # Hasil
    score = db.Column(db.Integer, nullable=False)
    love_story = db.Column(db.Text, nullable=False)
    date_idea = db.Column(db.Text, nullable=False)
    
    # Data mentah untuk ditampilkan kembali (disimpan sebagai JSON string)
    raw_data = db.Column(db.Text, nullable=False)
    
    # Kunci asing yang menghubungkan ke tabel User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Analysis(Score: {self.score} for user {self.user_id})"

class Feedback(db.Model):
    """Model untuk menyimpan umpan balik pengguna."""
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_accurate = db.Column(db.Boolean, nullable=False) # True for '👍', False for '👎'
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Feedback('{self.is_accurate}' for Analysis {self.analysis_id})"
