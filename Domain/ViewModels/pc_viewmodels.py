from dataclasses import dataclass
from typing import List, Optional

# --- ViewModels для ВІДПРАВКИ клієнту (Output) ---

@dataclass
class ComponentShortViewModel:
    """Коротка інформація для списків (випадаючих меню)"""
    id: int
    name: str 
    price: float

@dataclass
class CpuDetailViewModel:
    """Детальна інформація про процесор"""
    id: int
    full_name: str
    socket: str
    cores: int
    tdp: int
    price: float

@dataclass
class GpuDetailViewModel:
    """Детальна інформація про відеокарту"""
    id: int
    full_name: str
    vram: str
    psu_recommended: int
    price: float

@dataclass
class CompatibilityResultViewModel:
    """Результат перевірки: чи підходять деталі одна одній"""
    is_compatible: bool
    total_price: float
    total_wattage: int
    errors: List[str] 

@dataclass
class FullBuildViewModel:
    """Готова оптимальна збірка, яку повертає сервер"""
    cpu: ComponentShortViewModel
    motherboard: ComponentShortViewModel
    gpu: ComponentShortViewModel
    ram: ComponentShortViewModel
    storage: ComponentShortViewModel
    psu: ComponentShortViewModel
    case: ComponentShortViewModel
    cooler: ComponentShortViewModel 
    total_price: float
    performance_score: int 

@dataclass
class BuildComparisonViewModel:
    """Результат порівняння двох збірок"""
    build_1_score: int
    build_2_score: int
    price_difference: float
    winner_build: int 
    explanation_text: str 

# --- ViewModels для ОТРИМАННЯ від клієнта (Input) ---

@dataclass
class FilterRequestViewModel:
    """Те, що клієнт надсилає для фільтрації товарів"""
    min_price: Optional[float]
    max_price: Optional[float]
    brand: Optional[str]

@dataclass
class BuildCheckRequestViewModel:
    """Клієнт надсилає ID обраних деталей, щоб ми перевірили їх сумісність"""
    cpu_id: int
    motherboard_id: int
    gpu_id: Optional[int]
    ram_id: int
    psu_id: int

@dataclass
class AutoBuildRequestViewModel:
    """Запит на автоматичну збірку"""
    target_budget: float
    preference_brand: Optional[str] 

@dataclass
class PurposeBuildRequestViewModel:
    """Запит на збірку під конкретну задачу (ігри, 3D-моделювання, офіс, програмування)"""
    primary_use: str # Головна ціль: "Gaming", "3D_Modeling", "Office", "Video_Editing"
    specific_software: Optional[str] # Наприклад: "Blender", "Cyberpunk 2077", "AutoCAD"
    performance_level: str # Рівень: "Minimum" (бюджетно), "Recommended" (комфортно), "Maximum" (профі)
    resolution: Optional[str] # Роздільна здатність екрану (актуально для ігор та 3D: "1080p", "4K")


# --- НОВІ ViewModels ДЛЯ ОХОЛОДЖЕННЯ, КОРПУСІВ ТА КОРИСТУВАЧІВ ---

@dataclass
class CoolerDetailViewModel:
    """Детальна інформація про кулер або водяне охолодження"""
    id: int
    name: str
    cooler_type: str # "Air" (повітряне) або "Liquid" (водяне)
    max_tdp_dissipation: int # Скільки Ват тепла може відвести
    price: float

@dataclass
class CaseDetailViewModel:
    """Деталі комп'ютерного корпусу"""
    id: int
    name: str
    supported_motherboards: List[str] # Наприклад: ["ATX", "Micro-ATX"]
    max_gpu_length_mm: int # Максимальна довжина відеокарти (дуже важливо!)
    max_cooler_height_mm: int # Максимальна висота баштового кулера
    price: float

@dataclass
class UserProfileViewModel:
    """Профіль користувача"""
    id: int
    username: str
    email: str
    saved_builds_count: int

@dataclass
class UserAuthRequestViewModel:
    """Дані для реєстрації або логіну"""
    email: str
    password_hash: str


# --- НОВІ ViewModels ДЛЯ БЛОКІВ ЖИВЛЕННЯ ТА НАКОПИЧУВАЧІВ ---

@dataclass
class PsuDetailViewModel:
    """Детальна інформація про блок живлення"""
    id: int
    name: str
    wattage: int # Потужність у Ватах (напр. 750)
    efficiency_rating: str # Сертифікат (напр. "80+ Gold", "80+ Bronze")
    modularity: str # "Full", "Semi", "None" (чи відстібаються кабелі)
    price: float

@dataclass
class StorageDetailViewModel:
    """Детальна інформація про накопичувач (SSD/HDD)"""
    id: int
    name: str
    storage_type: str # "NVMe M.2", "SATA SSD", "HDD"
    capacity_gb: int # Об'єм пам'яті (напр. 1000 для 1TB)
    read_speed_mbps: Optional[int] # Швидкість читання (важливо для SSD)
    price: float


@dataclass
class ProfileUpdateRequestViewModel:
    """Дані для редагування профілю"""
    username: Optional[str]
    email: Optional[str]

@dataclass
class PasswordChangeRequestViewModel:
    """Запит на зміну пароля"""
    old_password: str
    new_password: str


# --- НОВІ ViewModels ДЛЯ АНАЛІТИКИ, ТЕМПЕРАТУР ТА ЕКСПОРТУ ---

@dataclass
class GamePerformanceRequestViewModel:
    """Запит на симуляцію FPS у грі"""
    build_id: int
    game_name: str
    resolution: str # "1080p", "1440p", "4K"
    graphics_preset: str # "Low", "Medium", "High", "Ultra"

@dataclass
class PerformanceScoreViewModel:
    """Результат бенчмарку або симуляції FPS"""
    expected_fps: int
    cpu_score_synthetic: int # Бали процесора (напр. Cinebench)
    gpu_score_synthetic: int # Бали відеокарти (напр. TimeSpy)
    bottleneck_percentage: float # Відсоток "пляшкового горлечка"

@dataclass
class ThermalAnalysisRequestViewModel:
    """Запит на аналіз температурного режиму"""
    cpu_id: int
    cooler_id: int
    case_id: int
    ambient_temp_c: int # Кімнатна температура (зазвичай 21-25)

@dataclass
class ThermalResultViewModel:
    """Результат розрахунку температур"""
    estimated_load_temp_c: int # Очікувана температура під навантаженням
    will_throttle: bool # Чи буде скидати частоти (перегрів)
    suggested_case_fans: int # Скільки додаткових кулерів треба докупити

@dataclass
class PriceHistoryViewModel:
    """Точка на графіку історії цін"""
    date: str
    average_price: float

@dataclass
class StoreLinkViewModel:
    """Посилання на зовнішній магазин для покупки деталі"""
    store_name: str # "Rozetka", "Telemart", "Brain"
    url: str
    current_price: float

@dataclass
class ShareableLinkViewModel:
    """Коротке посилання на збірку"""
    short_url: str
    expires_in_days: int

@dataclass
class SaveBuildRequestViewModel:
    """Запит на збереження збірки з усіма деталями"""
    build_name: str
    cpu_id: Optional[int] = None
    gpu_id: Optional[int] = None
    motherboard_id: Optional[int] = None
    ram_id: Optional[int] = None
    storage_id: Optional[int] = None
    psu_id: Optional[int] = None
    cooler_id: Optional[int] = None
    case_id: Optional[int] = None
    mouse_id: Optional[int] = None
    keyboard_id: Optional[int] = None
    headset_id: Optional[int] = None