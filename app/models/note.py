from datetime import datetime, timezone
from ..extensions import db
from sqlalchemy import func, Column, Text, Computed
from sqlalchemy.dialects.postgresql import TSVECTOR


class Note(db.Model):

    __tablename__ = 'notes'
    __searchable__ = ['title', 'content', 'subject', 'teacher']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # TSVECTOR поле для полнотекстового поиска
    search_vector = db.Column(
        TSVECTOR,
        Computed(
            "to_tsvector('russian', coalesce(title, '') || ' ' || coalesce(content, '') || ' ' || coalesce(subject, '') || ' ' || coalesce(teacher, ''))",
            persisted=True
        )
    )

    @classmethod
    def fulltext_search(cls, query):
        """
        Полнотекстовый поиск с поддержкой русского языка
        """
        if not query:
            return cls.query

        if query.startswith('@'):
            try:
                note_id = int(query[1:])  # Убираем @ и преобразуем в число
                return cls.query.filter(cls.id == note_id)
            except ValueError:
                # Если после @ не число, ищем как обычный текст
                pass

        # Преобразуем запрос в tsquery
        ts_query = func.plainto_tsquery('russian', query)

        # Ищем и сортируем по релевантности
        return cls.query.filter(
            cls.search_vector.op('@@')(ts_query)
        ).order_by(
            func.ts_rank(cls.search_vector, ts_query).desc()
        )

    def __repr__(self):
        return f'<Note {self.title}>'
