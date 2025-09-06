from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Room(db.Model):
    """Модель кімнати (події)"""
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    room_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes_count = db.Column(db.Integer, default=0)
    
    # Відношення з коментарями та лайками
    comments = db.relationship('Comment', backref='room', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='room', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Room {self.room_name}>'

class Comment(db.Model):
    """Модель коментаря"""
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    player_name = db.Column(db.String(100), default='Анонім')
    team_name = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment by {self.player_name}>'

class Like(db.Model):
    """Модель лайків (для запобігання зловживанням)"""
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Унікальний індекс для запобігання множинним лайкам від однієї сесії
    __table_args__ = (db.UniqueConstraint('room_id', 'session_id', name='_room_session_uc'),)
    
    def __repr__(self):
        return f'<Like room_id={self.room_id}>'
