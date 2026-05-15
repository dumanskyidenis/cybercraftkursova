from typing import List
from Domain.ViewModels.pc_viewmodels import CpuDetailViewModel, ComponentShortViewModel, FilterRequestViewModel
from BusinessLogic.cpu_service import CpuService

class CpuController:
    # ========================================================
    # ОСЬ ЦЕЙ МЕТОД ОБОВ'ЯЗКОВИЙ (він "приймає" сервіс з app.py)
    # ========================================================
    def __init__(self, cpu_service: CpuService):
        self._cpu_service = cpu_service

    def get_all_cpus(self) -> List[ComponentShortViewModel]:
        return self._cpu_service.get_all_cpus()

    def get_cpu_details(self, cpu_id: int) -> CpuDetailViewModel:
        return self._cpu_service.get_cpu_details(cpu_id)

    def filter_cpus(self, filters: FilterRequestViewModel) -> List[CpuDetailViewModel]:
        return self._cpu_service.filter_cpus(filters)