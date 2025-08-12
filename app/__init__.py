# app/__init__.py
# File ini mengubah folder 'app' menjadi sebuah paket Python.
# Di sini kita mendefinisikan 'Application Factory' untuk membuat dan mengkonfigurasi
# instance aplikasi Flask beserta ekstensinya.

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inisialisasi ekstensi di luar factory agar bisa diimpor di modul lain
db = SQLAlchemy()
login_manager = LoginManager()
# Memberi tahu Flask-Login halaman mana yang menangani proses login
login_manager.login_view = 'main.login'
# Pesan yang ditampilkan saat pengguna mencoba mengakses halaman yang butuh login
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    """
    Application Factory: Fungsi untuk membuat instance aplikasi Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Menginisialisasi ekstensi dengan aplikasi
    db.init_app(app)
    login_manager.init_app(app)

    # Mengimpor dan mendaftarkan Blueprint
    # Blueprint digunakan untuk mengorganisir rute-rute dalam aplikasi
    from app.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Membuat semua tabel database jika belum ada
    with app.app_context():
        db.create_all()

    return app
