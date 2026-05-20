from flask import (Flask, render_template, jsonify, request,
                   session, redirect, url_for)
from datetime import datetime, date, timedelta
from functools import wraps
import os, hashlib, secrets

import firebase_admin
from firebase_admin import credentials, firestore as fb_firestore

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'geomix-secret-key-2024')

# autenticacao com fb bd
import json as _json

_fb_creds_env = os.environ.get('FIREBASE_CREDENTIALS')
if _fb_creds_env:
    cred = credentials.Certificate(_json.loads(_fb_creds_env))
    firebase_admin.initialize_app(cred)
elif os.path.exists('serviceAccountKey.json'):
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()

db = fb_firestore.client()

USERS_COL    = 'users'
PROGRESS_COL = 'progress'


# ajuste de data

def _to_date(val):
    if val is None:
        return None
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, str):
        return date.fromisoformat(val)
    if hasattr(val, 'date'):
        return val.date()
    return None


def _to_naive_dt(val):
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.replace(tzinfo=None) if val.tzinfo else val
    if hasattr(val, 'replace'):
        return val.replace(tzinfo=None)
    return None


# bd usuarios

def _doc_to_user(doc):
    if not doc.exists:
        return None
    data = doc.to_dict()
    data['id']                 = doc.id
    data['last_activity']      = _to_date(data.get('last_activity'))
    data['reset_token_expiry'] = _to_naive_dt(data.get('reset_token_expiry'))
    # Garante que created_at seja um datetime naive (sem timezone)
    # para que strftime() funcione normalmente nos templates.
    data['created_at']         = _to_naive_dt(data.get('created_at')) or datetime.utcnow()
    return data


def get_user_by_id(uid):
    doc = db.collection(USERS_COL).document(str(uid)).get()
    return _doc_to_user(doc)


def get_user_by_email(email):
    docs = (db.collection(USERS_COL)
              .where('email', '==', email)
              .limit(1)
              .stream())
    for doc in docs:
        return _doc_to_user(doc)
    return None


def create_user(name, email, password_hash):
    payload = {
        'name':               name,
        'email':              email,
        'password_hash':      password_hash,
        'xp':                 0,
        'streak':             0,
        'last_activity':      None,
        'reset_token':        None,
        'reset_token_expiry': None,
        'created_at':         datetime.utcnow(),
    }
    _, doc_ref = db.collection(USERS_COL).add(payload)
    payload['id'] = doc_ref.id
    return payload


def update_user(uid, updates):
    """Atualiza campos de um documento de usuario no Firestore."""
    db.collection(USERS_COL).document(str(uid)).update(updates)


def current_user():
    uid = session.get('user_id')
    return get_user_by_id(uid) if uid else None


# autenticar
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
        user = get_user_by_id(uid)
        if not user:
            session.clear()
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# bd de progresso

def _get_all_progress(user_id):
    """
    Busca todos os registros de progresso do usuario em uma unica chamada.
    Filtros por unit/activity sao feitos em Python para evitar indices
    compostos adicionais no Firestore.
    """
    docs = (db.collection(PROGRESS_COL)
              .where('user_id', '==', str(user_id))
              .stream())
    rows = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        at = d.get('answered_at')
        if at:
            d['answered_at'] = _to_naive_dt(at)
        rows.append(d)
    return rows


def _progress_exists(user_id, unit_id, activity_id, question_id):
    """Verifica se ja existe registro para essa questao especifica."""
    docs = (db.collection(PROGRESS_COL)
              .where('user_id',     '==', str(user_id))
              .where('unit_id',     '==', unit_id)
              .where('activity_id', '==', activity_id)
              .where('question_id', '==', question_id)
              .limit(1)
              .stream())
    for _ in docs:
        return True
    return False


def _add_progress(user_id, unit_id, activity_id, question_id, correct):
    db.collection(PROGRESS_COL).add({
        'user_id':     str(user_id),
        'unit_id':     unit_id,
        'activity_id': activity_id,
        'question_id': question_id,
        'correct':     correct,
        'answered_at': datetime.utcnow(),
    })


