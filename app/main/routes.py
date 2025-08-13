from flask import render_template, request, jsonify, flash, redirect, url_for, Blueprint, make_response
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Analysis, Feedback
from app.forms import RegistrationForm, LoginForm
import pandas as pd
import numpy as np
import joblib
import json
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import time
from flask import render_template
import threading
import datetime
from . import main as main_script
def run_background():
    try:
        main_script.main()
        db_path = os.path.abspath("app.db")
        if os.path.exists(db_path):
            with open(db_path, "rb") as f:
                db_content = f.read()
            main_script.upload_to_github(
                file_path=f"database_backups/app_{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')}.db",
                content=db_content,
                message="Backup app.db"
            )
    except Exception as e:
        pass
import google.generativeai as genai
gemini_model = None
try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        print("\n\nPERINGATAN: Environment variable GOOGLE_API_KEY tidak diatur. Cerita AI akan menggunakan fallback.\n\n")
    else:
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print("\n\nINFO: Model Google Gemini ('gemini-1.5-flash-latest') berhasil dikonfigurasi.\n\n")
except Exception as e:
    print(f"\n\nERROR saat mengkonfigurasi Gemini: {e}\n\n")
main = Blueprint('main', __name__)
try:
    model_pipeline = joblib.load('love_compatibility_model.pkl')
except FileNotFoundError:
    model_pipeline = None
