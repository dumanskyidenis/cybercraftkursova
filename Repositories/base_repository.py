from database import db
from typing import List, TypeVar, Generic

# T означає "будь-який клас моделі" (наприклад, User, CPU, SavedBuild)
T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Універсальний репозиторій для базових CRUD-операцій з базою даних"""
    
    def __init__(self, model: T):
        self.model = model

    def get_all(self) -> List[T]:
        """Отримати всі записи з таблиці (SELECT)"""
        return self.model.query.all()

    def get_by_id(self, item_id: int) -> T:
        """Отримати один запис за його ID (SELECT)"""
        return self.model.query.get(item_id)

    def add(self, item: T) -> T:
        """Додати новий запис (INSERT)"""
        db.session.add(item)
        db.session.commit()
        return item

    def update(self) -> None:
        """Зберегти зміни в записах (UPDATE)"""
        db.session.commit()

    def delete(self, item: T) -> None:
        """Видалити запис (DELETE)"""
        db.session.delete(item)
        db.session.commit()
        
    def get_best_under_price(self, max_price: float) -> T:
        """Шукає найдорожчу деталь, яка вписується в бюджет, або найдешевшу загалом"""
        item = self.model.query.filter(self.model.price <= max_price).order_by(self.model.price.desc()).first()
        
        if not item:
            item = self.model.query.order_by(self.model.price.asc()).first()
            
        return item