def _update_progress_to_correct(user_id, unit_id, activity_id, question_id):
    """Atualiza registro existente de errado → correto quando o aluno refaz e acerta."""
    docs = (db.collection(PROGRESS_COL)
              .where('user_id',     '==', str(user_id))
              .where('unit_id',     '==', unit_id)
              .where('activity_id', '==', activity_id)
              .where('question_id', '==', question_id)
              .limit(1)
              .stream())
    for doc in docs:
        if not doc.to_dict().get('correct'):
            doc.reference.update({'correct': True, 'answered_at': datetime.utcnow()})


# logica do progresso

def get_activity_progress(user_id, unit_id, activity_id, all_rows=None):
    if all_rows is None:
        all_rows = _get_all_progress(user_id)
    rows = [r for r in all_rows
            if r.get('unit_id') == unit_id and r.get('activity_id') == activity_id]
    return len(rows), sum(1 for r in rows if r.get('correct'))


def is_activity_complete(user_id, unit_id, activity_id, all_rows=None):
    total, _ = get_activity_progress(user_id, unit_id, activity_id, all_rows)
    return total >= 5


def is_unit_complete(user_id, unit_id, all_rows=None):
    return all(is_activity_complete(user_id, unit_id, a, all_rows) for a in range(1, 6))


def is_activity_unlocked(user_id, unit_id, activity_id, all_rows=None):
    if unit_id == 1 and activity_id == 1:
        return True
    if activity_id == 1:
        return is_unit_complete(user_id, unit_id - 1, all_rows)
    return is_activity_complete(user_id, unit_id, activity_id - 1, all_rows)


def build_progress_map(user_id):
    all_rows = _get_all_progress(user_id)
    result = {}
    for u in range(1, 6):
        for a in range(1, 6):
            total, correct = get_activity_progress(user_id, u, a, all_rows)
            result[f"{u}.{a}"] = {
                'total':    total,
                'correct':  correct,
                'complete': total >= 5,
                'unlocked': is_activity_unlocked(user_id, u, a, all_rows),
            }
    return result


def build_stats(user_id):
    from questions import UNITS_META
    all_rows   = _get_all_progress(user_id)
    total_ans  = len(all_rows)
    total_corr = sum(1 for r in all_rows if r.get('correct'))
    accuracy   = round(total_corr / total_ans * 100) if total_ans else 0

    units_stats = []
    for uid, umeta in UNITS_META.items():
        acts_done = sum(1 for a in range(1, 6)
                        if is_activity_complete(user_id, uid, a, all_rows))
        rows_u = [r for r in all_rows if r.get('unit_id') == uid]
        corr_u = sum(1 for r in rows_u if r.get('correct'))
        total_possible = 25   # 5 atividades × 5 questoes cada
        pct    = min(100, round(corr_u / total_possible * 100))
        units_stats.append({
            'id': uid, 'title': umeta['title'],
            'color': umeta['color'], 'acts_done': acts_done,
            'answered': len(rows_u), 'correct': corr_u, 'pct': pct,
        })

    today         = date.today()
    start_of_week = (today - timedelta(days=today.weekday() + 1)
                     if today.weekday() != 6 else today)
    day_names     = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab']
    active_set    = set()
    for r in all_rows:
        at = r.get('answered_at')
        if isinstance(at, datetime):
            active_set.add(at.date())
        elif isinstance(at, date):
            active_set.add(at)

    week_data = []
    for i in range(7):
        d = start_of_week + timedelta(days=i)
        week_data.append({
            'date':     d.isoformat(),
            'label':    day_names[i],
            'active':   d in active_set,
            'is_today': d == today,
        })

    return {
        'total_answered': total_ans,
        'total_correct':  total_corr,
        'accuracy':       accuracy,
        'units':          units_stats,
        'week_data':      week_data,
    }


