from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, CaseDetailViewModel
# 1. Імпортуємо репозиторій
from Repositories.hardware_repository import CaseRepository

class CaseService:
    """Клас бізнес-логіки для корпусів"""

    # 2. Передаємо репозиторій через конструктор
    def __init__(self, case_repository: CaseRepository):
        self.case_repo = case_repository

    def get_all_cases(self) -> List[ComponentShortViewModel]:
        # 3. Базовий метод get_all
        cases_db = self.case_repo.get_all()
        
        result = []
        for c in cases_db:
            full_name = f"{c.brand} {c.model}"
            result.append(ComponentShortViewModel(id=c.id, name=full_name, price=c.price))
        return result

    def get_case_details(self, case_id: int) -> CaseDetailViewModel:
        # 4. Базовий метод get_by_id
        case_db = self.case_repo.get_by_id(case_id)
        
        if not case_db:
            return None
            
        full_name = f"{case_db.brand} {case_db.model}"
        return CaseDetailViewModel(
            id=case_db.id,
            full_name=full_name,
            form_factor=case_db.form,
            max_gpu_length=case_db.gpu_m,
            max_cooler_height=case_db.cool_m,
            price=case_db.price
        )

    def check_case_clearance(self, case_id: int, gpu_length: int, cooler_height: int) -> bool:
        """Повертає True, якщо комплектуючі помістяться, і False, якщо ні"""
        # 5. Базовий метод get_by_id
        case_db = self.case_repo.get_by_id(case_id)
        
        if not case_db:
            return False
            
        # Бізнес-логіка залишається недоторканою в сервісі
        is_gpu_ok = gpu_length <= case_db.gpu_m
        is_cooler_ok = cooler_height <= case_db.cool_m
        
        return is_gpu_ok and is_cooler_ok