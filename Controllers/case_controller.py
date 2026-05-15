from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, CaseDetailViewModel
from BusinessLogic.case_service import CaseService

class CaseController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, case_service: CaseService):
        self._case_service = case_service

    def get_all_cases(self) -> List[ComponentShortViewModel]:
        """Отримати список усіх корпусів"""
        return self._case_service.get_all_cases()

    def get_case_details(self, case_id: int) -> CaseDetailViewModel:
        """Отримати детальні розміри корпусу (макс. довжина GPU, висота кулера)"""
        return self._case_service.get_case_details(case_id)

    def check_case_clearance(self, case_id: int, gpu_length: int, cooler_height: int) -> bool:
        """Перевіряє сумісність розмірів комплектуючих з корпусом"""
        return self._case_service.check_case_clearance(case_id, gpu_length, cooler_height)