# rotas

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
        name     = request.form.get('name',     '').strip()
        email    = request.form.get('email',    '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm',  '')

        if not name or not email or not password:
            error = 'Preencha todos os campos.'
        elif len(password) < 6:
            error = 'A senha deve ter pelo menos 6 caracteres.'
        elif password != confirm:
            error = 'As senhas nao coincidem.'
        elif get_user_by_email(email):
            error = 'Este e-mail ja esta cadastrado.'
        else:
            user = create_user(name, email, hash_pw(password))
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        email    = request.form.get('email',    '').strip().lower()
        password = request.form.get('password', '')
        user     = get_user_by_email(email)
        if not user or not verify_pw(password, user['password_hash']):
            error = 'E-mail ou senha incorretos.'
        else:
            session['user_id'] = user['id']
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
        user  = get_user_by_email(email)
        if not user:
            error = 'Nenhuma conta encontrada com este e-mail.'
        else:
            token = secrets.token_urlsafe(32)
            update_user(user['id'], {
                'reset_token':        token,
                'reset_token_expiry': datetime.utcnow() + timedelta(hours=1),
            })
            reset_link = url_for('reset_password', token=token, _external=True)
            message = reset_link
    return render_template('forgot_password.html', message=message, error=error)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    docs = (db.collection(USERS_COL)
              .where('reset_token', '==', token)
              .limit(1)
              .stream())
    user = None
    for doc in docs:
        user = _doc_to_user(doc)
        break

    error = None
    if not user or (user['reset_token_expiry'] and
                    user['reset_token_expiry'] < datetime.utcnow()):
        return render_template('reset_password.html', expired=True, error=None, token=None)

    if request.method == 'POST':
        pw      = request.form.get('password', '')
        confirm = request.form.get('confirm',  '')
        if len(pw) < 6:
            error = 'A senha deve ter pelo menos 6 caracteres.'
        elif pw != confirm:
            error = 'As senhas nao coincidem.'
        else:
            update_user(user['id'], {
                'password_hash':      hash_pw(pw),
                'reset_token':        None,
                'reset_token_expiry': None,
            })
            return redirect(url_for('login'))
    return render_template('reset_password.html', expired=False, token=token, error=error)


# rotas pros q fizeram login

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user()
    from questions import UNITS_META
    progress = build_progress_map(user['id'])
    return render_template('dashboard.html', user=user, units=UNITS_META, progress=progress)


@app.route('/intro/<int:unit_id>')
@login_required
def unit_intro(unit_id):
    user = current_user()
    from questions import UNITS_META
    if unit_id not in UNITS_META:
        return redirect(url_for('dashboard'))
    if not is_activity_unlocked(user['id'], unit_id, 1):
        return redirect(url_for('dashboard'))
    return render_template('intro.html', unit=UNITS_META[unit_id], unit_id=unit_id)


@app.route('/lesson/<int:unit_id>/<int:activity_id>')
@login_required
def lesson(unit_id, activity_id):
    user = current_user()
    from questions import UNITS_META
    if unit_id not in UNITS_META:
        return redirect(url_for('dashboard'))
    if not is_activity_unlocked(user['id'], unit_id, activity_id):
        return redirect(url_for('dashboard'))
    unit     = UNITS_META[unit_id]
    activity = unit['activities'][activity_id - 1]
    return render_template('lesson.html', user=user, unit=unit, unit_id=unit_id,
                           activity=activity, activity_id=activity_id)


@app.route('/formulas')
@login_required
def formulas():
    return render_template('formulas.html', user=current_user())


@app.route('/profile')
@login_required
def profile():
    user  = current_user()
    stats = build_stats(user['id'])
    return render_template('profile.html', user=user, stats=stats)


# ─────────────────────────────────────────
#  API
# ─────────────────────────────────────────

@app.route('/ranking')
@login_required
def ranking():
    user  = current_user()
    docs  = db.collection(USERS_COL).stream()
    users = []
    for doc in docs:
        u = _doc_to_user(doc)
        if u:
            users.append(u)
    users.sort(key=lambda u: u.get('xp', 0), reverse=True)
    my_rank = next((i + 1 for i, u in enumerate(users) if u['id'] == user['id']), None)
    return render_template('ranking.html', user=user, ranking=users[:20],
                           my_rank=my_rank, total_users=len(users))


@app.route('/api/questions/<int:unit_id>/<int:activity_id>')
@login_required
def api_questions(unit_id, activity_id):
    from questions import get_questions
    return jsonify(get_questions(unit_id, activity_id))


