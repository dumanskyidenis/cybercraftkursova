from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, StorageDetailViewModel
from BusinessLogic.storage_service import StorageService

class StorageController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, storage_service: StorageService):
        self._storage_service = storage_service

    def get_all_storage_devices(self) -> List[ComponentShortViewModel]:
        """Отримати список усіх жорстких дисків та SSD"""
        return self._storage_service.get_all_storage_devices()

    def get_storage_details(self, storage_id: int) -> StorageDetailViewModel:
        """Отримати деталі накопичувача"""
        return self._storage_service.get_storage_details(storage_id)

    def get_storage_by_type(self, storage_type: str) -> List[StorageDetailViewModel]:
        """Відфільтрувати накопичувачі за типом"""
        return self._storage_service.get_storage_by_type(storage_type)