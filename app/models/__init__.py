# Принудительно импортируем все модели
from .role import Role
from .user import User
from .note import Note

# Явно указываем какие модели должны быть доступны
__all__ = ['Role', 'User', 'Note']