from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, PsuDetailViewModel
# 1. Імпортуємо репозиторій
from Repositories.hardware_repository import PsuRepository

class PsuService:
    """Клас бізнес-логіки для блоків живлення (використовує Репозиторій)"""

    # 2. Передаємо репозиторій через конструктор
    def __init__(self, psu_repository: PsuRepository):
        self.psu_repo = psu_repository

    def get_all_psus(self) -> List[ComponentShortViewModel]:
        # 3. Викликаємо базовий метод get_all
        psus_db = self.psu_repo.get_all()
        
        result = []
        for p in psus_db:
            full_name = f"{p.brand} {p.model} {p.watts}W"
            result.append(ComponentShortViewModel(id=p.id, name=full_name, price=p.price))
        return result

    def get_psu_details(self, psu_id: int) -> PsuDetailViewModel:
        # 4. Викликаємо базовий метод get_by_id
        psu_db = self.psu_repo.get_by_id(psu_id)
        
        if not psu_db:
            return None
            
        full_name = f"{psu_db.brand} {psu_db.model}"
        
        return PsuDetailViewModel(
            id=psu_db.id,
            name=full_name,
            wattage=psu_db.watts,
            efficiency_rating=getattr(psu_db, 'efficiency', "80+ Gold"), 
            modularity=getattr(psu_db, 'modular', "Full"),
            price=psu_db.price
        )

    def get_psus_by_min_wattage(self, min_wattage: int) -> List[PsuDetailViewModel]:
        # 5. Викликаємо наш кастомний метод з PsuRepository
        psus_db = self.psu_repo.get_by_min_wattage(min_wattage)
        
        result = []
        for psu_db in psus_db:
            full_name = f"{psu_db.brand} {psu_db.model}"
            result.append(PsuDetailViewModel(
                id=psu_db.id,
                name=full_name,
                wattage=psu_db.watts, 
                efficiency_rating=getattr(psu_db, 'efficiency', "80+ Gold"),
                modularity=getattr(psu_db, 'modular', "Full"),
                price=psu_db.price
            ))
        return result