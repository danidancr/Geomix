from flask import (Flask, render_template, jsonify, request,
                   session, redirect, url_for, flash)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from functools import wraps
import os, hashlib, secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'geomix-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geomix.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─────────────────────────────────────────
#  MODELS
# ─────────────────────────────────────────

class User(db.Model):
    id                  = db.Column(db.Integer,  primary_key=True)
    name                = db.Column(db.String(80),  nullable=False, default='Estudante')
    email               = db.Column(db.String(120), unique=True, nullable=False)
    password_hash       = db.Column(db.String(256),  nullable=False)
    xp                  = db.Column(db.Integer,  default=0)
    streak              = db.Column(db.Integer,  default=0)
    last_activity       = db.Column(db.Date,     nullable=True)
    reset_token         = db.Column(db.String(64),  nullable=True)
    reset_token_expiry  = db.Column(db.DateTime,    nullable=True)
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)


class Progress(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    unit_id     = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    correct     = db.Column(db.Boolean, default=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)


# ─────────────────────────────────────────
#  AUTH HELPERS
# ─────────────────────────────────────────

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def verify_pw(pw, hashed):
    return hashlib.sha256(pw.encode()).hexdigest() == hashed

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        uid = session.get('user_id')

        if not uid:
            return redirect(url_for('login'))

        user = db.session.get(User, uid)

        if not user:
            session.clear()  # limpa sessão inválida
            return redirect(url_for('login'))

        return f(*args, **kwargs)
    return decorated

def current_user():
    uid = session.get('user_id')
    return db.session.get(User, uid) if uid else None

# ─────────────────────────────────────────
#  PROGRESS HELPERS
# ─────────────────────────────────────────

def get_activity_progress(user_id, unit_id, activity_id):
    rows = Progress.query.filter_by(
        user_id=user_id, unit_id=unit_id, activity_id=activity_id
    ).all()
    return len(rows), sum(1 for r in rows if r.correct)

def is_activity_complete(user_id, unit_id, activity_id):
    total, _ = get_activity_progress(user_id, unit_id, activity_id)
    return total >= 5

def is_unit_complete(user_id, unit_id):
    return all(is_activity_complete(user_id, unit_id, a) for a in range(1, 6))

def is_activity_unlocked(user_id, unit_id, activity_id):
    if unit_id == 1 and activity_id == 1:
        return True
    if activity_id == 1:
        return is_unit_complete(user_id, unit_id - 1)
    return is_activity_complete(user_id, unit_id, activity_id - 1)

def build_progress_map(user_id):
    result = {}
    for u in range(1, 6):
        for a in range(1, 6):
            total, correct = get_activity_progress(user_id, u, a)
            result[f"{u}.{a}"] = {
                'total':    total,
                'correct':  correct,
                'complete': total >= 5,
                'unlocked': is_activity_unlocked(user_id, u, a),
            }
    return result

def build_stats(user_id):
    from questions import UNITS_META
    all_rows   = Progress.query.filter_by(user_id=user_id).all()
    total_ans  = len(all_rows)
    total_corr = sum(1 for r in all_rows if r.correct)
    accuracy   = round(total_corr / total_ans * 100) if total_ans else 0

    units_stats = []
    for uid, umeta in UNITS_META.items():
        acts_done = sum(1 for a in range(1,6) if is_activity_complete(user_id, uid, a))
        rows_u    = [r for r in all_rows if r.unit_id == uid]
        corr_u    = sum(1 for r in rows_u if r.correct)
        pct       = round(acts_done / 5 * 100)
        units_stats.append({
            'id': uid, 'title': umeta['title'],
            'color': umeta['color'], 'acts_done': acts_done,
            'answered': len(rows_u), 'correct': corr_u, 'pct': pct,
        })

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday() + 1) if today.weekday() != 6 else today
    day_names = ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb']
    active_set = {r.answered_at.date() for r in all_rows}

    week_data = []

    for i in range(7):
        d = start_of_week + timedelta(days=i)
        week_data.append({
            'date': d.isoformat(),
            'label': day_names[i],
            'active': d in active_set,
            'is_today': d == today
        })

    return {
        'total_answered': total_ans,
        'total_correct':  total_corr,
        'accuracy':       accuracy,
        'units':          units_stats,
        'week_data': week_data
    }

# ─────────────────────────────────────────
#  PUBLIC ROUTES
# ─────────────────────────────────────────

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')
        if not name or not email or not password:
            error = 'Preencha todos os campos.'
        elif len(password) < 6:
            error = 'A senha deve ter pelo menos 6 caracteres.'
        elif password != confirm:
            error = 'As senhas não coincidem.'
        elif User.query.filter_by(email=email).first():
            error = 'Este e-mail já está cadastrado.'
        else:
            user = User(name=name, email=email, password_hash=hash_pw(password))
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user     = User.query.filter_by(email=email).first()
        if not user or not verify_pw(password, user.password_hash):
            error = 'E-mail ou senha incorretos.'
        else:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    message = None
    error   = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user  = User.query.filter_by(email=email).first()
        if not user:
            error = 'Nenhuma conta encontrada com este e-mail.'
        else:
            token = secrets.token_urlsafe(32)
            user.reset_token        = token
            user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            reset_link = url_for('reset_password', token=token, _external=True)
            message = reset_link
    return render_template('forgot_password.html', message=message, error=error)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user  = User.query.filter_by(reset_token=token).first()
    error = None
    if not user or (user.reset_token_expiry and user.reset_token_expiry < datetime.utcnow()):
        return render_template('reset_password.html', expired=True, error=None, token=None)
    if request.method == 'POST':
        pw      = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        if len(pw) < 6:
            error = 'A senha deve ter pelo menos 6 caracteres.'
        elif pw != confirm:
            error = 'As senhas não coincidem.'
        else:
            user.password_hash      = hash_pw(pw)
            user.reset_token        = None
            user.reset_token_expiry = None
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('reset_password.html', expired=False, token=token, error=error)

