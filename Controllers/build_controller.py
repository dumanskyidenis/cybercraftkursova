from Domain.ViewModels.pc_viewmodels import BuildCheckRequestViewModel, CompatibilityResultViewModel
from BusinessLogic.build_service import BuildService

class BuildController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, build_service: BuildService):
        self._build_service = build_service

    def validate_build_compatibility(self, build_data: BuildCheckRequestViewModel) -> CompatibilityResultViewModel:
        """Перевірка сумісності всієї збірки"""
        return self._build_service.validate_build_compatibility(build_data)

    def calculate_build_power(self, build_data: BuildCheckRequestViewModel) -> int:
        """Споживання енергії"""
        return self._build_service.calculate_build_power(build_data)

    def generate_build_summary_txt(self, build_data: BuildCheckRequestViewModel) -> str:
        """Генерація текстового чека"""
        return self._build_service.generate_build_summary_txt(build_data)