from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel, CpuDetailViewModel, FilterRequestViewModel
# Імпортуємо репозиторій
from Repositories.hardware_repository import CpuRepository 

class CpuService:
    """Клас бізнес-логіки для процесорів (використовує Репозиторій)"""

    # 1. Dependency Injection
    def __init__(self, cpu_repository: CpuRepository):
        self.cpu_repo = cpu_repository

    def get_all_cpus(self) -> List[ComponentShortViewModel]:
        # Викликаємо базовий метод
        cpus_db = self.cpu_repo.get_all()
        
        result = []
        for c in cpus_db:
            full_name = f"{c.brand} {c.model}"
            result.append(ComponentShortViewModel(id=c.id, name=full_name, price=c.price))
            
        return result

    def get_cpu_details(self, cpu_id: int) -> CpuDetailViewModel:
        # Викликаємо базовий метод
        cpu_db = self.cpu_repo.get_by_id(cpu_id)
        
        if not cpu_db:
            return None
            
        full_name = f"{cpu_db.brand} {cpu_db.model}"
        return CpuDetailViewModel(
            id=cpu_db.id, 
            full_name=full_name, 
            socket=cpu_db.socket, 
            cores=cpu_db.cores, 
            tdp=cpu_db.tdp, 
            price=cpu_db.price
        )

    def filter_cpus(self, filters: FilterRequestViewModel) -> List[CpuDetailViewModel]:
        # 2. Викликаємо наш кастомний метод з CpuRepository
        cpus_db = self.cpu_repo.filter_by_params(
            brand=getattr(filters, 'brand', None),
            min_price=getattr(filters, 'min_price', None),
            max_price=getattr(filters, 'max_price', None)
        )

        result = []
        for cpu_db in cpus_db:
            full_name = f"{cpu_db.brand} {cpu_db.model}"
            result.append(CpuDetailViewModel(
                id=cpu_db.id, 
                full_name=full_name, 
                socket=cpu_db.socket, 
                cores=cpu_db.cores, 
                tdp=cpu_db.tdp, 
                price=cpu_db.price
            ))
            
        return result