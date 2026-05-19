from Domain.ViewModels.pc_viewmodels import (
    AutoBuildRequestViewModel, 
    FullBuildViewModel, 
    PurposeBuildRequestViewModel, 
    ComponentShortViewModel
)

# 1. Імпортуємо всі потрібні репозиторії замість моделей БД
from Repositories.hardware_repository import (
    CpuRepository, GpuRepository, MotherboardRepository, 
    RamRepository, StorageRepository, PsuRepository, CaseRepository, CoolerRepository
)

class SmartConfiguratorService:
    def __init__(self, cpu_repo: CpuRepository, gpu_repo: GpuRepository, 
                 mb_repo: MotherboardRepository, ram_repo: RamRepository, 
                 storage_repo: StorageRepository, psu_repo: PsuRepository, 
                 case_repo: CaseRepository, cooler_repo: CoolerRepository):
        self.cpu_repo = cpu_repo
        self.gpu_repo = gpu_repo
        self.mb_repo = mb_repo
        self.ram_repo = ram_repo
        self.storage_repo = storage_repo
        self.psu_repo = psu_repo
        self.case_repo = case_repo
        self.cooler_repo = cooler_repo

    def _get_best_compatible(self, repo, max_price: float, condition=None):
        items = repo.get_all()
        valid_items = [i for i in items if i.price <= max_price]
        if condition: valid_items = [i for i in valid_items if condition(i)]
        if not valid_items:
            valid_items = [i for i in items if (condition(i) if condition else True)]
            if not valid_items: return None
            valid_items.sort(key=lambda x: x.price)
            return valid_items[0]
        valid_items.sort(key=lambda x: x.price, reverse=True)
        return valid_items[0]

    def _to_vm(self, db_item):
        if not db_item: return ComponentShortViewModel(id=0, name="Не знайдено", price=0)
        return ComponentShortViewModel(id=db_item.id, name=f"{getattr(db_item, 'brand', '')} {getattr(db_item, 'model', '')}".strip(), price=db_item.price)

    def _build_compatible_system(self, budgets: dict) -> FullBuildViewModel:
        cpu_db = self._get_best_compatible(self.cpu_repo, budgets.get('cpu', 0))
        mb_cond = lambda m: getattr(m, 'socket', '') == getattr(cpu_db, 'socket', '') if cpu_db else True
        mb_db = self._get_best_compatible(self.mb_repo, budgets.get('mb', 0), mb_cond)
        
        ram_cond = lambda r: getattr(r, 'r_type', getattr(r, 'type', '')) == getattr(mb_db, 'memory_type', '') if mb_db else True
        ram_db = self._get_best_compatible(self.ram_repo, budgets.get('ram', 0), ram_cond)
        
        cooler_cond = lambda c: (getattr(cpu_db, 'socket', '') in getattr(c, 'socket', '')) if cpu_db else True
        cooler_db = self._get_best_compatible(self.cooler_repo, budgets.get('cooler', 0), cooler_cond)
        
        gpu_db = self._get_best_compatible(self.gpu_repo, budgets.get('gpu', 0))
        
        total_tdp = 50 + (getattr(cpu_db, 'tdp', 65) if cpu_db else 0) + (getattr(gpu_db, 'tdp', 200) if gpu_db else 0)
        psu_cond = lambda p: getattr(p, 'wattage', getattr(p, 'watts', 0)) >= int(total_tdp * 1.2)
        psu_db = self._get_best_compatible(self.psu_repo, budgets.get('psu', 0), psu_cond)
        
        st_db = self._get_best_compatible(self.storage_repo, budgets.get('storage', 0))
        all_cases = self.case_repo.get_all()
        case_db = all_cases[0] if all_cases else None

        result = FullBuildViewModel(
            cpu=self._to_vm(cpu_db), 
            motherboard=self._to_vm(mb_db), 
            gpu=self._to_vm(gpu_db), 
            ram=self._to_vm(ram_db), 
            storage=self._to_vm(st_db), 
            psu=self._to_vm(psu_db), 
            case=self._to_vm(case_db),
            cooler=self._to_vm(cooler_db),  # <--- ТЕПЕР КУЛЕР ТУТ!
            total_price=sum([c.price for c in [self._to_vm(cpu_db), self._to_vm(gpu_db), self._to_vm(mb_db), self._to_vm(ram_db), self._to_vm(st_db), self._to_vm(psu_db), self._to_vm(case_db), self._to_vm(cooler_db)]]),
            performance_score=0
        )
        return result

    def get_best_build_by_budget(self, request: AutoBuildRequestViewModel) -> FullBuildViewModel:
        b = request.target_budget
        budgets = {
            'cpu': b * 0.22, 'cooler': b * 0.05, 'gpu': b * 0.38, 
            'mb': b * 0.10, 'ram': b * 0.08, 'storage': b * 0.08, 'psu': b * 0.07, 'case': b * 0.02
        }
        res = self._build_compatible_system(budgets)
        res.performance_score = int(res.total_price * 0.15)
        return res

    def get_build_for_game(self, request: PurposeBuildRequestViewModel) -> FullBuildViewModel:
        # 1. Базові ціни для збірки рівня 1080p, Medium, Стандартна гра
        base_cpu = 5000
        base_gpu = 9000
        base_mb = 3000
        base_ram = 1500
        base_storage = 2000
        base_psu = 2000

        # 2. Множник РОЗДІЛЬНОЇ ЗДАТНОСТІ (Resolution)
        res = request.resolution.lower()
        res_mult_gpu = 1.0
        res_mult_cpu = 1.0
        if "1440" in res or "2k" in res:
            res_mult_gpu = 1.6  # 2K дуже навантажує відеокарту
            res_mult_cpu = 1.2
        elif "4k" in res or "2160" in res:
            res_mult_gpu = 2.5  # 4K вимагає топову відеокарту
            res_mult_cpu = 1.5
            base_ram += 1500    # Для 4K треба більше пам'яті
            base_psu += 1500    # І потужніший блок живлення

        # 3. Множник НАЛАШТУВАНЬ ГРАФІКИ (Performance Level)
        perf = request.performance_level.lower()
        perf_mult = 1.0
        if "low" in perf or "minimum" in perf:
            perf_mult = 0.7     # Економія для низьких налаштувань
        elif "high" in perf or "recommended" in perf:
            perf_mult = 1.3     # Запас потужності
            base_storage += 1000 # Сучасні ігри важать багато
        elif "ultra" in perf or "max" in perf:
            perf_mult = 1.7
            base_mb += 2000     # Краща плата для топового заліза
            base_ram += 2000

        # 4. ІНДИВІДУАЛЬНІ МНОЖНИКИ ВАЖКОСТІ (Розширений список)
        software_key = request.specific_software.lower().strip()
        
        multipliers = {
            # --- ГЕЙМІНГ ---
            "gta 6": 1.65,             # Максимальний запас на майбутнє
            "alan wake 2": 1.60,
            "cyberpunk 2077": 1.55,
            "flight simulator": 1.50,
            "silent hill 2": 1.45,
            "starfield": 1.40,
            "hogwarts": 1.35,
            "the last of us": 1.35,
            "the last of us 2": 1.35,
            "rdr 2": 1.35,
            "uncharted 4": 1.25,
            "the witcher 3": 1.15,
            "warzone": 1.10,
            "pubg": 1.05,
            "fortnite": 0.95,
            "apex legends": 0.90,
            "overwatch": 0.85,
            "world of tanks": 0.80,
            "minecraft": 0.75,
            "cs 2": 0.70,
            "valorant": 0.60,
            "dota 2": 0.60,
            "league of legends": 0.50,
            
            # --- ВІДЕОМОНТАЖ ---
            "after effects": 1.50,     # Дуже важка для RAM та CPU
            "davinci": 1.45,           # Дуже залежить від потужного GPU
            "premiere": 1.35,
            "vegas": 1.25,
            
            # --- 3D ТА РЕНДЕР ---
            "unreal engine 5": 1.60,   # Потребує топового заліза
            "maya": 1.50,
            "cinema 4d": 1.45,
            "blender": 1.45,
            "autocad": 1.15,           # AutoCAD більше любить високі частоти CPU
            
            # --- ОФІС / РОБОТА / ДИЗАЙН ---
            "photoshop": 1.00,         # Потребує RAM для великих проектів
            "programming": 0.85,       # Важливий CPU для компіляції та RAM
            "figma": 0.60,             # Легкий векторний редактор
            "office": 0.40             # Базова офісна система
        }

        # Отримуємо множник (якщо не знайдено - 1.0 за замовчуванням)
        game_mult = multipliers.get(software_key, 1.0)
            
        # 5. ДЕТАЛЬНА КОРЕКЦІЯ ПІД ПРОФЕСІЙНІ ЦІЛІ (Primary Use)
        use = request.primary_use.lower()
        
        # Сценарій: ВІДЕОМОНТАЖ (Video Editing)
        if "edit" in use or "монтаж" in use:
            base_cpu *= 1.8      # Процесор - це серце монтажу (кількість ядер)
            base_ram *= 2.5      # Монтажу потрібно мінімум 32-64 ГБ RAM
            base_storage *= 2.0  # Відеофайли займають дуже багато місця
            base_gpu *= 0.7      # Відеокарта важлива, але не так критично, як для ігор
            
        # Сценарій: 3D МОДЕЛЮВАННЯ ТА РЕНДЕР (3D Design / Rendering)
        elif "3d" in use or "render" in use or "modeling" in use:
            base_gpu *= 1.8      # Для 3D рендеру (Cycles, Octane) потрібен потужний GPU з великою VRAM
            base_cpu *= 1.4      # Процесор важливий для симуляцій
            base_ram *= 2.0      # Велика кількість полігонів потребує багато пам'яті
            base_psu += 1500     # Потужні відеокарти потребують більше живлення
            
        # Сценарій: ОФІС / НАВЧАННЯ (Office / Study)
        elif "office" in use or "work" in use:
            base_cpu *= 0.8
            base_gpu = 3000      # Мінімальна "затичка" або вбудована графіка
            base_ram = 1500
            base_storage = 1500
            base_psu = 1200

        # 6. ФІНАЛЬНИЙ РОЗРАХУНОК БЮДЖЕТУ ДЛЯ КОЖНОЇ ДЕТАЛІ
        budgets = {
            'cpu': base_cpu * res_mult_cpu * perf_mult * game_mult,
            'cooler': 1500 * perf_mult,
            'gpu': base_gpu * res_mult_gpu * perf_mult * game_mult,
            'mb': base_mb * perf_mult,
            'ram': base_ram * perf_mult,
            'storage': base_storage * perf_mult,
            'psu': base_psu * perf_mult * res_mult_gpu,
            'case': 2000 * perf_mult
        }

        # 7. ЗБИРАЄМО СУМІСНУ СИСТЕМУ
        result = self._build_compatible_system(budgets)
        
        score = int(result.total_price * 0.15)
        if "work" in use:
            score = int((result.cpu.price * 2 + result.gpu.price) * 0.2)
        result.performance_score = score

        return result

    def upgrade_suggestion(self, current_budget: float, cpu_id: int, gpu_id: int) -> str:
        if current_budget >= 15000:
            return "Бюджет дозволяє оновити відеокарту. Перевірте сумісність нового GPU з вашим блоком живлення."
        elif current_budget >= 5000:
            return "За ці гроші можна оновити процесор. Переконайтеся, що материнська плата підтримує новий сокет."
        else:
            return "Оптимальний вибір за ці гроші — додати оперативної пам'яті або швидкий M.2 накопичувач."