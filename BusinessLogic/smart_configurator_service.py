from Domain.ViewModels.pc_viewmodels import (
    AutoBuildRequestViewModel, 
    FullBuildViewModel, 
    PurposeBuildRequestViewModel, 
    ComponentShortViewModel
)

# 1. Імпортуємо всі потрібні репозиторії замість моделей БД
from Repositories.hardware_repository import (
    CpuRepository, GpuRepository, MotherboardRepository, 
    RamRepository, StorageRepository, PsuRepository, CaseRepository
)

class SmartConfiguratorService:
    """Сервіс для інтелектуального підбору комплектуючих (використовує Репозиторії)"""

    # 2. Передаємо репозиторії через конструктор
    def __init__(self, cpu_repo: CpuRepository, gpu_repo: GpuRepository, 
                 mb_repo: MotherboardRepository, ram_repo: RamRepository, 
                 storage_repo: StorageRepository, psu_repo: PsuRepository, 
                 case_repo: CaseRepository):
        self.cpu_repo = cpu_repo
        self.gpu_repo = gpu_repo
        self.mb_repo = mb_repo
        self.ram_repo = ram_repo
        self.storage_repo = storage_repo
        self.psu_repo = psu_repo
        self.case_repo = case_repo

    def _get_best_component(self, repo, max_price: float):
        """Допоміжний метод: тепер приймає об'єкт репозиторію, а не клас моделі"""
        # 3. Викликаємо наш новий універсальний метод з BaseRepository
        item = repo.get_best_under_price(max_price)
        
        if not item:
            return ComponentShortViewModel(id=0, name="Немає в наявності", price=0)
            
        return ComponentShortViewModel(id=item.id, name=f"{item.brand} {item.model}", price=item.price)

    def get_best_build_by_budget(self, request: AutoBuildRequestViewModel) -> FullBuildViewModel:
        budget = request.target_budget

        cpu_budget = budget * 0.25
        gpu_budget = budget * 0.40
        mb_budget = budget * 0.10
        ram_budget = budget * 0.10
        storage_budget = budget * 0.08
        psu_budget = budget * 0.07

        # 4. Передаємо репозиторії в допоміжний метод
        cpu_model = self._get_best_component(self.cpu_repo, cpu_budget)
        gpu_model = self._get_best_component(self.gpu_repo, gpu_budget)
        mb_model = self._get_best_component(self.mb_repo, mb_budget)
        ram_model = self._get_best_component(self.ram_repo, ram_budget)
        st_model = self._get_best_component(self.storage_repo, storage_budget)
        psu_model = self._get_best_component(self.psu_repo, psu_budget)
        
        # Беремо перший корпус через репозиторій
        all_cases = self.case_repo.get_all()
        case_db = all_cases[0] if all_cases else None
        case_model = ComponentShortViewModel(
            id=case_db.id if case_db else 0, 
            name=f"{case_db.brand} {case_db.model}" if case_db else "Немає в БД", 
            price=case_db.price if case_db else 0
        )

        real_total_price = sum([
            cpu_model.price, gpu_model.price, mb_model.price, 
            ram_model.price, st_model.price, psu_model.price, case_model.price
        ])

        return FullBuildViewModel(
            cpu=cpu_model, motherboard=mb_model, gpu=gpu_model, 
            ram=ram_model, storage=st_model, psu=psu_model, case=case_model,
            total_price=real_total_price,
            performance_score=int(real_total_price * 0.15)
        )

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

        # 6. ФІНАЛЬНИЙ РОЗРАХУНОК ЦІЛЬОВОГО БЮДЖЕТУ ДЛЯ КОЖНОЇ ДЕТАЛІ
        target_cpu_price = base_cpu * res_mult_cpu * perf_mult * game_mult
        target_gpu_price = base_gpu * res_mult_gpu * perf_mult * game_mult
        target_mb_price = base_mb * perf_mult
        target_ram_price = base_ram * perf_mult
        target_storage_price = base_storage * perf_mult
        target_psu_price = base_psu * perf_mult * res_mult_gpu

        # 7. ЗВЕРНЕННЯ ДО РЕПОЗИТОРІЇВ ЗА ДЕТАЛЯМИ
        cpu_model = self._get_best_component(self.cpu_repo, target_cpu_price)
        gpu_model = self._get_best_component(self.gpu_repo, target_gpu_price)
        mb_model = self._get_best_component(self.mb_repo, target_mb_price)
        ram_model = self._get_best_component(self.ram_repo, target_ram_price)
        st_model = self._get_best_component(self.storage_repo, target_storage_price)
        psu_model = self._get_best_component(self.psu_repo, target_psu_price)
        
        # Беремо перший корпус через репозиторій
        all_cases = self.case_repo.get_all()
        case_db = all_cases[0] if all_cases else None
        case_model = ComponentShortViewModel(
            id=case_db.id if case_db else 0, 
            name=f"{case_db.brand} {case_db.model}" if case_db else "Standard Case", 
            price=case_db.price if case_db else 0
        )

        real_total = sum([c.price for c in [cpu_model, gpu_model, mb_model, ram_model, st_model, psu_model, case_model]])

        # Визначаємо бали продуктивності (для ігор більше важить GPU, для роботи CPU)
        score = int(real_total * 0.15)
        if "work" in use:
            score = int((cpu_model.price * 2 + gpu_model.price) * 0.2)

        return FullBuildViewModel(
            cpu=cpu_model, motherboard=mb_model, gpu=gpu_model, 
            ram=ram_model, storage=st_model, psu=psu_model, case=case_model,
            total_price=real_total,
            performance_score=score
        )

    def upgrade_suggestion(self, current_budget: float, cpu_id: int, gpu_id: int) -> str:
        if current_budget >= 15000:
            return "Бюджет дозволяє оновити відеокарту. Перевірте сумісність нового GPU з вашим блоком живлення."
        elif current_budget >= 5000:
            return "За ці гроші можна оновити процесор. Переконайтеся, що материнська плата підтримує новий сокет."
        else:
            return "Оптимальний вибір за ці гроші — додати оперативної пам'яті або швидкий M.2 накопичувач."