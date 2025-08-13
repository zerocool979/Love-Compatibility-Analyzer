<p align="center">
  <img src="https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif" width="100%" alt="anime banner">
</p>

<h1 align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&duration=3000&pause=1000&color=FF6F61&center=true&vCenter=true&width=440&lines=Love+Compatibility+Analyzer;Possibility+of+Falling+in+Love..." alt="Typing SVG" />
</h1>

<p align="center"><i><strong>Apakah cinta bisa dianalisis dengan data?</strong><br>Temui aplikasi web cerdas berbasis Machine Learning yang mencoba menjawab pertanyaan paling klasik dalam sejarah umat manusia: “Apakah dia juga suka aku?”</i></p>

<p align="center">
  <a href="https://github.com/zerocool979/Love-Compatibility-Analyzer" target="_blank">
    <img src="https://img.shields.io/badge/Deploy%20Link-Coming%20Soon-blueviolet?style=for-the-badge&logo=vercel" alt="Deploy Link">
  </a>
</p>

---

## Lampiran

1.  **Gambaran Umum**
2.  **Struktur Proyek**
3.  **Fitur Unggulan**
4.  **Teknologi yang Digunakan**
5.  **Cara Menjalankan Secara Lokal**
6.  **Referensi dan Dataset**
7.  **Feedback dan Kontribusi**
8.  **Author**

---

---

## Gambaran Umum

**Love Compatibility Analyzer** adalah sebuah aplikasi web cerdas berbasis **Flask** yang memadukan **Machine Learning** dan kekuatan naratif dari **Google Gemini AI** untuk memprediksi dan menceritakan potensi kisah berdasarkan data dari *Speed Dating Experiment*.

---

## Struktur Proyek

Berikut adalah arsitektur folder dan file yang membentuk proyek ini:

- [Love-Compatibility-Analyzer/](https://github.com/zerocool979/Love-Compatibility-Analyzer)
  - `./run.py` – Entry point untuk menjalankan aplikasi
  - `./pelatihan_model_lanjutan.py` – Script untuk data preprocessing dan tuning model
  - `./pelatihan_model_lanjutan.pkl` – Model RandomForestClassifier yang telah dioptimalkan
  - `./Speed-Dating-Data.csv` – Dataset asli yang digunakan untuk pelatihan
  - `./requirements.txt` - Daftar Dependensi Python
- [app/](./app/)
  - `./app/__init__.py` – Inisialisasi aplikasi (App Factory)
  - `./app/models.py` – Model database (User, Analysis)
  - `./app/forms.py` - Formulir login & registrasi
    - [app/main/](./app/main/)
      - `./app/main/routes.py` – Semua logika rute & halaman
    - [app/templates](./app/templates/)
      - `./app/templates/base.html`
      - `./app/templates/dashboard.html`
      - `./app/templates/form_lanjutan.html`
      - `./app/templates/loading.html`
      - `./app/templates/login.html`
      - `./app/templates/register.html`
      - `./app/templates/result_lanjutan.html`
  ---

> _"Beberapa file mungkin tidak tersedia dan akan otomatis tersedia jika user mempraktekannya langsung. Hal ini dikarenakan kami ingin user dapat merasakan bagaimana rasanya menggunakan proyek ini secara langsung"_

---

## Fitur-fitur Unggulan

Proyek ini dibangun dengan serangkaian fitur yang membuatnya fungsional, akurat, dan menarik.

### Model & Data

1. **Prediksi Berbasis Data** : Skor kecocokan dihitung menggunakan model **Machine Learning** yang dilatih pada data **Speed Dating Experiment** nyata.

2. **Akun Pengguna & Riwayat** : Buat akun, login, dan simpan semua hasil analisis Anda dalam dasbor pribadi yang modern.

3. **AI Storyteller (Google Gemini)** : Dapatkan narasi unik yang dihasilkan **AI**, mencakup:

	- Kisah Pertemuan yang personal.

	- Analisis Kepribadian yang mendalam.

	- Prediksi Bahasa Cinta (Love Language).

	- Ide Kencan yang kreatif.

4. **Halaman Hasil Interaktif** : Halaman hasil bukan akhir. **Regenerasi cerita** atau minta **ide kencan baru** dengan sekali klik.

5. **Bagikan Hasilmu** : Buat dan bagikan gambar ringkasan hasil analisis Anda yang estetik, siap untuk media sosial.
---

## Teknologi yang Digunakan
- **Backend** : Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Machine Learning** : Scikit-learn, Pandas, Joblib
- **Generative AI** : Google Gemini AI (gemini-1.5-flash-latest)
- **Database** : SQlite
- **Image Processing** : Pillow
- **Frontend** : HTML, Tailwind CSS, Javascript, Chart.js

---

## Cara Menjalankan Secara Lokal

Ikuti langkah-langkah ini untuk menjalankan proyek di komputer Anda.

1. Prasyarat 

  - **Python** 3.10+
  - **Git**

2.  Clone repository ini ke komputer kamu:
    ```bash
    git clone https://github.com/zerocool979/Love-Compatibility-Analyzer.git
    cd Love-Compatibility-Analyzer
    ```

3. Buat dan Aktifkan Virtual Environment

  - **Windows** :

    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```

  - **Mac/Linux**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  Install Dependensi

Pastikan memiliki file `requirements.txt`. Jika belum, buat dengan `pip freeze > requirements.txt`. Lalu jalankan:

    ```bash
    pip install -r requirements.txt
    ```

5.  Atur Environment Variable

Anda harus mengatus 2 variable penting.

  - **SECRET_KEY** : Untuk keamanan sesi Flask.
  - **GOOGLE_API_KEY** : Kunci API dari Google AI Studio.
> _"Catatan : Dapatkan kunci API dari (https://aistudio.google.com/app/apikey)"_

  - **Windows**
    ```bash
    $env:SECRET_KEY = "kunci_rahasia_acak_anda"
    $env:GOOGLE_API_KEY = "kunci_api_google_anda"   
    ```

  - **Mac/Linux**
    ```bash
    export SECRET_KEY="kunci_rahasia_acak_anda"
    export GOOGLE_API_KEY="kunci_api_google_anda"
    ```

6.  Inisialisasi Database

Langkah ini hanya perlu dilakukan sekali untuk membuat file `app.db`.

- Atur entry point aplikasi
    ```bash
    export FLASK_APP=run.py  # (Untuk Mac/Linux)
    set FLASK_APP=run.py     # (Untuk Windows)
    ```

- Masuk ke shell Flask

    ```bash
    flask shell
    ```

- Di dalam shell, jalankan:

    ```bash
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

7.  Jalankan Aplikasi

    ```bash
    flask run
    ```

8.  Buka browser web kamu dan akses:

    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

---

## Referensi dan Dataset

- **Dataset**: [Speed Dating Experiment Data](https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment) dari Kaggle, yang merupakan eksperimen nyata untuk mempelajari faktor-faktor ketertarikan romantis.

---

## Feedback dan Kontribusi

Kami percaya cinta itu dinamis — begitu juga dengan proyek ini!
Sangat terbuka untuk setiap saran, laporan *bug*, atau kontribusi kode. Jangan ragu untuk membuat *Pull Request* atau membuka *Issue*.

Terutama, jangan lupa untuk mengisi formulir umpan balik di halaman web — kami membaca semua umpan balik untuk terus meningkatkan akurasi model .

---

## Author

**zerocool979**
GitHub: [@zerocool979](https://github.com/zerocool979)

---

> _"Machine Learning can’t guarantee true love… but hey, at least it can give you a hint!"_ – someone strange