# ─────────────────────────────────────────
#  PROTECTED ROUTES
# ─────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user()

    if not user:
        return redirect(url_for('login'))

    from questions import UNITS_META

    progress = build_progress_map(user.id)

    return render_template(
        'dashboard.html',
        user=user,
        units=UNITS_META,
        progress=progress
    )


@app.route('/intro/<int:unit_id>')
@login_required
def unit_intro(unit_id):
    user = current_user()
    from questions import UNITS_META
    if unit_id not in UNITS_META:
        return redirect(url_for('dashboard'))
    if not is_activity_unlocked(user.id, unit_id, 1):
        return redirect(url_for('dashboard'))
    unit = UNITS_META[unit_id]
    return render_template('intro.html', unit=unit, unit_id=unit_id)


@app.route('/lesson/<int:unit_id>/<int:activity_id>')
@login_required
def lesson(unit_id, activity_id):
    user = current_user()
    from questions import UNITS_META
    if unit_id not in UNITS_META:
        return redirect(url_for('dashboard'))
    if not is_activity_unlocked(user.id, unit_id, activity_id):
        return redirect(url_for('dashboard'))
    unit     = UNITS_META[unit_id]
    activity = unit['activities'][activity_id - 1]
    return render_template('lesson.html', user=user, unit=unit, unit_id=unit_id,
                           activity=activity, activity_id=activity_id)


@app.route('/formulas')
@login_required
def formulas():
    user = current_user()
    return render_template('formulas.html', user=user)


@app.route('/profile')
@login_required
def profile():
    user  = current_user()
    stats = build_stats(user.id)
    return render_template('profile.html', user=user, stats=stats)


# ─────────────────────────────────────────
#  API
# ─────────────────────────────────────────

@app.route('/api/questions/<int:unit_id>/<int:activity_id>')
@login_required
def api_questions(unit_id, activity_id):
    from questions import get_questions
    return jsonify(get_questions(unit_id, activity_id))


@app.route('/api/submit', methods=['POST'])
@login_required
def api_submit():
    user = current_user()
    data = request.json or {}
    unit_id     = data.get('unit_id')
    activity_id = data.get('activity_id')
    question_id = data.get('question_id')
    correct     = data.get('correct', False)
    xp_gain     = data.get('xp', 10)

    existing = Progress.query.filter_by(
        user_id=user.id, unit_id=unit_id,
        activity_id=activity_id, question_id=question_id
    ).first()

    if not existing:
        db.session.add(Progress(
            user_id=user.id, unit_id=unit_id,
            activity_id=activity_id, question_id=question_id, correct=correct
        ))
        if correct:
            user.xp += xp_gain
        today = date.today()
        if user.last_activity != today:
            if user.last_activity and (today - user.last_activity).days == 1:
                user.streak += 1
            elif not user.last_activity or (today - user.last_activity).days > 1:
                user.streak = 1
            user.last_activity = today
        db.session.commit()

    return jsonify({'success': True, 'xp': user.xp, 'streak': user.streak})


@app.route('/api/progress')
@login_required
def api_progress():
    user = current_user()
    return jsonify({'xp': user.xp, 'streak': user.streak,
                    'progress': build_progress_map(user.id)})


@app.route('/api/profile/update', methods=['POST'])
@login_required
def api_profile_update():
    user   = current_user()
    data   = request.json or {}
    errors = {}

    new_name  = data.get('name', '').strip()
    new_email = data.get('email', '').strip().lower()
    new_pw    = data.get('password', '').strip()
    cur_pw    = data.get('current_password', '').strip()

    if new_name:
        user.name = new_name[:80]

    if new_email and new_email != user.email:
        if User.query.filter_by(email=new_email).first():
            errors['email'] = 'Este e-mail já está em uso.'
        else:
            user.email = new_email

    if new_pw:
        if not verify_pw(cur_pw, user.password_hash):
            errors['password'] = 'Senha atual incorreta.'
        elif len(new_pw) < 6:
            errors['password'] = 'Nova senha deve ter ao menos 6 caracteres.'
        else:
            user.password_hash = hash_pw(new_pw)

    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    db.session.commit()
    return jsonify({'success': True, 'name': user.name, 'email': user.email})


# ─────────────────────────────────────────
# Jinja2 custom filter
@app.template_filter('strptime')
def strptime_filter(value, fmt):
    return datetime.strptime(value, fmt)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
