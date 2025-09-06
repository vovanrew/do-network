from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import uuid
import os
from .models import db, Room, Comment, Like

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ініціалізація бази даних
db.init_app(app)

# Створення таблиць
with app.app_context():
    db.create_all()

# Функція для форматування часу
def format_time_ago(time):
    """Форматує час у вигляді 'X часів тому'"""
    now = datetime.utcnow()
    diff = now - time
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} {'рік' if years == 1 else 'роки' if years < 5 else 'років'} тому"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} {'місяць' if months == 1 else 'місяці' if months < 5 else 'місяців'} тому"
    elif diff.days > 0:
        return f"{diff.days} {'день' if diff.days == 1 else 'дні' if diff.days < 5 else 'днів'} тому"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} {'годину' if hours == 1 else 'години' if hours < 5 else 'годин'} тому"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} {'хвилину' if minutes == 1 else 'хвилини' if minutes < 5 else 'хвилин'} тому"
    else:
        return "щойно"

# Реєстрація функції як фільтру для шаблонів
app.jinja_env.filters['time_ago'] = format_time_ago

# Middleware для генерації session_id
@app.before_request
def before_request():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session.permanent = True

@app.route('/')
def index():
    """Головна сторінка зі списком кімнат"""
    rooms = Room.query.order_by(Room.created_at.desc()).all()
    return render_template('index.html', rooms=rooms)

@app.route('/create', methods=['GET', 'POST'])
def create_room():
    """Створення нової кімнати"""
    if request.method == 'POST':
        team_name = request.form.get('team_name', '').strip()
        room_name = request.form.get('room_name', '').strip()
        content = request.form.get('content', '').strip()
        
        # Валідація
        errors = []
        if not team_name:
            errors.append('Назва команди є обов\'язковою')
        if not room_name:
            errors.append('Назва кімнати є обов\'язковою')
        if not content:
            errors.append('Опис є обов\'язковим')
        
        # Перевірка довжини
        if len(room_name) > 100:
            errors.append('Назва кімнати не може бути довшою за 100 символів')
        if len(team_name) > 100:
            errors.append('Назва команди не може бути довшою за 100 символів')
        if len(content) > 1000:
            errors.append('Опис не може бути довшим за 1000 символів')
        
        if errors:
            return render_template('create.html', errors=errors, 
                                   team_name=team_name, room_name=room_name, content=content)
        
        # Створення нової кімнати
        new_room = Room(
            team_name=team_name,
            room_name=room_name,
            content=content
        )
        db.session.add(new_room)
        db.session.commit()
        
        return redirect(url_for('room_detail', room_id=new_room.id))
    
    return render_template('create.html')

@app.route('/room/<int:room_id>')
def room_detail(room_id):
    """Детальна сторінка кімнати"""
    room = Room.query.get_or_404(room_id)
    comments = Comment.query.filter_by(room_id=room_id).order_by(Comment.created_at.desc()).all()
    
    # Перевірка, чи користувач вже лайкав цю кімнату
    user_liked = False
    if 'session_id' in session:
        like = Like.query.filter_by(room_id=room_id, session_id=session['session_id']).first()
        user_liked = like is not None
    
    return render_template('room.html', room=room, comments=comments, user_liked=user_liked)

@app.route('/room/<int:room_id>/like', methods=['POST'])
def like_room(room_id):
    """AJAX endpoint для лайку кімнати"""
    room = Room.query.get_or_404(room_id)
    
    if 'session_id' not in session:
        return jsonify({'error': 'Session not found'}), 400
    
    # Перевірка, чи користувач вже лайкав
    existing_like = Like.query.filter_by(room_id=room_id, session_id=session['session_id']).first()
    
    if existing_like:
        # Видалення лайку
        db.session.delete(existing_like)
        room.likes_count = max(0, room.likes_count - 1)
        liked = False
    else:
        # Додавання лайку
        new_like = Like(room_id=room_id, session_id=session['session_id'])
        db.session.add(new_like)
        room.likes_count += 1
        liked = True
    
    db.session.commit()
    
    return jsonify({
        'likes_count': room.likes_count,
        'liked': liked
    })

@app.route('/room/<int:room_id>/comment', methods=['POST'])
def add_comment(room_id):
    """Додавання коментаря"""
    room = Room.query.get_or_404(room_id)
    
    player_name = request.form.get('player_name', '').strip() or 'Анонім'
    team_name = request.form.get('team_name', '').strip() or None
    content = request.form.get('content', '').strip()
    
    # Валідація
    if not content:
        return redirect(url_for('room_detail', room_id=room_id))
    
    if len(content) > 500:
        return redirect(url_for('room_detail', room_id=room_id))
    
    # Створення коментаря
    new_comment = Comment(
        room_id=room_id,
        player_name=player_name,
        team_name=team_name,
        content=content
    )
    db.session.add(new_comment)
    db.session.commit()
    
    return redirect(url_for('room_detail', room_id=room_id) + '#comments')

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
