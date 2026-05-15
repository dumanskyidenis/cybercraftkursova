from typing import List
from Domain.ViewModels.pc_viewmodels import ComponentShortViewModel

# 1. Імпортуємо всі три репозиторії
from Repositories.hardware_repository import MouseRepository, KeyboardRepository, HeadsetRepository

class PeripheralsService:
    """Клас бізнес-логіки для периферії (використовує Репозиторії)"""

    # 2. Передаємо всі три репозиторії через конструктор
    def __init__(self, mouse_repo: MouseRepository, keyboard_repo: KeyboardRepository, headset_repo: HeadsetRepository):
        self.mouse_repo = mouse_repo
        self.keyboard_repo = keyboard_repo
        self.headset_repo = headset_repo

    def get_all_mice(self) -> List[ComponentShortViewModel]:
        # 3. Використовуємо репозиторій мишок
        mice_db = self.mouse_repo.get_all()
        
        result = []
        for m in mice_db:
            full_name = f"{m.brand} {m.model}"
            result.append(ComponentShortViewModel(id=m.id, name=full_name, price=m.price))
        return result

    def get_all_keyboards(self) -> List[ComponentShortViewModel]:
        # 4. Використовуємо репозиторій клавіатур
        keyboards_db = self.keyboard_repo.get_all()
        
        result = []
        for kb in keyboards_db:
            full_name = f"{kb.brand} {kb.model}"
            result.append(ComponentShortViewModel(id=kb.id, name=full_name, price=kb.price))
        return result

    def get_all_headsets(self) -> List[ComponentShortViewModel]:
        # 5. Використовуємо репозиторій навушників
        headsets_db = self.headset_repo.get_all()
        
        result = []
        for h in headsets_db:
            full_name = f"{h.brand} {h.model}"
            result.append(ComponentShortViewModel(id=h.id, name=full_name, price=h.price))
        return result