from typing import List
from Repositories.base_repository import BaseRepository
from Domain.Models.gpu import GPU
from Domain.Models.cpu import CPU
from Domain.Models.ram import RAM
from Domain.Models.motherboard import Motherboard
from Domain.Models.psu import PSU
from Domain.Models.storage import Storage
from Domain.Models.case import Case
from Domain.Models.cooler import Cooler
from Domain.Models.mouse import Mouse
from Domain.Models.keyboard import Keyboard
from Domain.Models.headset import Headset

class GpuRepository(BaseRepository[GPU]):
    """Репозиторій для роботи з відеокартами"""
    
    def __init__(self):
        super().__init__(GPU)

    # Унікальний метод, який ми забрали з сервісу
    def get_by_max_psu(self, max_wattage: int) -> List[GPU]:
        """Знайти відеокарти, яким вистачить вказаного блоку живлення"""
        return self.model.query.filter(self.model.psu_req <= max_wattage).all()
    
class CpuRepository(BaseRepository[CPU]):
    """Репозиторій для роботи з процесорами"""
    
    def __init__(self):
        super().__init__(CPU)

    # Забрали логіку динамічного фільтрування з сервісу
    def filter_by_params(self, brand: str = None, min_price: float = None, max_price: float = None) -> List[CPU]:
        """Складне фільтрування процесорів за параметрами"""
        query = self.model.query
        
        if brand:
            query = query.filter(self.model.brand.ilike(f"%{brand}%"))
        if min_price is not None:
            query = query.filter(self.model.price >= min_price)
        if max_price is not None:
            query = query.filter(self.model.price <= max_price)
            
        return query.all()
    
class MotherboardRepository(BaseRepository[Motherboard]):
    """Репозиторій для роботи з материнськими платами"""
    def __init__(self):
        super().__init__(Motherboard)

    def get_by_socket(self, socket_name: str) -> List[Motherboard]:
        return self.model.query.filter(self.model.socket == socket_name).all()

    def get_by_form_factor(self, form_factor: str) -> List[Motherboard]:
        return self.model.query.filter(self.model.form == form_factor).all()

class RamRepository(BaseRepository[RAM]):
    """Репозиторій для роботи з оперативною пам'яттю"""
    def __init__(self):
        super().__init__(RAM)

    def get_by_type(self, memory_type: str) -> List[RAM]:
        """Шукає пам'ять за типом (наприклад, DDR4, DDR5)"""
        return self.model.query.filter(self.model.r_type == memory_type).all()
        
    def get_by_capacity(self, gb: int) -> List[RAM]:
        """Шукає пам'ять за об'ємом"""
        return self.model.query.filter(self.model.cap == gb).all()
    
class PsuRepository(BaseRepository[PSU]):
    """Репозиторій для роботи з блоками живлення"""
    def __init__(self):
        super().__init__(PSU)

    def get_by_min_wattage(self, min_wattage: int) -> List[PSU]:
        """Знайти блоки живлення, потужність яких не менша за вказану"""
        return self.model.query.filter(self.model.watts >= min_wattage).all()
    
class StorageRepository(BaseRepository[Storage]):
    """Репозиторій для роботи з накопичувачами"""
    def __init__(self):
        super().__init__(Storage)

    def get_by_type(self, storage_type: str) -> List[Storage]:
        """Знайти накопичувачі за типом (SSD, HDD, NVMe тощо)"""
        return self.model.query.filter(self.model.s_type.ilike(f"%{storage_type}%")).all()
    
class CaseRepository(BaseRepository[Case]):
    """Репозиторій для роботи з корпусами"""
    def __init__(self):
        super().__init__(Case)

class CoolerRepository(BaseRepository[Cooler]):
    """Репозиторій для роботи з системами охолодження"""
    def __init__(self):
        super().__init__(Cooler)

    def get_by_socket(self, socket_name: str) -> List[Cooler]:
        """Знайти кулери, які підходять під певний сокет (наприклад, AM4)"""
        return self.model.query.filter(self.model.socket.ilike(f"%{socket_name}%")).all()

    def get_by_min_tdp(self, cpu_tdp: int) -> List[Cooler]:
        """Знайти кулери, які здатні розсіяти вказане тепло (TDP)"""
        return self.model.query.filter(self.model.tdp >= cpu_tdp).all()
    
class MouseRepository(BaseRepository[Mouse]):
    """Репозиторій для роботи з мишами"""
    def __init__(self):
        super().__init__(Mouse)

class KeyboardRepository(BaseRepository[Keyboard]):
    """Репозиторій для роботи з клавіатурами"""
    def __init__(self):
        super().__init__(Keyboard)

class HeadsetRepository(BaseRepository[Headset]):
    """Репозиторій для роботи з навушниками"""
    def __init__(self):
        super().__init__(Headset)