# pelatihan_model_lanjutan.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import warnings

warnings.filterwarnings('ignore')

def train_and_save_advanced_model(data_path='Speed Dating Data.csv'):
    """
    Fungsi ini memuat data, melakukan rekayasa fitur,
    membuat pipeline pra-pemrosesan & model, melatihnya, dan menyimpannya.
    """
    print("Memulai proses pelatihan model LANJUTAN...")

    # --- 1. Memuat Data ---
    try:
        df = pd.read_csv(data_path, encoding='ISO-8859-1')
        print(f"Data berhasil dimuat. Shape awal: {df.shape}")
    except FileNotFoundError:
        print(f"Error: File '{data_path}' tidak ditemukan.")
        return

    # --- 2. Rekayasa & Pemilihan Fitur (Feature Engineering & Selection) ---
    # Fitur yang akan kita gunakan dari form input pengguna
    # Ini adalah kombinasi dari penilaian diri, preferensi, dan minat
    features = [
        # Preferensi Partisipan 1 (akan diisi dari form)
        'attr1_1', 'sinc1_1', 'intel1_1', 'fun1_1', 'amb1_1', 'shar1_1',
        # Penilaian Partisipan 1 terhadap Partisipan 2 (akan disimulasikan/diisi dari form)
        'attr', 'sinc', 'intel', 'fun', 'amb', 'shar', 'like',
        # Minat (akan dihitung kesamaannya)
        'sports', 'tvsports', 'exercise', 'dining', 'museums', 'art',
        'hiking', 'gaming', 'clubbing', 'reading', 'tv', 'theater',
        'movies', 'concerts', 'music', 'shopping', 'yoga',
        # Demografi
        'age', 'age_o',
        # Fitur baru hasil rekayasa
        'age_diff', 'interest_similarity'
    ]
    target = 'match'

    # Membuat fitur rekayasa
    # Perbedaan Usia
    df['age_diff'] = abs(df['age'] - df['age_o'])

    # Kesamaan Minat (Interest Similarity)
    interest_cols = ['sports', 'tvsports', 'exercise', 'dining', 'museums', 'art', 'hiking', 'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies', 'concerts', 'music', 'shopping', 'yoga']
    
    # Untuk menghitung kesamaan, kita perlu data pasangan. Data ini sudah berpasangan per baris.
    # Kita akan membuat fitur kesamaan minat berdasarkan data yang ada.
    # Di aplikasi, kita akan menghitung ini secara manual.
    # Untuk pelatihan, kita asumsikan data minat pasangan ada di kolom yang sama (ini adalah simplifikasi)
    # Dalam kasus nyata, kita perlu data minat dari kedua belah pihak.
    # Di sini, kita akan membuat fitur dummy untuk pelatihan.
    # Di aplikasi, kita akan hitung ini dari input dua orang.
    df['interest_similarity'] = df[interest_cols].sum(axis=1) / len(interest_cols) # Placeholder

    # Memilih kolom yang relevan
    # Kolom 'shar' (shared interests) bisa menjadi proksi yang baik untuk kesamaan minat
    df['interest_similarity'] = df['shar']

    # Final feature list
    final_features = [
        'attr1_1', 'sinc1_1', 'intel1_1', 'fun1_1', 'amb1_1', 'shar1_1',
        'attr', 'sinc', 'intel', 'fun', 'amb', 'like',
        'age', 'age_o', 'age_diff', 'interest_similarity'
    ]
    target = 'match'

    df_selected = df[final_features + [target]].copy().dropna()
    print(f"Shape setelah pemilihan fitur dan dropna: {df_selected.shape}")

    # --- 3. Membangun Pipeline ---
    # Pipeline menggabungkan beberapa langkah menjadi satu.
    # 1. SimpleImputer: Mengisi nilai yang hilang.
    # 2. StandardScaler: Menyesuaikan skala semua fitur.
    # 3. RandomForestClassifier: Model machine learning.
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=150, random_state=42, max_depth=10, min_samples_leaf=5))
    ])
    print("Pipeline berhasil dibuat.")

    # --- 4. Memisahkan Data dan Melatih Model ---
    X = df_selected[final_features]
    y = df_selected[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Melatih pipeline pada data pelatihan...")
    pipeline.fit(X_train, y_train)
    print("Pipeline berhasil dilatih.")

    # --- 5. Mengevaluasi Model ---
    print("\nMengevaluasi performa pipeline pada data pengujian...")
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Akurasi Pipeline: {accuracy:.2%}")
    print("\nLaporan Klasifikasi:")
    print(classification_report(y_test, y_pred))

    # --- 6. Menyimpan Pipeline yang Telah Dilatih ---
    output_filename = 'love_compatibility_model.pkl'
    joblib.dump(pipeline, output_filename)
    print(f"\nPipeline telah berhasil disimpan sebagai '{output_filename}'")
    print("File ini sekarang siap digunakan di aplikasi Flask Anda.")


if __name__ == '__main__':
    train_and_save_advanced_model()
