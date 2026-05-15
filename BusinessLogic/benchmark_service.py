from Domain.ViewModels.pc_viewmodels import GamePerformanceRequestViewModel, PerformanceScoreViewModel
# 1. Імпортуємо наші готові репозиторії
from Repositories.saved_build_repository import SavedBuildRepository
from Repositories.hardware_repository import CpuRepository, GpuRepository

class BenchmarkService:
    # 2. Передаємо репозиторії через конструктор
    def __init__(self, build_repo: SavedBuildRepository, cpu_repo: CpuRepository, gpu_repo: GpuRepository):
        self.build_repo = build_repo
        self.cpu_repo = cpu_repo
        self.gpu_repo = gpu_repo

    def predict_game_fps(self, request: GamePerformanceRequestViewModel) -> PerformanceScoreViewModel:
        # 3. Використовуємо репозиторії замість прямого доступу до БД
        build = self.build_repo.get_by_id(request.build_id)
        if not build or not build.cpu_id or not build.gpu_id:
            raise ValueError("Збірка не має процесора або відеокарти для тестування.")

        cpu = self.cpu_repo.get_by_id(build.cpu_id)
        gpu = self.gpu_repo.get_by_id(build.gpu_id)

        # РЕАЛЬНА МАТЕМАТИКА РОЗРАХУНКУ FPS
        base_fps_1080p = (gpu.gpu_mark / 20000) * 120 
        
        res_multiplier = {"1080p": 1.0, "1440p": 0.7, "4K": 0.45}.get(request.resolution, 1.0)
        preset_multiplier = {"Low": 1.5, "Medium": 1.2, "High": 1.0, "Ultra": 0.8}.get(request.graphics_preset, 1.0)

        final_fps = int(base_fps_1080p * res_multiplier * preset_multiplier)

        bottleneck = self._calculate_bottleneck_value(cpu.cpu_mark, gpu.gpu_mark)

        return PerformanceScoreViewModel(
            expected_fps=final_fps,
            cpu_score_synthetic=cpu.cpu_mark,
            gpu_score_synthetic=gpu.gpu_mark,
            bottleneck_percentage=bottleneck
        )

    def _calculate_bottleneck_value(self, cpu_mark: int, gpu_mark: int) -> float:
        ratio = gpu_mark / cpu_mark if cpu_mark > 0 else 0
        if ratio > 1.8: 
            return round(((ratio - 1.8) / ratio) * 100, 1)
        elif ratio < 0.8: 
            return round(((0.8 - ratio) / 0.8) * 100, 1)
        return 0.0 

    def calculate_bottleneck(self, cpu_id: int, gpu_id: int, resolution: str) -> str:
        # 4. Використовуємо репозиторії тут також
        cpu = self.cpu_repo.get_by_id(cpu_id)
        gpu = self.gpu_repo.get_by_id(gpu_id)
        
        if not cpu or not gpu:
            return "Недостатньо даних"

        percent = self._calculate_bottleneck_value(cpu.cpu_mark, gpu.gpu_mark)
        
        if percent == 0:
            return "0.0% (Відмінно збалансована збірка)"
        elif gpu.gpu_mark / cpu.cpu_mark > 1.8:
            return f"{percent}% (CPU Bottleneck - процесор не розкриває потенціал відеокарти)"
        else:
            return f"{percent}% (GPU Bottleneck - відеокарта є слабким місцем)"
        
    def analyze_custom_system(self, cpu_id: int, gpu_id: int, resolution: str, game_name: str) -> dict:
        cpu = self.cpu_repo.get_by_id(cpu_id)
        gpu = self.gpu_repo.get_by_id(gpu_id)

        if not cpu or not gpu:
            return {"error": "Недостатньо даних для аналізу."}

        # 1. РОЗРАХУНОК BOTTLENECK
        percent = self._calculate_bottleneck_value(cpu.cpu_mark, gpu.gpu_mark)
        desc = "Система ідеально збалансована! Жодних обмежень."
        if percent > 0:
            if gpu.gpu_mark / cpu.cpu_mark > 1.8:
                desc = "CPU Bottleneck - процесор не розкриває потенціал відеокарти"
            else:
                desc = "GPU Bottleneck - відеокарта є слабким місцем"

        # 2. РОЗРАХУНОК FPS
        # Множники оптимізації ігор (як у твоєму smart_configurator_service)
        multipliers = {
            "gta 6": 0.45, "alan wake 2": 0.50, "cyberpunk 2077": 0.60,
            "flight simulator": 0.65, "silent hill 2": 0.65, "starfield": 0.70,
            "hogwarts": 0.75, "the last of us": 0.75, "the last of us 2": 0.75, 
            "rdr 2": 0.85, "uncharted 4": 0.9, "the witcher 3": 1.1, 
            "warzone": 1.2, "pubg": 1.3, "fortnite": 1.5, "apex legends": 1.6, 
            "overwatch": 1.8, "world of tanks": 2.0, "minecraft": 2.5, 
            "cs 2": 2.8, "valorant": 3.0, "dota 2": 2.5, "league of legends": 3.5,
            "standard": 1.0
        }
        
        game_key = game_name.lower().strip()
        mult = multipliers.get(game_key, 1.0)

        # Базовий розрахунок для 1080p
        base_fps = (gpu.gpu_mark / 15000) * 90 * mult
        
        # Множник роздільної здатності
        res_multiplier = {"1080p": 1.0, "1440p": 0.65, "4K": 0.4}.get(resolution, 1.0)
        final_fps = base_fps * res_multiplier

        # Якщо є жорсткий ботлнек процесора, він "обрізає" максимальний FPS
        if gpu.gpu_mark / cpu.cpu_mark > 1.8:
            cpu_limit = (cpu.cpu_mark / 10000) * 80 * mult
            if final_fps > cpu_limit:
                final_fps = cpu_limit

        return {
            "bottleneck_percent": percent,
            "bottleneck_desc": desc,
            "fps": int(final_fps)
        }