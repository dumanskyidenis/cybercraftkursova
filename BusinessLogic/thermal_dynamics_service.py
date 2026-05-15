from Domain.ViewModels.pc_viewmodels import ThermalAnalysisRequestViewModel, ThermalResultViewModel

# 1. Імпортуємо наші готові репозиторії замість моделей БД
from Repositories.hardware_repository import CpuRepository, CoolerRepository, CaseRepository, MotherboardRepository

class ThermalDynamicsService:
    # 2. Передаємо всі 4 репозиторії через конструктор
    def __init__(self, cpu_repo: CpuRepository, cooler_repo: CoolerRepository, case_repo: CaseRepository, mb_repo: MotherboardRepository):
        self.cpu_repo = cpu_repo
        self.cooler_repo = cooler_repo
        self.case_repo = case_repo
        self.mb_repo = mb_repo

    def estimate_thermal_throttling(self, request: ThermalAnalysisRequestViewModel) -> ThermalResultViewModel:
        # 3. Використовуємо репозиторії замість query.get
        cpu = self.cpu_repo.get_by_id(request.cpu_id)
        cooler = self.cooler_repo.get_by_id(request.cooler_id)
        
        if not cpu or not cooler:
            return ThermalResultViewModel(estimated_load_temp_c=0, will_throttle=False, suggested_case_fans=0)

        cooler_capacity = cooler.max_tdp_dissipation if hasattr(cooler, 'max_tdp_dissipation') and cooler.max_tdp_dissipation else 150
        cpu_tdp = cpu.tdp if hasattr(cpu, 'tdp') and cpu.tdp else 65
        
        tdp_ratio = cpu_tdp / cooler_capacity
        
        base_temp = request.ambient_temp_c + (60 * tdp_ratio)
        estimated_temp = int(base_temp)
        
        will_throttle = estimated_temp >= 90
        
        suggested_fans = 0
        if estimated_temp > 80:
            suggested_fans = 3
        elif estimated_temp > 70:
            suggested_fans = 1

        return ThermalResultViewModel(
            estimated_load_temp_c=estimated_temp,
            will_throttle=will_throttle,
            suggested_case_fans=suggested_fans
        )

    def get_overclocking_headroom(self, cpu_id: int, motherboard_id: int) -> str:
        cpu = self.cpu_repo.get_by_id(cpu_id)
        mb = self.mb_repo.get_by_id(motherboard_id)
        
        if not cpu or not mb:
            return "Деталі не знайдено для аналізу VRM."

        cpu_tdp = cpu.tdp if hasattr(cpu, 'tdp') else 65

        if cpu_tdp > 105 and mb.price < 4000:
            return f"Обережно: процесор має високий TDP ({cpu_tdp}W). Плата {mb.brand} відноситься до бюджетного сегменту. Екстремальний розгін не рекомендується через ризик перегріву VRM."
        elif cpu_tdp <= 65 and mb.price > 5000:
            return f"Відмінний потенціал: плата {mb.brand} має потужну підсистему живлення, а процесор холодний. Можна безпечно експериментувати з розгоном."
        else:
            return "Середній потенціал: збірка збалансована. Допустимий легкий розгін, але обов'язково слідкуйте за температурами в стрес-тестах."

    def suggest_airflow_optimization(self, case_id: int, total_system_tdp: int) -> str:
        case = self.case_repo.get_by_id(case_id)
        case_name = f"{case.brand} {case.model}" if case else "цього корпусу"
        
        if total_system_tdp < 150:
            return f"Для {case_name} з TDP {total_system_tdp}W достатньо одного вентилятора на видув ззаду."
        elif total_system_tdp <= 300:
            return f"Система генерує {total_system_tdp}W тепла. Рекомендуємо класичну схему: 2 вентилятори на вдув (спереду) та 1 на видув (ззаду)."
        else:
            return f"Увага: гаряча збірка ({total_system_tdp}W)! Необхідний максимальний продув: 3 вентилятори на вдув і мінімум 2 на видув. Розгляньте рідинне охолодження."