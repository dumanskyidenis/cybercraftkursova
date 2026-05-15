from Repositories.base_repository import BaseRepository
from Domain.Models.user import User

class UserRepository(BaseRepository[User]):
    """Репозиторій для роботи з таблицею користувачів"""
    
    def __init__(self):
        super().__init__(User) # Передаємо модель у базовий клас

    # Додаємо унікальний метод, якого немає в базовому CRUD
    def get_by_email(self, email: str) -> User:
        """Отримати користувача за email (потрібно для логіну та реєстрації)"""
        return self.model.query.filter_by(email=email).first()