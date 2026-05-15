from typing import List
from Domain.ViewModels.pc_viewmodels import BuildCheckRequestViewModel, BuildComparisonViewModel

# 1. Імпортуємо ВСІ репозиторії
from Repositories.hardware_repository import (
    CpuRepository, GpuRepository, MotherboardRepository, RamRepository, PsuRepository,
    StorageRepository, CoolerRepository, CaseRepository
)

class ComparisonService:
    # 2. Dependency Injection (Тепер тут є всі 8 репозиторіїв)
    def __init__(self, cpu_repo: CpuRepository, gpu_repo: GpuRepository, 
                 mb_repo: MotherboardRepository, ram_repo: RamRepository, 
                 psu_repo: PsuRepository, storage_repo: StorageRepository,
                 cooler_repo: CoolerRepository, case_repo: CaseRepository):
        self.cpu_repo = cpu_repo
        self.gpu_repo = gpu_repo
        self.mb_repo = mb_repo
        self.ram_repo = ram_repo
        self.psu_repo = psu_repo
        self.storage_repo = storage_repo
        self.cooler_repo = cooler_repo
        self.case_repo = case_repo

    def _evaluate_build_score_and_price(self, build: BuildCheckRequestViewModel):
        cpu = self.cpu_repo.get_by_id(build.cpu_id)
        gpu = self.gpu_repo.get_by_id(build.gpu_id) if build.gpu_id else None
        mb = self.mb_repo.get_by_id(build.motherboard_id)
        ram = self.ram_repo.get_by_id(build.ram_id)
        psu = self.psu_repo.get_by_id(build.psu_id)

        total_price = sum(item.price for item in [cpu, gpu, mb, ram, psu] if item)
        
        cpu_score = cpu.cpu_mark if cpu and hasattr(cpu, 'cpu_mark') else 0
        gpu_score = gpu.gpu_mark if gpu and hasattr(gpu, 'gpu_mark') else 0
        score = cpu_score + gpu_score
        
        return total_price, score

    def compare_two_builds(self, build_1: BuildCheckRequestViewModel, build_2: BuildCheckRequestViewModel) -> dict:
        price1, score1 = self._evaluate_build_score_and_price(build_1)
        price2, score2 = self._evaluate_build_score_and_price(build_2)

        # Словник для збереження аналізу кожного компонента
        detailed_analysis = {}
        
        # Список всіх категорій для порівняння
        component_map = {
            'cpu': (build_1.cpu_id, build_2.cpu_id, "Процесор"),
            'gpu': (build_1.gpu_id, build_2.gpu_id, "Відеокарта"),
            'motherboard': (build_1.motherboard_id, build_2.motherboard_id, "Материнська плата"),
            'ram': (build_1.ram_id, build_2.ram_id, "Пам'ять"),
            'psu': (build_1.psu_id, build_2.psu_id, "Блок живлення"),
            'storage': (getattr(build_1, 'storage_id', None), getattr(build_2, 'storage_id', None), "Накопичувач"),
            'cooler': (getattr(build_1, 'cooler_id', None), getattr(build_2, 'cooler_id', None), "Охолодження"),
            'case': (getattr(build_1, 'case_id', None), getattr(build_2, 'case_id', None), "Корпус")
        }

        for key, (id1, id2, label) in component_map.items():
            if id1 and id2:
                # Використовуємо твій існуючий метод порівняння компонентів
                advantages = self.compare_components(key, id1, id2)
                detailed_analysis[label] = advantages
            elif id1 or id2:
                detailed_analysis[label] = ["Один з компонентів не обрано для порівняння."]

        price_diff = abs(price1 - price2)
        winner = 1 if score1 > score2 else 2
        
        if score1 == score2:
            explanation = "Обидві збірки мають однакову продуктивність за бенчмарками."
        else:
            cheaper_text = f" Вона також є дешевшою на {price_diff} грн!" if (winner == 1 and price1 < price2) or (winner == 2 and price2 < price1) else f" Проте вона дорожча на {price_diff} грн."
            explanation = f"Збірка №{winner} перемагає за загальною потужністю.{cheaper_text}"

        return {
            "build_1_score": score1,
            "build_2_score": score2,
            "price_difference": price_diff,
            "winner_build": winner,
            "explanation_text": explanation,
            "detailed_analysis": detailed_analysis
        }

    def compare_cpu_gpu_balance(self, cpu_id: int, gpu_id: int) -> str:
        cpu = self.cpu_repo.get_by_id(cpu_id)
        gpu = self.gpu_repo.get_by_id(gpu_id)
        
        if not cpu or not gpu:
            return "Не знайдено процесор або відеокарту для аналізу."

        price_ratio = gpu.price / cpu.price if cpu.price > 0 else 0

        if price_ratio > 3.5:
            return f"Увага: Процесор {cpu.brand} занадто слабкий для потужної {gpu.brand}. Виникне 'bottleneck' (пляшкове горлечко) з боку процесора."
        elif price_ratio < 0.8:
            return f"Увага: Відеокарта {gpu.brand} занадто слабка для такого потужного {cpu.brand}. Для ігор краще взяти дешевший процесор і дорожчу відеокарту."
        else:
            return f"Відмінний баланс! Ці деталі чудово доповнюють одна одну."

    # === ОСЬ ТУТ НОВА СУПЕР-ЛОГІКА ПОРІВНЯННЯ ВСІХ ДЕТАЛЕЙ ===
    def compare_components(self, component_type: str, item_id_1: int, item_id_2: int) -> List[str]:
        advantages = []
        
        # 1. Знаходимо потрібний репозиторій
        repo_map = {
            'cpu': self.cpu_repo, 'gpu': self.gpu_repo, 'motherboard': self.mb_repo,
            'ram': self.ram_repo, 'psu': self.psu_repo, 'storage': self.storage_repo,
            'cooler': self.cooler_repo, 'case': self.case_repo
        }
        
        repo = repo_map.get(component_type.lower())
        if not repo: return ["Категорію деталей не знайдено."]
            
        item1 = repo.get_by_id(item_id_1)
        item2 = repo.get_by_id(item_id_2)
        if not item1 or not item2: return ["Одну з деталей не знайдено в БД."]
            
        # 2. Допоміжні функції
        def get_name(item):
            if hasattr(item, 'name') and item.name: return item.name
            return f"{getattr(item, 'brand', '')} {getattr(item, 'model', '')}".strip() or "Деталь"
            
        # Безпечне отримання атрибутів (на випадок якщо в БД назва колонки відрізняється)
        def get_val(item, *keys):
            for k in keys:
                if hasattr(item, k) and getattr(item, k) is not None: 
                    return getattr(item, k)
            return 0

        name1 = f"<strong style='color: var(--accent-cyan);'>{get_name(item1)}</strong>"
        name2 = f"<strong style='color: var(--accent-cyan);'>{get_name(item2)}</strong>"
        
        # 3. Порівняння ЦІНИ (працює для всіх)
        if item1.price < item2.price:
            advantages.append(f"{name1} вигідніший (дешевший на {item2.price - item1.price} ₴).")
        elif item2.price < item1.price:
            advantages.append(f"{name2} вигідніший (дешевший на {item1.price - item2.price} ₴).")

        # 4. СПЕЦИФІЧНІ ПОРІВНЯННЯ ДЛЯ КОЖНОГО КЛАСУ
        ctype = component_type.lower()

        if ctype == 'cpu':
            cores1, cores2 = get_val(item1, 'cores', 'core_count'), get_val(item2, 'cores', 'core_count')
            if cores1 > cores2: advantages.append(f"{name1} має більше ядер ({cores1} проти {cores2}). Краще для робочих завдань та монтажу.")
            elif cores2 > cores1: advantages.append(f"{name2} має більше ядер ({cores2} проти {cores1}). Краще для робочих завдань та монтажу.")
            
            clock1, clock2 = get_val(item1, 'base_clock_ghz', 'base_clock'), get_val(item2, 'base_clock_ghz', 'base_clock')
            if clock1 > clock2: advantages.append(f"{name1} має вищу базову частоту ({clock1} ГГц проти {clock2} ГГц).")
            elif clock2 > clock1: advantages.append(f"{name2} має вищу базову частоту ({clock2} ГГц проти {clock1} ГГц).")

        elif ctype == 'gpu':
            vram1, vram2 = get_val(item1, 'vram_gb', 'vram'), get_val(item2, 'vram_gb', 'vram')
            if vram1 > vram2: advantages.append(f"{name1} має більше відеопам'яті ({vram1} ГБ проти {vram2} ГБ). Це важливо для важких ігор у 2K/4K.")
            elif vram2 > vram1: advantages.append(f"{name2} має більше відеопам'яті ({vram2} ГБ проти {vram1} ГБ). Це важливо для важких ігор у 2K/4K.")

        elif ctype == 'ram':
            cap1, cap2 = get_val(item1, 'capacity', 'cap'), get_val(item2, 'capacity', 'cap')
            if cap1 > cap2: advantages.append(f"{name1} має більший об'єм пам'яті ({cap1} ГБ проти {cap2} ГБ).")
            elif cap2 > cap1: advantages.append(f"{name2} має більший об'єм пам'яті ({cap2} ГБ проти {cap1} ГБ).")

        elif ctype == 'storage':
            cap1, cap2 = get_val(item1, 'capacity', 'cap'), get_val(item2, 'capacity', 'cap')
            if cap1 > cap2: advantages.append(f"{name1} більш місткий ({cap1} ГБ проти {cap2} ГБ). Ви зможете встановити більше ігор.")
            elif cap2 > cap1: advantages.append(f"{name2} більш місткий ({cap2} ГБ проти {cap1} ГБ). Ви зможете встановити більше ігор.")

        elif ctype == 'psu':
            watt1, watt2 = get_val(item1, 'wattage'), get_val(item2, 'wattage')
            if watt1 > watt2: advantages.append(f"{name1} потужніший ({watt1} Вт проти {watt2} Вт). Це дасть кращий запас для майбутнього апгрейду.")
            elif watt2 > watt1: advantages.append(f"{name2} потужніший ({watt2} Вт проти {watt1} Вт). Це дасть кращий запас для майбутнього апгрейду.")

        elif ctype == 'motherboard':
            # 1. Порівняння покоління пам'яті (DDR5 vs DDR4)
            mem1 = str(get_val(item1, 'memory_type', 'r_type')).upper()
            mem2 = str(get_val(item2, 'memory_type', 'r_type')).upper()
            
            if 'DDR5' in mem1 and 'DDR4' in mem2:
                advantages.append(f"{name1} підтримує сучасний стандарт пам'яті DDR5. Це забезпечить набагато більшу швидкість роботи системи порівняно з DDR4.")
            elif 'DDR5' in mem2 and 'DDR4' in mem1:
                advantages.append(f"{name2} підтримує сучасний стандарт пам'яті DDR5. Це забезпечить набагато більшу швидкість роботи системи порівняно з DDR4.")
                
            # 2. Порівняння кількості слотів під ОЗУ
            slots1, slots2 = get_val(item1, 'slots', 'ram_slots'), get_val(item2, 'slots', 'ram_slots')
            if slots1 > slots2: 
                advantages.append(f"{name1} має більше слотів під оперативну пам'ять ({slots1} проти {slots2}). Це дає чудові можливості для майбутнього апгрейду.")
            elif slots2 > slots1: 
                advantages.append(f"{name2} має більше слотів під оперативну пам'ять ({slots2} проти {slots1}). Це дає чудові можливості для майбутнього апгрейду.")

        elif ctype == 'cooler':
            # Відступ тут обов'язковий (зазвичай 4 пробіли або 1 Tab)
            tdp1, tdp2 = get_val(item1, 'tdp', 'max_tdp'), get_val(item2, 'tdp', 'max_tdp')
            
            if tdp1 > tdp2:
                advantages.append(f"{name1} ефективніше відводить тепло...")
            elif tdp2 > tdp1:
                advantages.append(f"{name2} ефективніше відводить тепло...")

        elif ctype == 'case':
            # Для корпусу можемо порівняти підтримку довгих відеокарт
            gpu_len1, gpu_len2 = get_val(item1, 'max_gpu_length_mm'), get_val(item2, 'max_gpu_length_mm')
            if gpu_len1 > gpu_len2:
                advantages.append(f"У {name1} помістяться масивніші відеокарти (до {gpu_len1} мм проти {gpu_len2} мм).")
            elif gpu_len2 > gpu_len1:
                advantages.append(f"У {name2} помістяться масивніші відеокарти (до {gpu_len2} мм проти {gpu_len1} мм).")
            
        return advantages