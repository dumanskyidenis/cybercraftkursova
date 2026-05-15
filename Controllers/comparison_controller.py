from typing import List
from Domain.ViewModels.pc_viewmodels import BuildCheckRequestViewModel, BuildComparisonViewModel
from BusinessLogic.comparison_service import ComparisonService

class ComparisonController:
    # === DEPENDENCY INJECTION ===
    def __init__(self, comparison_service: ComparisonService):
        self._comparison_service = comparison_service

    def compare_two_builds(self, build_1: BuildCheckRequestViewModel, build_2: BuildCheckRequestViewModel) -> BuildComparisonViewModel:
        """Порівнює дві готові конфігурації ПК"""
        return self._comparison_service.compare_two_builds(build_1, build_2)

    def compare_cpu_gpu_balance(self, cpu_id: int, gpu_id: int) -> str:
        """Швидке порівняння класів CPU та GPU на загальний баланс збірки"""
        return self._comparison_service.compare_cpu_gpu_balance(cpu_id, gpu_id)

    def compare_components(self, component_type: str, item_id_1: int, item_id_2: int) -> List[str]:
        """Порівнює дві конкретні деталі"""
        return self._comparison_service.compare_components(component_type, item_id_1, item_id_2)