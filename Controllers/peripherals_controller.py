from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel
from BusinessLogic.peripherals_service import PeripheralsService

class PeripheralsController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, peripherals_service: PeripheralsService):
        self._peripherals_service = peripherals_service

    def get_all_mice(self) -> List[ComponentShortViewModel]:
        """Отримати список ігрових та офісних мишок"""
        return self._peripherals_service.get_all_mice()

    def get_all_keyboards(self) -> List[ComponentShortViewModel]:
        """Отримати список клавіатур"""
        return self._peripherals_service.get_all_keyboards()

    def get_all_headsets(self) -> List[ComponentShortViewModel]:
        """Отримати список навушників та гарнітур"""
        return self._peripherals_service.get_all_headsets()