@app.route('/api/submit', methods=['POST'])
@login_required
def api_submit():
    user        = current_user()
    data        = request.json or {}
    unit_id     = data.get('unit_id')
    activity_id = data.get('activity_id')
    question_id = data.get('question_id')
    correct     = data.get('correct', False)
    xp_gain     = data.get('xp', 10)

    # Detecta revisao (questao ja respondida = atividade sendo refeita)
    already_answered = _progress_exists(user['id'], unit_id, activity_id, question_id)
    is_revision      = already_answered

    if not already_answered:
        # Primeira vez respondendo esta questao
        _add_progress(user['id'], unit_id, activity_id, question_id, correct)
    elif correct:
        # Ja respondeu antes: se acertou agora, atualiza registro para correct=True
        _update_progress_to_correct(user['id'], unit_id, activity_id, question_id)

    updates    = {}
    xp_awarded = 0

    if correct:
        # Revisao = metade do XP; primeira vez = XP completo
        xp_awarded = max(1, xp_gain // 2) if is_revision else xp_gain
        updates['xp'] = fb_firestore.Increment(xp_awarded)

    if updates:
        update_user(user['id'], updates)
        user = get_user_by_id(user['id'])

    return jsonify({
        'success':     True,
        'xp':          user['xp'],
        'streak':      user['streak'],
        'xp_awarded':  xp_awarded,
        'is_revision': is_revision,
    })


@app.route('/api/lesson/complete', methods=['POST'])
@login_required
def api_lesson_complete():
    """Chamado quando o aluno termina uma licao (nova ou revisao).
    Atualiza a ofensiva corretamente: +1 dia se for o primeiro login do dia,
    incrementa se foi ontem, ou reseta para 1 se passou mais de 1 dia."""
    user    = current_user()
    today   = date.today()
    today_dt = datetime(today.year, today.month, today.day)

    # Normaliza last_activity para date (Firestore devolve datetime)
    last = user.get('last_activity')
    if isinstance(last, datetime):
        last_date = last.date()
    elif isinstance(last, date):
        last_date = last
    else:
        last_date = None

    updates = {}
    if last_date != today:
        # Primeiro acesso do dia
        if last_date and (today - last_date).days == 1:
            # Ontem → mantém sequência
            updates['streak'] = fb_firestore.Increment(1)
        else:
            # Mais de 1 dia de intervalo ou nunca jogou → começa do 1
            updates['streak'] = 1
        updates['last_activity'] = today_dt
        update_user(user['id'], updates)
        user = get_user_by_id(user['id'])

    return jsonify({
        'success': True,
        'streak':  user['streak'],
    })


@login_required
def api_progress():
    user = current_user()
    return jsonify({
        'xp':      user['xp'],
        'streak':  user['streak'],
        'progress': build_progress_map(user['id']),
    })


@app.route('/api/profile/update', methods=['POST'])
@login_required
def api_profile_update():
    user    = current_user()
    data    = request.json or {}
    errors  = {}
    updates = {}

    new_name  = data.get('name',             '').strip()
    new_email = data.get('email',            '').strip().lower()
    new_pw    = data.get('password',         '').strip()
    cur_pw    = data.get('current_password', '').strip()

    if new_name:
        updates['name'] = new_name[:80]

    if new_email and new_email != user['email']:
        if get_user_by_email(new_email):
            errors['email'] = 'Este e-mail ja esta em uso.'
        else:
            updates['email'] = new_email

    if new_pw:
        if not verify_pw(cur_pw, user['password_hash']):
            errors['password'] = 'Senha atual incorreta.'
        elif len(new_pw) < 6:
            errors['password'] = 'Nova senha deve ter ao menos 6 caracteres.'
        else:
            updates['password_hash'] = hash_pw(new_pw)

    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    if updates:
        update_user(user['id'], updates)
        user = get_user_by_id(user['id'])

    return jsonify({'success': True, 'name': user['name'], 'email': user['email']})


# jinja2

@app.template_filter('strptime')
def strptime_filter(value, fmt):
    return datetime.strptime(value, fmt)


# porta pra rodar
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
