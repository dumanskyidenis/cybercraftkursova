from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, StorageDetailViewModel
# 1. Імпортуємо репозиторій
from Repositories.hardware_repository import StorageRepository

class StorageService:
    """Клас бізнес-логіки для накопичувачів (використовує Репозиторій)"""

    # 2. Передаємо репозиторій через конструктор
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repo = storage_repository

    def get_all_storage_devices(self) -> List[ComponentShortViewModel]:
        # 3. Викликаємо базовий метод get_all
        storages_db = self.storage_repo.get_all()
        
        result = []
        for s in storages_db:
            full_name = f"{s.brand} {s.model} {s.cap}GB"
            result.append(ComponentShortViewModel(id=s.id, name=full_name, price=s.price))
        return result

    def get_storage_details(self, storage_id: int) -> StorageDetailViewModel:
        # 4. Викликаємо базовий метод get_by_id
        s_db = self.storage_repo.get_by_id(storage_id)
        
        if not s_db:
            return None
            
        full_name = f"{s_db.brand} {s_db.model}"
        
        return StorageDetailViewModel(
            id=s_db.id,
            name=full_name,
            storage_type=s_db.s_type,
            capacity_gb=s_db.cap,
            read_speed_mbps=getattr(s_db, 'read_speed', None),
            price=s_db.price
        )

    def get_storage_by_type(self, storage_type: str) -> List[StorageDetailViewModel]:
        # 5. Викликаємо наш кастомний метод з StorageRepository
        storages_db = self.storage_repo.get_by_type(storage_type)
        
        result = []
        for s_db in storages_db:
            full_name = f"{s_db.brand} {s_db.model}"
            result.append(StorageDetailViewModel(
                id=s_db.id,
                name=full_name,
                storage_type=s_db.s_type,
                capacity_gb=s_db.cap,
                read_speed_mbps=getattr(s_db, 'read_speed', None),
                price=s_db.price
            ))
        return result