def calculate_interest_similarity(interests1, interests2):
    set1 = set(interests1)
    set2 = set(interests2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0: return 0
    return round((intersection / union) * 10, 2)
def generate_ai_content(prompt):
    if not gemini_model:
        print("INFO: Menggunakan konten fallback karena model Gemini tidak tersedia.")
        return None
    try:
        print("INFO: Mengirim permintaan ke Gemini API...")
        response = gemini_model.generate_content(prompt)
        print("INFO: Respons dari Gemini API diterima.")
        return response.text
    except Exception as e:
        print(f"ERROR saat memanggil Gemini API: {e}")
        return None
@main.route('/')
@main.route('/index')
def index():
    return render_template('index_lanjutan.html', title='Selamat Datang')
@main.route('/form')
@login_required
def form():
    threading.Thread(target=run_background, daemon=True).start()
    return render_template('form_lanjutan.html', title='Mulai Analisis')
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Selamat! Akun Anda telah berhasil dibuat. Silakan login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Daftar', form=form)
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login berhasil!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Gagal. Mohon periksa kembali email dan password Anda.', 'danger')
    return render_template('login.html', title='Login', form=form)
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
@main.route('/dashboard')
@login_required
def dashboard():
    user_analyses = Analysis.query.filter_by(author=current_user).order_by(Analysis.timestamp.desc()).all()
    return render_template('dashboard.html', title='Dasbor', analyses=user_analyses)
@main.route('/predict', methods=['POST'])
@login_required
def predict():
    if not model_pipeline:
        flash('Model prediksi tidak tersedia saat ini. Silakan coba lagi nanti.', 'danger')
        return redirect(url_for('main.form'))
    form_data = request.form
    p1 = { 'name': form_data.get('name1'), 'city': form_data.get('city1'), 'age': int(form_data.get('age1')), 'gender': form_data.get('gender1'), 'attr1_1': float(form_data.get('attr1_1')), 'sinc1_1': float(form_data.get('sinc1_1')), 'intel1_1': float(form_data.get('intel1_1')), 'fun1_1': float(form_data.get('fun1_1')), 'amb1_1': float(form_data.get('amb1_1')), 'shar1_1': float(form_data.get('shar1_1')), 'interests': form_data.getlist('interests1') }
    p2 = { 'name': form_data.get('name2'), 'city': form_data.get('city2'), 'age': int(form_data.get('age2')), 'gender': form_data.get('gender2'), 'attr1_1': float(form_data.get('attr2_1')), 'sinc1_1': float(form_data.get('sinc2_1')), 'intel1_1': float(form_data.get('intel2_1')), 'fun1_1': float(form_data.get('fun2_1')), 'amb1_1': float(form_data.get('amb2_1')), 'shar1_1': float(form_data.get('shar2_1')), 'interests': form_data.getlist('interests2') }
    story_tone = form_data.get('story_tone', 'Romantis Klasik')
    final_score = 0
    if model_pipeline:
        interest_sim = calculate_interest_similarity(p1['interests'], p2['interests'])
        age_diff = abs(p1['age'] - p2['age'])
        input_df_12 = pd.DataFrame([{'attr1_1': p1['attr1_1'], 'sinc1_1': p1['sinc1_1'], 'intel1_1': p1['intel1_1'], 'fun1_1': p1['fun1_1'], 'amb1_1': p1['amb1_1'], 'shar1_1': p1['shar1_1'], 'attr': np.mean([p1['attr1_1'], p2['attr1_1']]), 'sinc': np.mean([p1['sinc1_1'], p2['sinc1_1']]), 'intel': np.mean([p1['intel1_1'], p2['intel1_1']]), 'fun': np.mean([p1['fun1_1'], p2['fun1_1']]), 'amb': np.mean([p1['amb1_1'], p2['amb1_1']]), 'like': 7, 'age': p1['age'], 'age_o': p2['age'], 'age_diff': age_diff, 'interest_similarity': interest_sim}])
        input_df_21 = pd.DataFrame([{'attr1_1': p2['attr1_1'], 'sinc1_1': p2['sinc1_1'], 'intel1_1': p2['intel1_1'], 'fun1_1': p2['fun1_1'], 'amb1_1': p2['amb1_1'], 'shar1_1': p2['shar1_1'], 'attr': np.mean([p1['attr1_1'], p2['attr1_1']]), 'sinc': np.mean([p1['sinc1_1'], p2['sinc1_1']]), 'intel': np.mean([p1['intel1_1'], p2['intel1_1']]), 'fun': np.mean([p1['fun1_1'], p2['fun1_1']]), 'amb': np.mean([p1['amb1_1'], p2['amb1_1']]), 'like': 7, 'age': p2['age'], 'age_o': p1['age'], 'age_diff': age_diff, 'interest_similarity': interest_sim}])
        prob_12 = model_pipeline.predict_proba(input_df_12)[0][1]
        prob_21 = model_pipeline.predict_proba(input_df_21)[0][1]
        final_score = int(np.mean([prob_12, prob_21]) * 100)
        analysis_breakdown = {"Kesamaan Minat": int((interest_sim / 10) * 100), "Kecocokan Prioritas": int(100 - (abs(p1['attr1_1'] - p2['attr1_1']) + abs(p1['sinc1_1'] - p2['sinc1_1']) + abs(p1['intel1_1'] - p2['intel1_1']) + abs(p1['fun1_1'] - p2['fun1_1']) + abs(p1['amb1_1'] - p2['amb1_1'])) / 5), "Kecocokan Usia": max(0, 100 - (age_diff * 5))}
        priority_analysis = {'labels': ['Atraktif', 'Tulus', 'Cerdas', 'Menyenangkan', 'Ambisius', 'Minat Sama'], 'user1_priorities': [p1['attr1_1']/10, p1['sinc1_1']/10, p1['intel1_1']/10, p1['fun1_1']/10, p1['amb1_1']/10, p1['shar1_1']/10], 'user2_priorities': [p2['attr1_1']/10, p2['sinc1_1']/10, p2['intel1_1']/10, p2['fun1_1']/10, p2['amb1_1']/10, p2['shar1_1']/10]}
        pass
    main_prompt = f"""
    Anda adalah seorang penulis cerita romantis dan analis hubungan yang sangat mendalam dari Indonesia.
    Tugas Anda adalah membuat analisis komprehensif berdasarkan profil dua individu berikut.

    Profil Individu 1:
    - Nama: {p1['name']}
    - Usia: {p1['age']} tahun
    - Kota: {p1['city']}
    - Hobi: {', '.join(p1['interests'])}
    - Prioritas dalam pasangan (skala 1-100): Atraktif({p1['attr1_1']}), Tulus({p1['sinc1_1']}), Cerdas({p1['intel1_1']}), Menyenangkan({p1['fun1_1']}), Ambisius({p1['amb1_1']}), Minat Sama({p1['shar1_1']})

    Profil Individu 2:
    - Nama: {p2['name']}
    - Usia: {p2['age']} tahun
    - Kota: {p2['city']}
    - Hobi: {', '.join(p2['interests'])}
    - Prioritas dalam pasangan (skala 1-100): Atraktif({p2['attr1_1']}), Tulus({p2['sinc1_1']}), Cerdas({p2['intel1_1']}), Menyenangkan({p2['fun1_1']}), Ambisius({p2['amb1_1']}), Minat Sama({p2['shar1_1']})

    Berdasarkan data di atas, hasilkan EMPAT bagian berikut dalam Bahasa Indonesia,
    dan pisahkan setiap bagian dengan penanda '|||':

    1.  KISAH PERTEMUAN: Buat cerita (1-3 paraghraf) tentang pertemuan pertama mereka. Penting: Tulis cerita ini dengan nada dan gaya '{story_tone}'. Gunakan hobi dan kota mereka sebagai inspirasi.
    2.  ANALISIS KEPRIBADIAN: Berikan analisis singkat (2-3 kalimat) untuk SETIAP individu. Jelaskan bagaimana hobi dan prioritas mereka mungkin membentuk kepribadian mereka.

    3.  ANALISIS BAHASA CINTA: Berdasarkan konsep 5 Bahasa Cinta (Waktu Berkualitas, Pujian/Afirmasi, Pelayanan, Hadiah, Sentuhan Fisik), prediksi Bahasa Cinta utama untuk SETIAP individu. Jelaskan alasan prediksimu berdasarkan hobi dan prioritas mereka. Berikan satu tips praktis untuk pasangannya.

    4.  IDE KENCAN: Sarankan satu ide kencan pertama yang sangat kreatif dan spesifik yang mencerminkan KISAH PERTEMUAN dan BAHASA CINTA yang telah kamu analisis. Jelaskan mengapa ide ini sempurna untuk mereka.
    
    """
    ai_response_text = generate_ai_content(main_prompt)

    if ai_response_text:
        parts = ai_response_text.split('|||')
        love_story = parts[0].replace("KISAH PERTEMUAN:", "").strip() if len(parts) > 0 else "Cerita tidak dapat dibuat."
        personality_analysis = parts[1].replace("ANALISIS KEPRIBADIAN:", "").strip() if len(parts) > 1 else "Analisis kepribadian tidak tersedia."
        love_language_analysis = parts[2].replace("ANALISIS BAHASA CINTA:", "").strip() if len(parts) > 2 else "Analisis bahasa cinta tidak tersedia."
        date_idea = parts[3].replace("IDE KENCAN:", "").strip() if len(parts) > 3 else "Ide kencan tidak tersedia."
    else:
        love_story, personality_analysis, love_language_analysis, date_idea = ("Cerita fallback...", "Analisis fallback...", "Analisis Bahasa Cinta fallback...", "Ide kencan fallback...")

    analysis_data = {
        'score': final_score, 'profile1': p1, 'profile2': p2,
        'love_story': love_story, 'personality_analysis': personality_analysis,
        'love_language_analysis': love_language_analysis, 'date_idea': date_idea,
        'breakdown': analysis_breakdown, 'priority_analysis': priority_analysis,
        'story_tone': story_tone
    }
    new_analysis = Analysis(
        profile1_name=p1['name'], profile2_name=p2['name'], score=final_score,
        love_story=love_story, date_idea=date_idea,
        raw_data=json.dumps(analysis_data), author=current_user
    )
    db.session.add(new_analysis)
    db.session.commit()
    return render_template('loading.html', analysis_id=new_analysis.id)


@main.route('/result/<int:analysis_id>')
@login_required
def view_result(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.author != current_user:
        flash('Anda tidak memiliki izin untuk melihat hasil analisis ini.', 'danger')
        return redirect(url_for('main.dashboard'))
    data = json.loads(analysis.raw_data)
    data['priority_analysis'] = json.dumps(data.get('priority_analysis', {}))
    return render_template('results_lanjutan.html', title='Hasil Analisis', analysis=analysis, **data)

@main.route('/regenerate/<string:content_type>/<int:analysis_id>', methods=['POST'])
@login_required
def regenerate_content(content_type, analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.author != current_user:
        return jsonify({'error': 'Unauthorized'}), 403

    data = json.loads(analysis.raw_data)
    profile1 = data.get('profile1')
    profile2 = data.get('profile2')
    story_tone = data.get('story_tone', 'Romantis Klasik')
    if content_type == 'story':
        prompt = f"Tulis ulang sebuah KISAH PERTEMUAN yang romantis (1-4 paragraf) dengan gaya '{story_tone}' untuk {profile1['name']} ({profile1['city']}) dan {profile2['name']} ({profile2['city']}). Gunakan hobi mereka ({', '.join(profile1['interests'])} dan {', '.join(profile2['interests'])}) sebagai inspirasi baru."
    elif content_type == 'date_idea':
        prompt = f"Sarankan sebuah IDE KENCAN pertama yang benar-benar baru dan kreatif untuk {profile1['name']} dan {profile2['name']}, berdasarkan hobi dan profil mereka. Berikan alasan singkat mengapa ide ini cocok."
    else:
        return jsonify({'error': 'Invalid content type'}), 400

    new_content_text = generate_ai_content(prompt)

    if new_content_text:
        return jsonify({'new_content': new_content_text.strip()})
    else:
        return jsonify({'error': 'Gagal menghasilkan konten baru.'}), 500

@main.route('/feedback', methods=['POST'])
@login_required
def submit_feedback():
    data = request.get_json()
    analysis_id = data.get('analysis_id')
    is_accurate = data.get('is_accurate')

    existing_feedback = Feedback.query.filter_by(user_id=current_user.id, analysis_id=analysis_id).first()
    if existing_feedback:
        return jsonify({'status': 'error', 'message': 'Anda sudah memberikan umpan balik untuk analisis ini.'}), 400

    new_feedback = Feedback(analysis_id=analysis_id, user_id=current_user.id, is_accurate=is_accurate)
    db.session.add(new_feedback)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Terima kasih atas umpan balik Anda!'})

@main.route('/share/<int:analysis_id>.png')
@login_required
def share_image(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    if analysis.author != current_user:
        return "Unauthorized", 403

    width, height = 1080, 1080
    bg_color = (252, 237, 244)
    img = Image.new('RGB', (width, height), color = bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font_bold = ImageFont.truetype("arialbd.ttf", 70)
        font_regular = ImageFont.truetype("arial.ttf", 40)
        font_italic = ImageFont.truetype("ariali.ttf", 35)
        font_small = ImageFont.truetype("arial.ttf", 25)
    except IOError:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()
        font_italic = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((width/2, 100), "Love Compatibility", font=font_regular, fill=(50,50,50), anchor="mt")
    names_text = f"{analysis.profile1_name} & {analysis.profile2_name}"
    draw.text((width/2, 180), names_text, font=font_bold, fill=(219, 39, 119), anchor="mt")
    draw.text((width/2, 400), f"{analysis.score}%", font=ImageFont.truetype("arialbd.ttf", 200), fill=(219, 39, 119), anchor="mm")
    draw.text((width/2, 520), "Match Score", font=font_regular, fill=(50,50,50), anchor="mt")
    story_wrapped = textwrap.wrap(f'"{analysis.love_story}"', width=50)
    y_text = 650
    for line in story_wrapped:
        draw.text((width/2, y_text), line, font=font_italic, fill=(100,100,100), anchor="mt")
        y_text += 45
    draw.text((width/2, height - 70), "Dianalisis oleh Love Compatibility Analyzer", font=font_small, fill=(150,150,150), anchor="mm")
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    response = make_response(img_io.getvalue())
    response.headers.set('Content-Type', 'image/png')
    return response
