from typing import List
from Domain.ViewModels.pc_viewmodels import GpuDetailViewModel, ComponentShortViewModel

# Імпортуємо наш сервіс
from BusinessLogic.gpu_service import GpuService

class GpuController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, gpu_service: GpuService):
        self._gpu_service = gpu_service

    def get_all_gpus(self) -> List[ComponentShortViewModel]:
        """Отримати короткий список усіх відеокарт"""
        return self._gpu_service.get_all_gpus()

    def get_gpu_details(self, gpu_id: int) -> GpuDetailViewModel:
        """Отримати всі характеристики однієї відеокарти за ID"""
        return self._gpu_service.get_gpu_details(gpu_id)

    def get_gpus_by_psu_limit(self, max_wattage: int) -> List[GpuDetailViewModel]:
        """Знайти відеокарти, які потягне блок живлення клієнта"""
        return self._gpu_service.get_gpus_by_psu_limit(max_wattage)