from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel
# Імпортуємо обидва репозиторії
from Repositories.hardware_repository import RamRepository, MotherboardRepository

class RamService:
    """Клас бізнес-логіки для оперативної пам'яті (використовує Репозиторії)"""

    # 1. Dependency Injection: передаємо репозиторій RAM та Материнок
    def __init__(self, ram_repository: RamRepository, motherboard_repository: MotherboardRepository):
        self.ram_repo = ram_repository
        self.mb_repo = motherboard_repository

    def get_all_ram(self) -> List[ComponentShortViewModel]:
        rams_db = self.ram_repo.get_all()
        
        result = []
        for r in rams_db:
            full_name = f"{r.brand} {r.model} {r.cap}GB {r.r_type}"
            result.append(ComponentShortViewModel(id=r.id, name=full_name, price=r.price))
        return result

    def get_compatible_ram(self, motherboard_id: int) -> List[ComponentShortViewModel]:
        # 2. Звертаємось до репозиторію материнок
        mb = self.mb_repo.get_by_id(motherboard_id)
        if not mb:
            return []
            
        # 3. Передаємо тип пам'яті знайденої материнки в репозиторій оперативки
        rams_db = self.ram_repo.get_by_type(mb.memory_type)
        
        result = []
        for r in rams_db:
            full_name = f"{r.brand} {r.model} {r.cap}GB {r.r_type}"
            result.append(ComponentShortViewModel(id=r.id, name=full_name, price=r.price))
        return result
    
    def get_ram_by_capacity(self, min_gb: int) -> List[ComponentShortViewModel]:
        # 4. Використовуємо специфічний метод репозиторію
        rams_db = self.ram_repo.get_by_capacity(min_gb)
        
        result = []
        for r in rams_db:
            full_name = f"{r.brand} {r.model} {r.cap}GB {r.r_type}"
            result.append(ComponentShortViewModel(id=r.id, name=full_name, price=r.price))
        return result