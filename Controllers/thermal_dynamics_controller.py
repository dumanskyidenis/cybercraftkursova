from Domain.ViewModels.pc_viewmodels import ThermalAnalysisRequestViewModel, ThermalResultViewModel
from BusinessLogic.thermal_dynamics_service import ThermalDynamicsService

class ThermalDynamicsController:
    # === DEPENDENCY INJECTION ===
    def __init__(self, thermal_service: ThermalDynamicsService):
        self._thermal_service = thermal_service

    def estimate_thermal_throttling(self, request: ThermalAnalysisRequestViewModel) -> ThermalResultViewModel:
        """Аналізує, чи витримає обраний кулер процесор під навантаженням"""
        return self._thermal_service.estimate_thermal_throttling(request)

    def get_overclocking_headroom(self, cpu_id: int, motherboard_id: int) -> str:
        """Аналізує підсистему живлення (VRM) материнської плати"""
        return self._thermal_service.get_overclocking_headroom(cpu_id, motherboard_id)

    def suggest_airflow_optimization(self, case_id: int, total_system_tdp: int) -> str:
        """Надає поради щодо правильного розташування вентиляторів"""
        return self._thermal_service.suggest_airflow_optimization(case_id, total_system_tdp)