from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, CoolerDetailViewModel
# 1. Імпортуємо репозиторій
from Repositories.hardware_repository import CoolerRepository

class CoolingService:
    """Клас бізнес-логіки для систем охолодження (використовує Репозиторій)"""

    # 2. Передаємо репозиторій через конструктор
    def __init__(self, cooler_repository: CoolerRepository):
        self.cooler_repo = cooler_repository

    def get_all_coolers(self) -> List[ComponentShortViewModel]:
        # 3. Викликаємо базовий метод get_all
        coolers_db = self.cooler_repo.get_all()
        
        result = []
        for c in coolers_db:
            full_name = f"{c.brand} {c.model}"
            result.append(ComponentShortViewModel(id=c.id, name=full_name, price=c.price))
        return result

    def get_coolers_by_socket(self, socket_name: str) -> List[ComponentShortViewModel]:
        # 4. Викликаємо кастомний метод з CoolerRepository
        coolers_db = self.cooler_repo.get_by_socket(socket_name)
        
        result = []
        for c in coolers_db:
            full_name = f"{c.brand} {c.model}"
            result.append(ComponentShortViewModel(id=c.id, name=full_name, price=c.price))
        return result

    def get_coolers_by_tdp(self, cpu_tdp: int) -> List[CoolerDetailViewModel]:
        # 5. Викликаємо кастомний метод з CoolerRepository
        coolers_db = self.cooler_repo.get_by_min_tdp(cpu_tdp)
        
        result = []
        for c in coolers_db:
            full_name = f"{c.brand} {c.model}"
            result.append(CoolerDetailViewModel(
                id=c.id,
                name=full_name,
                cooler_type=c.c_type,
                max_tdp_dissipation=c.tdp,
                price=c.price
            ))
        return result