from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, PsuDetailViewModel
from BusinessLogic.psu_service import PsuService

class PsuController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, psu_service: PsuService):
        self._psu_service = psu_service

    def get_all_psus(self) -> List[ComponentShortViewModel]:
        """Отримати загальний список усіх блоків живлення"""
        return self._psu_service.get_all_psus()

    def get_psu_details(self, psu_id: int) -> PsuDetailViewModel:
        """Отримати всі характеристики конкретного блоку живлення"""
        return self._psu_service.get_psu_details(psu_id)

    def get_psus_by_min_wattage(self, min_wattage: int) -> List[PsuDetailViewModel]:
        """Фільтр: показує тільки ті блоки живлення, які потягнуть збірку"""
        return self._psu_service.get_psus_by_min_wattage(min_wattage)