from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel

# Імпортуємо наш сервіс
from BusinessLogic.motherboard_service import MotherboardService

class MotherboardController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, motherboard_service: MotherboardService):
        self._mb_service = motherboard_service

    def get_all_motherboards(self) -> List[ComponentShortViewModel]:
        """Отримати всі материнські плати"""
        return self._mb_service.get_all_motherboards()

    def get_motherboards_by_socket(self, socket_name: str) -> List[ComponentShortViewModel]:
        """Отримати материнки тільки під конкретний сокет (напр. 'AM4')"""
        return self._mb_service.get_motherboards_by_socket(socket_name)

    def get_motherboards_by_form_factor(self, form_factor: str) -> List[ComponentShortViewModel]:
        """Отримати плати за розміром (ATX, Micro-ATX)"""
        return self._mb_service.get_motherboards_by_form_factor(form_factor)