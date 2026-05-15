from typing import List
from Domain.ViewModels.pc_viewmodels import BuildCheckRequestViewModel, CompatibilityResultViewModel

# 1. Імпортуємо всі потрібні репозиторії замість моделей
from Repositories.hardware_repository import (
    CpuRepository, MotherboardRepository, GpuRepository, RamRepository, PsuRepository
)

class BuildService:
    """Головний сервіс конфігуратора для перевірки збірок (використовує Репозиторії)"""

    # 2. Передаємо всі репозиторії через конструктор
    def __init__(self, cpu_repo: CpuRepository, mb_repo: MotherboardRepository, 
                 gpu_repo: GpuRepository, ram_repo: RamRepository, psu_repo: PsuRepository):
        self.cpu_repo = cpu_repo
        self.mb_repo = mb_repo
        self.gpu_repo = gpu_repo
        self.ram_repo = ram_repo
        self.psu_repo = psu_repo

    def calculate_build_power(self, build_data: BuildCheckRequestViewModel) -> int:
        total_watts = 50 # Базове споживання (материнка, вентилятори, накопичувачі)

        # 3. Використовуємо репозиторії замість БД
        cpu = self.cpu_repo.get_by_id(build_data.cpu_id) if build_data.cpu_id else None
        gpu = self.gpu_repo.get_by_id(build_data.gpu_id) if build_data.gpu_id else None

        if cpu:
            total_watts += cpu.tdp
        
        if gpu:
            total_watts += getattr(gpu, 'tdp', 200) 

        return total_watts

    def validate_build_compatibility(self, build_data: BuildCheckRequestViewModel) -> CompatibilityResultViewModel:
        errors = []
        total_price = 0.0

        # 4. Використовуємо репозиторії
        cpu = self.cpu_repo.get_by_id(build_data.cpu_id) if build_data.cpu_id else None
        mb = self.mb_repo.get_by_id(build_data.motherboard_id) if build_data.motherboard_id else None
        gpu = self.gpu_repo.get_by_id(build_data.gpu_id) if build_data.gpu_id else None
        ram = self.ram_repo.get_by_id(build_data.ram_id) if build_data.ram_id else None
        psu = self.psu_repo.get_by_id(build_data.psu_id) if build_data.psu_id else None

        for comp in [cpu, mb, gpu, ram, psu]:
            if comp:
                total_price += comp.price

        if cpu and mb:
            if cpu.socket != mb.socket:
                errors.append(f"Конфлікт: Процесор має сокет {cpu.socket}, а материнська плата — {mb.socket}.")

        total_wattage = self.calculate_build_power(build_data)
        if psu:
            required_wattage = int(total_wattage * 1.2)
            if psu.watts < required_wattage:
                errors.append(f"Слабкий БЖ: Збірка споживає ~{total_wattage}W. Рекомендовано мінімум {required_wattage}W, а обрано {psu.watts}W.")

        return CompatibilityResultViewModel(
            is_compatible=len(errors) == 0,
            total_price=total_price,
            total_wattage=total_wattage,
            errors=errors
        )

    def generate_build_summary_txt(self, build_data: BuildCheckRequestViewModel) -> str:
        result = self.validate_build_compatibility(build_data)
        
        summary = "=== ВАША КОМП'ЮТЕРНА ЗБІРКА ===\n"
        summary += f"Загальна вартість: {result.total_price} грн (або $)\n"
        summary += f"Енергоспоживання: ~{result.total_wattage}W\n\n"
        
        if result.is_compatible:
            summary += "✅ Збірка ідеально сумісна!\n"
        else:
            summary += "❌ Увага! Є проблеми сумісності:\n"
            for err in result.errors:
                summary += f" - {err}\n"
                
        return summary