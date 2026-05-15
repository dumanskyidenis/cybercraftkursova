from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel
from BusinessLogic.ram_service import RamService

class MemoryController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, ram_service: RamService):
        self._ram_service = ram_service

    def get_all_ram(self) -> List[ComponentShortViewModel]:
        """Отримати всю оперативну пам'ять"""
        return self._ram_service.get_all_ram()

    def get_compatible_ram(self, motherboard_id: int) -> List[ComponentShortViewModel]:
        """Отримати плашки RAM, які підходять до обраної материнки"""
        return self._ram_service.get_compatible_ram(motherboard_id)
    
    def get_ram_by_capacity(self, min_gb: int) -> List[ComponentShortViewModel]:
        """Фільтр: знайти комплекти пам'яті потрібного об'єму"""
        return self._ram_service.get_ram_by_capacity(min_gb)