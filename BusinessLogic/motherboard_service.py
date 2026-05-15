from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel
# 1. Імпортуємо наш репозиторій
from Repositories.hardware_repository import MotherboardRepository

class MotherboardService:
    """Клас бізнес-логіки для материнських плат (використовує Репозиторій)"""

    # 2. Dependency Injection: передаємо репозиторій через конструктор
    def __init__(self, motherboard_repository: MotherboardRepository):
        self.mb_repo = motherboard_repository

    def get_all_motherboards(self) -> List[ComponentShortViewModel]:
        # 3. Викликаємо базовий метод
        mbs_db = self.mb_repo.get_all()
        
        result = []
        for m in mbs_db:
            full_name = f"{m.brand} {m.model}"
            result.append(ComponentShortViewModel(id=m.id, name=full_name, price=m.price))
        return result

    def get_motherboards_by_socket(self, socket_name: str) -> List[ComponentShortViewModel]:
        # 4. Викликаємо кастомний метод репозиторію
        mbs_db = self.mb_repo.get_by_socket(socket_name)
        
        result = []
        for m in mbs_db:
            full_name = f"{m.brand} {m.model}"
            result.append(ComponentShortViewModel(id=m.id, name=full_name, price=m.price))
        return result

    def get_motherboards_by_form_factor(self, form_factor: str) -> List[ComponentShortViewModel]:
        # 5. Викликаємо кастомний метод репозиторію
        mbs_db = self.mb_repo.get_by_form_factor(form_factor)
        
        result = []
        for m in mbs_db:
            full_name = f"{m.brand} {m.model}"
            result.append(ComponentShortViewModel(id=m.id, name=full_name, price=m.price))
        return result