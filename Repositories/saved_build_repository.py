from typing import List
from Repositories.base_repository import BaseRepository
from Domain.Models.saved_build import SavedBuild

class SavedBuildRepository(BaseRepository[SavedBuild]):
    """Репозиторій для роботи зі збереженими збірками"""
    
    def __init__(self):
        super().__init__(SavedBuild)

    # Унікальний метод для профілю
    def get_by_user_id(self, user_id: int) -> List[SavedBuild]:
        """Отримати всі збірки конкретного користувача"""
        return self.model.query.filter_by(user_id=user_id).all()