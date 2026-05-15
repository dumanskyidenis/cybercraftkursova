from Domain.ViewModels.pc_viewmodels import AutoBuildRequestViewModel, FullBuildViewModel, PurposeBuildRequestViewModel
from BusinessLogic.smart_configurator_service import SmartConfiguratorService

class SmartConfiguratorController:
    # === DEPENDENCY INJECTION ===
    def __init__(self, smart_service: SmartConfiguratorService):
        self._smart_service = smart_service

    def get_best_build_by_budget(self, request: AutoBuildRequestViewModel) -> FullBuildViewModel:
        """Знаходить найкращу збірку ціна-якість під вказаний бюджет"""
        return self._smart_service.get_best_build_by_budget(request)

    def get_build_for_game(self, request: PurposeBuildRequestViewModel) -> FullBuildViewModel:
        """Підбирає мінімально необхідну збірку для комфортної гри"""
        return self._smart_service.get_build_for_game(request)

    def upgrade_suggestion(self, current_budget: float, cpu_id: int, gpu_id: int) -> str:
        """Аналізує поточний ПК і радить, що краще оновити"""
        return self._smart_service.upgrade_suggestion(current_budget, cpu_id, gpu_id)