from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, CoolerDetailViewModel
from BusinessLogic.cooling_service import CoolingService

class CoolingController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, cooling_service: CoolingService):
        self._cooling_service = cooling_service

    def get_all_coolers(self) -> List[ComponentShortViewModel]:
        """Отримати список усього охолодження"""
        return self._cooling_service.get_all_coolers()

    def get_coolers_by_socket(self, socket_name: str) -> List[ComponentShortViewModel]:
        """Відфільтрувати кулери за сокетом материнки"""
        return self._cooling_service.get_coolers_by_socket(socket_name)

    def get_coolers_by_tdp(self, cpu_tdp: int) -> List[CoolerDetailViewModel]:
        """Розумний фільтр: показує тільки ті кулери, які здатні охолодити обраний процесор"""
        return self._cooling_service.get_coolers_by_tdp(cpu_tdp)