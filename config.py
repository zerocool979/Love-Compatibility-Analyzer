# config.py
# Menyimpan semua variabel konfigurasi untuk aplikasi.
# Memisahkan konfigurasi membuat aplikasi lebih aman dan mudah dikelola.

import os

# Menentukan direktori dasar proyek
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Kelas konfigurasi dasar.
    """
    # Kunci rahasia untuk melindungi formulir dan sesi dari serangan CSRF.
    # PENTING: Ganti dengan string acak yang sangat kuat di lingkungan produksi!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-yang-sangat-sulit-ditebak'

    # Konfigurasi database SQLAlchemy
    # Menggunakan SQLite untuk kemudahan setup. File database akan bernama 'site.db'.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Menonaktifkan fitur modifikasi track dari SQLAlchemy yang tidak kita butuhkan
    SQLALCHEMY_TRACK_MODIFICATIONS = False
