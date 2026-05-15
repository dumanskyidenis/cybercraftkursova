from Domain.ViewModels.pc_viewmodels import GamePerformanceRequestViewModel, PerformanceScoreViewModel
from BusinessLogic.benchmark_service import BenchmarkService

class BenchmarkController:
    # --- DEPENDENCY INJECTION ---
    def __init__(self, benchmark_service: BenchmarkService):
        self._benchmark_service = benchmark_service

    def predict_game_fps(self, request: GamePerformanceRequestViewModel) -> PerformanceScoreViewModel:
        """Прогнозує середній FPS у конкретній грі"""
        return self._benchmark_service.predict_game_fps(request)

    def get_synthetic_score(self, build_id: int) -> PerformanceScoreViewModel:
        """Вираховує теоретичні бали збірки у синтетичних тестах"""
        return self._benchmark_service.get_synthetic_score(build_id)

    def calculate_bottleneck(self, cpu_id: int, gpu_id: int, resolution: str) -> str:
        """Точний математичний розрахунок 'пляшкового горлечка'"""
        return self._benchmark_service.calculate_bottleneck(cpu_id, gpu_id, resolution)