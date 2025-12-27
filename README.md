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
6.  **File Bonus**
7.  **Referensi dan Dataset**
8.  **Feedback dan Kontribusi**
9.  **Author**

---

## Gambaran Umum

**Love Compatibility Analyzer** adalah sebuah aplikasi web cerdas berbasis **Flask** yang memadukan **Machine Learning** dan kekuatan naratif dari **Google Gemini AI** untuk memprediksi dan menceritakan potensi kisah berdasarkan data dari *Speed Dating Experiment*.

---

## Struktur Proyek

```
Love-Compatibility-Analyzer/
├── app/
│   ├── main/
│   │   ├── routes.py			# Semua logika rute, halaman, dan GeminiCall
│   │   └── main.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── loading.html
│   │   ├── index_lanjutan.html
│   │   ├── dashboard.html
│   │   ├── form_lanjutan.html
│   │   └── result_lanjutan.html
│   ├── forms.py			# Formulir login & registrasi
│   ├── models.py			# Model database (User, Analysis)
│   └── __init__.py			# Inisialisasi aplikasi (App Factory)
├── love_compatibility_model.pkl	# Model RandomForestClassifier yang telah dioptimalkan
├── pelatihan_model_lanjutan.py		# Script untuk data preprocessing dan tuning model
├── Speed Dating Data.csv		# Dataset asli yang digunakan untuk pelatihan
├── requirements.txt			# Daftar Dependensi Python
├── config.py
├── ListModelGemini.py			# Daftar model Gemini yang bisa digunkan
├── GeminiCLI.py			# File Bonus
├── README.md
└── run.py				# Entry point untuk menjalankan aplikasi
```

> _"Ganti model sesuai keinginan kamu, atur dan ganti model Gemini API di file **app/main/routes.py**, lihat lebih detail lihat bagian **File Bonus**"_

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

  - **Windows/Mac/Linux**

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

- Membuat akun admin

    ```bash
    flask create-admin
    ```

7.  Jalankan Aplikasi

    ```bash
    flask run
    ```

8.  Buka browser web kamu dan akses:

    ```
    http://127.0.0.1:5000
    ```

---

## File Bonus

**GeminiCLI.py** pada dasarnya untuk membuat pengecekan pada respon model yang akan digunkaan, tapi bisa juga digunakan lebih lanjut dengan tujuan yang positif.

### Step by step:

1. Pastikan sebelumnya anda telah mendapatkan kunci API dari **(https://aistudio.google.com/app/apikey)**

2. Export variable Gemini API

  - **Windows**
    ```bash
    $env:GOOGLE_API_KEY = "kunci_api_google_anda"   
    ```
  - **Mac/Linux**
    ```bash
    export GOOGLE_API_KEY="kunci_api_google_anda"
    ```

3. Cek Model yang tersedia untuk Gemini API

    ```bash
    python3 ListModelGemini.py
    ```

4. Atur Model dan promt sesuai keinginanmu dan lihat lah hasilnya setelah kamu menjalankannya

    ```bash
    python3 GeminiCLI.py
    ```

### Contoh Praktik:

```
(0-0) fufufafa@whoiam:~/Love-Compatibility-Analyzer$ export GOOGLE_API_KEY="kunci_api_google_anda"
(0-0) fufufafa@whoiam:~/Love-Compatibility-Analyzer$ python ListModelGemini.py
models/embedding-gecko-001
models/gemini-2.5-flash
models/gemini-2.5-pro
models/gemini-2.0-flash-exp
models/gemini-2.0-flash
models/gemini-2.0-flash-001
models/gemini-2.0-flash-exp-image-generation
models/gemini-2.0-flash-lite-001
models/gemini-2.0-flash-lite
models/gemini-2.0-flash-lite-preview-02-05
models/gemini-2.0-flash-lite-preview
models/gemini-exp-1206
models/gemini-2.5-flash-preview-tts
...
...
...
(0-0) fufufafa@whoiam:~/Love-Compatibility-Analyzer$ cat GeminiCLI.py
from google import genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents="Jawab dengan singkat: tips untuk public speaking dengan profesional dan friendly"
)

print(response.text)
(0-0) fufufafa@whoiam:~/Love-Compatibility-Analyzer$ python GeminiCLI.py
Berikut tipsnya:

1.  **Kuasai Materi:** Pahami betul topikmu, strukturkan dengan jelas. (Profesional)
2.  **Artikulasi Jelas & Intonasi Bervariasi:** Bicara terang, tidak monoton. (Profesional & Friendly)
3.  **Kontak Mata Merata & Senyum Tulus:** Jalin koneksi, terlihat ramah dan percaya diri. (Profesional & Friendly)
4.  **Gestur Alami:** Gunakan tangan untuk mendukung poin, jangan kaku. (Profesional & Friendly)
5.  **Bahasa Mudah Dicerna:** Hindari jargon, selipkan cerita/contoh relevan. (Friendly)
6.  **Libatkan Audiens:** Ajukan pertanyaan retoris, beri jeda. (Friendly)
7.  **Antusias & Autentik:** Tunjukkan *passion*, jadilah diri sendiri. (Profesional & Friendly)
(0-0) fufufafa@whoiam:~/Love-Compatibility-Analyzer$
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
