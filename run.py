# run.py
# File ini adalah titik masuk (entry point) baru untuk menjalankan aplikasi Anda.
# Tugasnya sederhana: mengimpor dan menjalankan instance aplikasi dari paket 'app'.

from app import create_app, db
from app.models import User, Analysis

# Membuat instance aplikasi menggunakan fungsi factory 'create_app'
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Membuat shell context agar bisa melakukan testing database
    langsung dari terminal flask. Cukup jalankan `flask shell`.
    """
    return {'db': db, 'User': User, 'Analysis': Analysis}

if __name__ == '__main__':
    app.run(debug=True)
