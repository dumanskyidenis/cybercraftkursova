from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, GpuDetailViewModel
from Repositories.hardware_repository import GpuRepository # <--- Додали імпорт репозиторію

class GpuService:
    """Клас бізнес-логіки для відеокарт (використовує Репозиторій)"""

    # 1. Передаємо репозиторій через конструктор
    def __init__(self, gpu_repository: GpuRepository):
        self.gpu_repo = gpu_repository

    def get_all_gpus(self) -> List[ComponentShortViewModel]:
        # 2. Викликаємо базовий метод get_all()
        gpus_db = self.gpu_repo.get_all()
        
        result = []
        for g in gpus_db:
            full_name = f"{g.brand} {g.model}"
            result.append(ComponentShortViewModel(id=g.id, name=full_name, price=g.price))
            
        return result

    def get_gpu_details(self, gpu_id: int) -> GpuDetailViewModel:
        # 3. Викликаємо базовий метод get_by_id()
        gpu_db = self.gpu_repo.get_by_id(gpu_id)
        
        if not gpu_db:
            return None
            
        full_name = f"{gpu_db.brand} {gpu_db.model}"
        return GpuDetailViewModel(
            id=gpu_db.id, 
            full_name=full_name, 
            vram=gpu_db.vram, 
            psu_recommended=gpu_db.psu_req, 
            price=gpu_db.price
        )

    def get_gpus_by_psu_limit(self, max_wattage: int) -> List[GpuDetailViewModel]:
        # 4. Викликаємо наш кастомний метод з GpuRepository
        gpus_db = self.gpu_repo.get_by_max_psu(max_wattage)
        
        result = []
        for gpu_db in gpus_db:
            full_name = f"{gpu_db.brand} {gpu_db.model}"
            result.append(GpuDetailViewModel(
                id=gpu_db.id, 
                full_name=full_name, 
                vram=gpu_db.vram, 
                psu_recommended=gpu_db.psu_req, 
                price=gpu_db.price
            ))
            
        return result