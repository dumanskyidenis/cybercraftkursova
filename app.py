from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db
import dataclasses
import os
from werkzeug.utils import secure_filename

# 1. Імпорт моделей бази даних
from Domain.Models.cpu import CPU
from Domain.Models.gpu import GPU
from Domain.Models.motherboard import Motherboard
from Domain.Models.ram import RAM
from Domain.Models.storage import Storage
from Domain.Models.psu import PSU
from Domain.Models.cooler import Cooler
from Domain.Models.case import Case
from Domain.Models.mouse import Mouse
from Domain.Models.keyboard import Keyboard
from Domain.Models.headset import Headset
from Domain.Models.user import User
from Domain.Models.saved_build import SavedBuild

from Domain.ViewModels.pc_viewmodels import FilterRequestViewModel
from BusinessLogic.cpu_service import CpuService
from Controllers.cpu_controller import CpuController

from BusinessLogic.gpu_service import GpuService
from Controllers.gpu_controller import GpuController
from Repositories.hardware_repository import GpuRepository, CpuRepository, RamRepository, MotherboardRepository, PsuRepository, StorageRepository, CaseRepository, CoolerRepository, MouseRepository, KeyboardRepository, HeadsetRepository

from BusinessLogic.motherboard_service import MotherboardService
from Controllers.motherboard_controller import MotherboardController

from BusinessLogic.ram_service import RamService
from Controllers.memory_controller import MemoryController

from BusinessLogic.case_service import CaseService
from Controllers.case_controller import CaseController

from BusinessLogic.cooling_service import CoolingService
from Controllers.cooling_controller import CoolingController

from BusinessLogic.psu_service import PsuService
from Controllers.psu_controller import PsuController

from BusinessLogic.storage_service import StorageService
from Controllers.storage_controller import StorageController

from BusinessLogic.peripherals_service import PeripheralsService
from Controllers.peripherals_controller import PeripheralsController

from BusinessLogic.benchmark_service import BenchmarkService
from Controllers.benchmark_controller import BenchmarkController
from Domain.ViewModels.pc_viewmodels import GamePerformanceRequestViewModel # Додай цей імпорт

from BusinessLogic.build_service import BuildService
from Controllers.build_controller import BuildController
from Domain.ViewModels.pc_viewmodels import BuildCheckRequestViewModel

from BusinessLogic.export_service import ExportService
from Controllers.export_controller import ExportController

from BusinessLogic.smart_configurator_service import SmartConfiguratorService
from Controllers.smart_configurator_controller import SmartConfiguratorController
from Domain.ViewModels.pc_viewmodels import AutoBuildRequestViewModel, PurposeBuildRequestViewModel

from Domain.ViewModels.pc_viewmodels import ThermalAnalysisRequestViewModel
from BusinessLogic.thermal_dynamics_service import ThermalDynamicsService
from Controllers.thermal_dynamics_controller import ThermalDynamicsController

from BusinessLogic.comparison_service import ComparisonService
from Controllers.comparison_controller import ComparisonController

from BusinessLogic.market_analytics_service import MarketAnalyticsService
from Controllers.market_analytics_controller import MarketAnalyticsController

from Domain.ViewModels.pc_viewmodels import (
    ProfileUpdateRequestViewModel, 
    PasswordChangeRequestViewModel,
    SaveBuildRequestViewModel
)
from BusinessLogic.profile_service import ProfileService
from Controllers.profile_controller import ProfileController

from Domain.ViewModels.pc_viewmodels import UserAuthRequestViewModel
from BusinessLogic.auth_service import AuthService
from Controllers.auth_controller import AuthController
from Repositories.user_repository import UserRepository
from Repositories.saved_build_repository import SavedBuildRepository

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
app.json.ensure_ascii = False

# ПІДКЛЮЧЕННЯ ДО БД
# На початку файлу додай імпорт, якщо його немає: import os

# Змінюємо налаштування підключення:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:denoro2007@localhost:5432/pc_builder_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False 
app.config['UPLOAD_FOLDER'] = 'static/avatars'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

# ==========================================
# 3. DEPENDENCY INJECTION CONTAINER
# ==========================================

build_repo = SavedBuildRepository() 

cpu_repo = CpuRepository()
cpu_service = CpuService(cpu_repository=cpu_repo)
cpu_controller = CpuController(cpu_service=cpu_service)

gpu_repo = GpuRepository()
gpu_service = GpuService(gpu_repository=gpu_repo)
gpu_controller = GpuController(gpu_service=gpu_service)

mb_repo = MotherboardRepository()
# Тепер передаємо репозиторій у сервіс:
mb_service = MotherboardService(motherboard_repository=mb_repo) 
mb_controller = MotherboardController(motherboard_service=mb_service)

ram_repo = RamRepository()
# Передаємо в RamService ОБИДВА репозиторії
ram_service = RamService(ram_repository=ram_repo, motherboard_repository=mb_repo)
memory_controller = MemoryController(ram_service=ram_service)

case_repo = CaseRepository()
case_service = CaseService(case_repository=case_repo)
case_controller = CaseController(case_service=case_service)

cooler_repo = CoolerRepository()
cooling_service = CoolingService(cooler_repository=cooler_repo)
cooling_controller = CoolingController(cooling_service=cooling_service)

psu_repo = PsuRepository()
psu_service = PsuService(psu_repository=psu_repo)
psu_controller = PsuController(psu_service=psu_service)

storage_repo = StorageRepository()
storage_service = StorageService(storage_repository=storage_repo)
storage_controller = StorageController(storage_service=storage_service)

mouse_repo = MouseRepository()
keyboard_repo = KeyboardRepository()
headset_repo = HeadsetRepository()


peripherals_service = PeripheralsService(
    mouse_repo=mouse_repo, 
    keyboard_repo=keyboard_repo, 
    headset_repo=headset_repo
)
peripherals_controller = PeripheralsController(peripherals_service=peripherals_service)

benchmark_service = BenchmarkService(
    build_repo=build_repo,
    cpu_repo=cpu_repo,
    gpu_repo=gpu_repo
)
benchmark_controller = BenchmarkController(benchmark_service=benchmark_service)

build_service = BuildService(
    cpu_repo=cpu_repo,
    mb_repo=mb_repo,
    gpu_repo=gpu_repo,
    ram_repo=ram_repo,
    psu_repo=psu_repo
)
build_controller = BuildController(build_service=build_service)

export_service = ExportService(
    build_repo=build_repo,
    cpu_repo=cpu_repo,
    gpu_repo=gpu_repo,
    mb_repo=mb_repo,
    ram_repo=ram_repo,
    storage_repo=storage_repo,
    psu_repo=psu_repo,
    mouse_repo=mouse_repo,
    keyboard_repo=keyboard_repo,
    headset_repo=headset_repo
)
export_controller = ExportController(export_service=export_service)

smart_service = SmartConfiguratorService(
    cpu_repo=cpu_repo,
    gpu_repo=gpu_repo,
    mb_repo=mb_repo,
    ram_repo=ram_repo,
    storage_repo=storage_repo,
    psu_repo=psu_repo,
    case_repo=case_repo,
    cooler_repo=cooler_repo
)
smart_controller = SmartConfiguratorController(smart_service=smart_service)

thermal_service = ThermalDynamicsService(
    cpu_repo=cpu_repo, 
    cooler_repo=cooler_repo, 
    case_repo=case_repo, 
    mb_repo=mb_repo
)
thermal_controller = ThermalDynamicsController(thermal_service=thermal_service)

# Шукай щось схоже на це в app.py
comparison_service = ComparisonService(
    cpu_repo=cpu_repo, 
    gpu_repo=gpu_repo, 
    mb_repo=mb_repo, 
    ram_repo=ram_repo, 
    psu_repo=psu_repo,
    storage_repo=storage_repo,  # <--- ДОДАЙ ЦЕ
    cooler_repo=cooler_repo,    # <--- ДОДАЙ ЦЕ
    case_repo=case_repo         # <--- ДОДАЙ ЦЕ
)

# Переконайся, що ці репозиторії імпортовані і створені в app.py вище!
comparison_controller = ComparisonController(comparison_service=comparison_service)

market_service = MarketAnalyticsService(
    cpu_repo=cpu_repo,
    gpu_repo=gpu_repo,
    mb_repo=mb_repo,
    ram_repo=ram_repo,
    storage_repo=storage_repo,
    psu_repo=psu_repo,
    case_repo=case_repo,         # <-- ДОДАНО
    cooler_repo=cooler_repo,     # <-- ДОДАНО
    mouse_repo=mouse_repo,       # <-- ДОДАНО
    keyboard_repo=keyboard_repo, # <-- ДОДАНО
    headset_repo=headset_repo    # <-- ДОДАНО
)
market_controller = MarketAnalyticsController(market_service=market_service)


user_repo = UserRepository()

# Передаємо ОБОХ у ProfileService
profile_service = ProfileService(user_repository=user_repo, build_repository=build_repo)
profile_controller = ProfileController(profile_service=profile_service)

# auth_service вже має user_repo з минулого кроку
auth_service = AuthService(user_repository=user_repo)
auth_controller = AuthController(auth_service=auth_service)



def init_db():
    with app.app_context():
        db.create_all() 
        print("✅ Базу підключено та перевірено!")

        from Domain.Models.user import User
        if not User.query.first():
            test_user = User(
                username="Denis_VNTU", 
                email="denis@vntu.edu.ua", 
                password_hash="old_password_123"
         )
            db.session.add(test_user)
            db.session.commit()
            print("✅ Тестового користувача (ID: 1) успішно створено!")


# ==========================================
# 4. МАРШРУТИ (ROUTES) ДЛЯ ПРОЦЕСОРІВ
# ==========================================

@app.route('/api/cpus', methods=['GET'])
def get_all_cpus():
    """Отримати всі процесори"""
    # Контролер робить всю роботу
    cpus = cpu_controller.get_all_cpus()
    # Перетворюємо об'єкти в JSON
    return jsonify([dataclasses.asdict(c) for c in cpus])


@app.route('/api/cpus/<int:cpu_id>', methods=['GET'])
def get_cpu_details(cpu_id):
    """Отримати деталі одного процесора за його ID"""
    cpu = cpu_controller.get_cpu_details(cpu_id)
    if not cpu:
        return jsonify({'error': 'Процесор не знайдено'}), 404
    return jsonify(dataclasses.asdict(cpu))


@app.route('/api/cpus/filter', methods=['POST'])
def filter_cpus():
    """Відфільтрувати процесори (очікує JSON з параметрами)"""
    # Отримуємо дані від користувача (наприклад, {"brand": "AMD", "max_price": 6000})
    data = request.json or {}
    
    # Запаковуємо їх у нашу ViewModel
    filters = FilterRequestViewModel(
        brand=data.get('brand'),
        min_price=data.get('min_price'),
        max_price=data.get('max_price')
    )
    
    # Передаємо в контролер
    cpus = cpu_controller.filter_cpus(filters)
    return jsonify([dataclasses.asdict(c) for c in cpus])

# ==========================================

# ==========================================
# МАРШРУТИ ДЛЯ ВІДЕОКАРТ
# ==========================================
@app.route('/api/gpus', methods=['GET'])
def get_all_gpus():
    gpus = gpu_controller.get_all_gpus()
    return jsonify([dataclasses.asdict(g) for g in gpus])

@app.route('/api/gpus/<int:gpu_id>', methods=['GET'])
def get_gpu_details(gpu_id):
    gpu = gpu_controller.get_gpu_details(gpu_id)
    if not gpu:
        return jsonify({'error': 'Відеокарту не знайдено'}), 404
    return jsonify(dataclasses.asdict(gpu))

@app.route('/api/gpus/psu_limit/<int:wattage>', methods=['GET'])
def get_gpus_by_psu(wattage):
    gpus = gpu_controller.get_gpus_by_psu_limit(wattage)
    return jsonify([dataclasses.asdict(g) for g in gpus])

# ==========================================
# МАРШРУТИ ДЛЯ МАТЕРИНСЬКИХ ПЛАТ
# ==========================================
@app.route('/api/motherboards', methods=['GET'])
def get_all_motherboards():
    mbs = mb_controller.get_all_motherboards()
    return jsonify([dataclasses.asdict(m) for m in mbs])

@app.route('/api/motherboards/socket/<string:socket_name>', methods=['GET'])
def get_motherboards_by_socket(socket_name):
    mbs = mb_controller.get_motherboards_by_socket(socket_name)
    return jsonify([dataclasses.asdict(m) for m in mbs])

@app.route('/api/motherboards/form/<string:form_factor>', methods=['GET'])
def get_motherboards_by_form_factor(form_factor):
    mbs = mb_controller.get_motherboards_by_form_factor(form_factor)
    return jsonify([dataclasses.asdict(m) for m in mbs])

# ==========================================
# МАРШРУТИ ДЛЯ ОПЕРАТИВНОЇ ПАМ'ЯТІ (RAM)
# ==========================================
@app.route('/api/rams', methods=['GET'])
def get_all_ram():
    rams = memory_controller.get_all_ram()
    return jsonify([dataclasses.asdict(r) for r in rams])

@app.route('/api/rams/compatible/<int:motherboard_id>', methods=['GET'])
def get_compatible_ram(motherboard_id):
    rams = memory_controller.get_compatible_ram(motherboard_id)
    return jsonify([dataclasses.asdict(r) for r in rams])

@app.route('/api/rams/capacity/<int:min_gb>', methods=['GET'])
def get_ram_by_capacity(min_gb):
    rams = memory_controller.get_ram_by_capacity(min_gb)
    return jsonify([dataclasses.asdict(r) for r in rams])

# ==========================================
# МАРШРУТИ ДЛЯ КОРПУСІВ (CASES)
# ==========================================
@app.route('/api/cases', methods=['GET'])
def get_all_cases():
    cases = case_controller.get_all_cases()
    return jsonify([dataclasses.asdict(c) for c in cases])

@app.route('/api/cases/<int:case_id>', methods=['GET'])
def get_case_details(case_id):
    case_data = case_controller.get_case_details(case_id)
    if not case_data:
        return jsonify({'error': 'Корпус не знайдено'}), 404
    return jsonify(dataclasses.asdict(case_data))

@app.route('/api/cases/<int:case_id>/clearance', methods=['GET'])
def check_clearance(case_id):
    # Отримуємо розміри прямо з посилання (URL parameters)
    # Наприклад: /api/cases/1/clearance?gpu=300&cooler=150
    # request ми вже імпортували раніше з flask
    gpu_len = request.args.get('gpu', default=0, type=int)
    cooler_h = request.args.get('cooler', default=0, type=int)
    
    is_compatible = case_controller.check_case_clearance(case_id, gpu_len, cooler_h)
    return jsonify({
        'case_id': case_id, 
        'is_compatible': is_compatible,
        'checked_gpu_length': gpu_len,
        'checked_cooler_height': cooler_h
    })

# ==========================================
# МАРШРУТИ ДЛЯ ОХОЛОДЖЕННЯ (COOLERS)
# ==========================================
@app.route('/api/coolers', methods=['GET'])
def get_all_coolers():
    coolers = cooling_controller.get_all_coolers()
    return jsonify([dataclasses.asdict(c) for c in coolers])

@app.route('/api/coolers/socket/<string:socket_name>', methods=['GET'])
def get_coolers_by_socket(socket_name):
    coolers = cooling_controller.get_coolers_by_socket(socket_name)
    return jsonify([dataclasses.asdict(c) for c in coolers])

@app.route('/api/coolers/tdp/<int:cpu_tdp>', methods=['GET'])
def get_coolers_by_tdp(cpu_tdp):
    coolers = cooling_controller.get_coolers_by_tdp(cpu_tdp)
    return jsonify([dataclasses.asdict(c) for c in coolers])

# ==========================================
# МАРШРУТИ ДЛЯ БЛОКІВ ЖИВЛЕННЯ (PSU)
# ==========================================
@app.route('/api/psus', methods=['GET'])
def get_all_psus():
    psus = psu_controller.get_all_psus()
    return jsonify([dataclasses.asdict(p) for p in psus])

@app.route('/api/psus/<int:psu_id>', methods=['GET'])
def get_psu_details(psu_id):
    psu = psu_controller.get_psu_details(psu_id)
    if not psu:
        return jsonify({'error': 'Блок живлення не знайдено'}), 404
    return jsonify(dataclasses.asdict(psu))

@app.route('/api/psus/wattage/<int:min_wattage>', methods=['GET'])
def get_psus_by_min_wattage(min_wattage):
    psus = psu_controller.get_psus_by_min_wattage(min_wattage)
    return jsonify([dataclasses.asdict(p) for p in psus])

# ==========================================
# МАРШРУТИ ДЛЯ НАКОПИЧУВАЧІВ (STORAGE)
# ==========================================
@app.route('/api/storage', methods=['GET'])
def get_all_storage():
    storages = storage_controller.get_all_storage_devices()
    return jsonify([dataclasses.asdict(s) for s in storages])

@app.route('/api/storage/<int:storage_id>', methods=['GET'])
def get_storage_details(storage_id):
    storage_data = storage_controller.get_storage_details(storage_id)
    if not storage_data:
        return jsonify({'error': 'Накопичувач не знайдено'}), 404
    return jsonify(dataclasses.asdict(storage_data))

@app.route('/api/storage/type/<string:storage_type>', methods=['GET'])
def get_storage_by_type(storage_type):
    storages = storage_controller.get_storage_by_type(storage_type)
    return jsonify([dataclasses.asdict(s) for s in storages])

# ==========================================
# МАРШРУТИ ДЛЯ ПЕРИФЕРІЇ
# ==========================================
@app.route('/api/peripherals/mice', methods=['GET'])
def get_all_mice():
    mice = peripherals_controller.get_all_mice()
    return jsonify([dataclasses.asdict(m) for m in mice])

@app.route('/api/peripherals/keyboards', methods=['GET'])
def get_all_keyboards():
    keyboards = peripherals_controller.get_all_keyboards()
    return jsonify([dataclasses.asdict(kb) for kb in keyboards])

@app.route('/api/peripherals/headsets', methods=['GET'])
def get_all_headsets():
    headsets = peripherals_controller.get_all_headsets()
    return jsonify([dataclasses.asdict(h) for h in headsets])

# ==========================================
# МАРШРУТИ ДЛЯ БЕНЧМАРКІВ ТА АНАЛІТИКИ
# ==========================================
@app.route('/api/benchmarks/fps', methods=['POST'])
def predict_game_fps():
    # Отримуємо JSON від клієнта (наприклад, з фронтенду або Postman)
    data = request.get_json()
    
    # Перетворюємо сирий словник (dict) на твою красиву ViewModel
    req_model = GamePerformanceRequestViewModel(
        build_id=data.get('build_id', 0),
        game_name=data.get('game_name', 'Unknown Game'),
        resolution=data.get('resolution', '1080p'),
        graphics_preset=data.get('graphics_preset', 'High')
    )
    
    # Передаємо в контролер
    score = benchmark_controller.predict_game_fps(req_model)
    return jsonify(dataclasses.asdict(score))

@app.route('/api/benchmarks/synthetic/<int:build_id>', methods=['GET'])
def get_synthetic_score(build_id):
    score = benchmark_controller.get_synthetic_score(build_id)
    return jsonify(dataclasses.asdict(score))

@app.route('/api/benchmarks/bottleneck', methods=['GET'])
def calculate_bottleneck():
    # Дістаємо параметри з URL (напр. ?cpu=1&gpu=3&res=1440p)
    cpu_id = request.args.get('cpu', type=int)
    gpu_id = request.args.get('gpu', type=int)
    res = request.args.get('res', default='1080p', type=str)
    
    result_text = benchmark_controller.calculate_bottleneck(cpu_id, gpu_id, res)
    return jsonify({"bottleneck_analysis": result_text})

@app.route('/api/benchmarks/analyze', methods=['POST'])
def analyze_custom_system():
    data = request.get_json()
    cpu_id = data.get('cpu_id')
    gpu_id = data.get('gpu_id')
    resolution = data.get('resolution', '1080p')
    game_name = data.get('game_name', 'Cyberpunk 2077')
    
    # Викликаємо сервіс напряму
    result = benchmark_service.analyze_custom_system(cpu_id, gpu_id, resolution, game_name)
    
    if "error" in result:
        return jsonify(result), 400
        
    return jsonify(result)

# ==========================================
# МАРШРУТИ ДЛЯ ЗБІРОК (BUILD VALIDATION)
# ==========================================
@app.route('/api/build/validate', methods=['POST'])
def validate_build():
    data = request.get_json()
    
    # Збираємо запит від користувача
    req_model = BuildCheckRequestViewModel(
        cpu_id=data.get('cpu_id', 0),
        motherboard_id=data.get('motherboard_id', 0),
        gpu_id=data.get('gpu_id'), # Optional
        ram_id=data.get('ram_id', 0),
        psu_id=data.get('psu_id', 0)
    )
    
    result = build_controller.validate_build_compatibility(req_model)
    return jsonify(dataclasses.asdict(result))

@app.route('/api/build/summary', methods=['POST'])
def get_build_summary():
    data = request.get_json()
    
    req_model = BuildCheckRequestViewModel(
        cpu_id=data.get('cpu_id', 0),
        motherboard_id=data.get('motherboard_id', 0),
        gpu_id=data.get('gpu_id'),
        ram_id=data.get('ram_id', 0),
        psu_id=data.get('psu_id', 0)
    )
    
    txt_result = build_controller.generate_build_summary_txt(req_model)
    # Віддаємо простим текстом
    return txt_result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

# ==========================================
# МАРШРУТИ ДЛЯ ЕКСПОРТУ (EXPORT)
# ==========================================

@app.route('/api/build/<int:build_id>', methods=['GET'])
def get_public_build_details(build_id):
    """Отримати конфігурацію збереженої збірки за ID"""
    from Domain.Models.saved_build import SavedBuild
    
    build = SavedBuild.query.get(build_id)
    if not build:
        return jsonify({"error": "Збірку не знайдено"}), 404
        
    return jsonify({
        "name": build.build_name,
        "cpu_id": build.cpu_id,
        "gpu_id": build.gpu_id,
        "motherboard_id": build.motherboard_id,
        "ram_id": build.ram_id,
        "storage_id": build.storage_id,
        "psu_id": build.psu_id,
        "cooler_id": build.cooler_id,
        "case_id": build.case_id,
        "mouse_id": build.mouse_id,
        "keyboard_id": build.keyboard_id,
        "headset_id": build.headset_id
    }), 200
@app.route('/api/export/pdf/<int:build_id>', methods=['GET'])
def get_pdf_export(build_id):
    file_path = export_controller.generate_pdf_specification(build_id)
    return jsonify({"pdf_download_url": file_path})

@app.route('/api/export/markdown/<int:build_id>', methods=['GET'])
def get_markdown_export(build_id):
    md_text = export_controller.generate_reddit_markdown(build_id)
    return jsonify({"markdown_text": md_text})

@app.route('/api/export/share/<int:build_id>', methods=['GET'])
def get_share_link(build_id):
    link_model = export_controller.create_shareable_shortlink(build_id)
    return jsonify(dataclasses.asdict(link_model))


# ==========================================
# МАРШРУТИ ДЛЯ РОЗУМНОГО КОНФІГУРАТОРА
# ==========================================
# ==========================================
# МАРШРУТИ ДЛЯ РОЗУМНОГО КОНФІГУРАТОРА
# ==========================================
@app.route('/api/smart/auto-build', methods=['POST'])
def auto_build():
    data = request.get_json()
    target_budget = float(data.get('target_budget', 25000.0))
    req_model = AutoBuildRequestViewModel(
        target_budget=target_budget,
        preference_brand=data.get('preference_brand')
    )
    
    result = smart_controller.get_best_build_by_budget(req_model)
    
    # ПЕРЕВІРКА НА БЮДЖЕТ (+10% похибки, щоб бути гнучкими)
    if result and hasattr(result, 'total_price'):
        if result.total_price > (target_budget * 1.10):
            return jsonify({
                "error": f"Замалий бюджет! Найдешевша оптимальна збірка коштує мінімум {result.total_price} ₴. Спробуйте збільшити суму."
            }), 400

    return jsonify(dataclasses.asdict(result))

@app.route('/api/smart/purpose-build', methods=['POST'])
def purpose_build():
    data = request.get_json()
    # Витягуємо бюджет, який передав наш оновлений фронтенд
    target_budget = float(data.get('target_budget', 0.0)) 
    
    req_model = PurposeBuildRequestViewModel(
        primary_use=data.get('primary_use', 'Gaming'),
        specific_software=data.get('specific_software', 'Cyberpunk 2077'),
        performance_level=data.get('performance_level', 'Recommended'),
        resolution=data.get('resolution', '1080p')
    )
    
    result = smart_controller.get_build_for_game(req_model)
    
    # ПЕРЕВІРКА НА БЮДЖЕТ ДЛЯ ЦІЛЬОВОЇ ЗБІРКИ
    if target_budget > 0 and result and hasattr(result, 'total_price'):
        if result.total_price > (target_budget * 1.10): 
            return jsonify({
                "error": f"Недостатньо коштів! Для комфортної роботи/гри у '{req_model.specific_software}' найдешевша збірка коштує мінімум {result.total_price} ₴. Спробуйте збільшити бюджет."
            }), 400

    return jsonify(dataclasses.asdict(result))

@app.route('/api/smart/upgrade', methods=['GET'])
def suggest_upgrade():
    # Отримуємо параметри з URL (напр. ?budget=8000&cpu=1&gpu=2)
    budget = request.args.get('budget', default=0.0, type=float)
    cpu_id = request.args.get('cpu', default=0, type=int)
    gpu_id = request.args.get('gpu', default=0, type=int)
    
    suggestion = smart_controller.upgrade_suggestion(budget, cpu_id, gpu_id)
    return jsonify({"upgrade_advice": suggestion})

# ==========================================
# МАРШРУТИ ДЛЯ ТЕМПЕРАТУР ТА ОХОЛОДЖЕННЯ
# ==========================================
@app.route('/api/thermal/estimate', methods=['POST'])
def estimate_thermals():
    data = request.get_json()
    req_model = ThermalAnalysisRequestViewModel(
        cpu_id=data.get('cpu_id', 1),
        cooler_id=data.get('cooler_id', 1),
        case_id=data.get('case_id', 1),
        ambient_temp_c=data.get('ambient_temp_c', 22) # Кімнатна температура
    )
    
    result = thermal_controller.estimate_thermal_throttling(req_model)
    return jsonify(dataclasses.asdict(result))

@app.route('/api/thermal/overclocking', methods=['GET'])
def check_overclocking():
    # Отримуємо параметри з URL (напр. ?cpu=1&mb=2)
    cpu_id = request.args.get('cpu', default=1, type=int)
    mb_id = request.args.get('mb', default=1, type=int)
    
    advice = thermal_controller.get_overclocking_headroom(cpu_id, mb_id)
    return jsonify({"overclocking_advice": advice})

@app.route('/api/thermal/airflow', methods=['GET'])
def suggest_airflow():
    case_id = request.args.get('case', default=1, type=int)
    total_tdp = request.args.get('tdp', default=100, type=int)
    
    suggestion = thermal_controller.suggest_airflow_optimization(case_id, total_tdp)
    return jsonify({"airflow_suggestion": suggestion})

# ==========================================
# МАРШРУТИ ДЛЯ ПОРІВНЯННЯ ТА БАЛАНСУ
# ==========================================

@app.route('/api/comparison/balance', methods=['POST'])
def compare_balance():
    data = request.json
    cpu_id = data.get('cpu_id')
    gpu_id = data.get('gpu_id')
    
    if not cpu_id or not gpu_id:
        return jsonify({"error": "Оберіть і CPU, і GPU"}), 400
        
    try:
        # Викликаємо метод з твого контролера
        advice = comparison_controller.compare_cpu_gpu_balance(cpu_id, gpu_id)
        return jsonify({"advice": advice}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/comparison/components', methods=['POST'])
def compare_components():
    data = request.json
    comp_type = data.get('component_type')
    id1 = data.get('item_id_1')
    id2 = data.get('item_id_2')
    
    try:
        # Викликаємо контролер
        advantages = comparison_controller.compare_components(comp_type, id1, id2)
        return jsonify({"advantages": advantages}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/api/compare/builds', methods=['POST'])
def compare_builds():
    data = request.get_json()
    
    # Витягуємо дві збірки з отриманого JSON
    b1_data = data.get('build_1', {})
    b2_data = data.get('build_2', {})
    
    build_1 = BuildCheckRequestViewModel(
        cpu_id=b1_data.get('cpu_id') or 0, motherboard_id=b1_data.get('motherboard_id') or 0,
        gpu_id=b1_data.get('gpu_id') or 0, ram_id=b1_data.get('ram_id') or 0, psu_id=b1_data.get('psu_id') or 0
    )
    build_2 = BuildCheckRequestViewModel(
        cpu_id=b2_data.get('cpu_id') or 0, motherboard_id=b2_data.get('motherboard_id') or 0,
        gpu_id=b2_data.get('gpu_id') or 0, ram_id=b2_data.get('ram_id') or 0, psu_id=b2_data.get('psu_id') or 0
    )
    
    # ДОДАЄМО ІНШІ ДЕТАЛІ ДЛЯ ПОРІВНЯННЯ (яких немає в стандартній моделі)
    build_1.storage_id = b1_data.get('storage_id')
    build_1.cooler_id = b1_data.get('cooler_id')
    build_1.case_id = b1_data.get('case_id')
    
    build_2.storage_id = b2_data.get('storage_id')
    build_2.cooler_id = b2_data.get('cooler_id')
    build_2.case_id = b2_data.get('case_id')
    
    result = comparison_controller.compare_two_builds(build_1, build_2)
    
    # ВИПРАВЛЕНО: result тепер словник (dict), тому dataclasses.asdict тут викликав помилку
    return jsonify(result)
@app.route('/api/compare/balance', methods=['GET'])
def check_balance():
    # Наприклад: /api/compare/balance?cpu=1&gpu=2
    cpu_id = request.args.get('cpu', type=int)
    gpu_id = request.args.get('gpu', type=int)
    
    analysis = comparison_controller.compare_cpu_gpu_balance(cpu_id, gpu_id)
    return jsonify({"balance_analysis": analysis})

@app.route('/api/compare/components', methods=['GET'])
def compare_items():
    # Наприклад: /api/compare/components?type=cpu&id1=1&id2=2
    comp_type = request.args.get('type', default='cpu', type=str)
    id1 = request.args.get('id1', type=int)
    id2 = request.args.get('id2', type=int)
    
    advantages = comparison_controller.compare_components(comp_type, id1, id2)
    return jsonify({"advantages": advantages})

# ==========================================
# МАРШРУТИ ДЛЯ АНАЛІТИКИ РИНКУ
# ==========================================
@app.route('/api/market/history', methods=['GET'])
def price_history():
    # Наприклад: /api/market/history?type=gpu&id=1
    comp_type = request.args.get('type', default='gpu', type=str)
    comp_id = request.args.get('id', default=1, type=int)
    
    history = market_controller.get_price_history(comp_type, comp_id)
    return jsonify([dataclasses.asdict(h) for h in history])

@app.route('/api/market/trend', methods=['GET'])
def price_trend():
    comp_type = request.args.get('type', default='gpu', type=str)
    comp_id = request.args.get('id', default=1, type=int)
    
    verdict = market_controller.check_price_trend(comp_type, comp_id)
    return jsonify({"trend_analysis": verdict})

@app.route('/api/market/stores', methods=['GET'])
def store_links():
    comp_type = request.args.get('type', default='gpu', type=str)
    comp_id = request.args.get('id', default=1, type=int)
    
    links = market_controller.get_external_store_links(comp_type, comp_id)
    return jsonify([dataclasses.asdict(l) for l in links])

# ==========================================
# МАРШРУТИ ДЛЯ ПРОФІЛЮ КОРИСТУВАЧА
# ==========================================
# ==========================================
# МАРШРУТИ ДЛЯ ПРОФІЛЮ КОРИСТУВАЧА
# ==========================================
@app.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    profile = profile_controller.get_my_profile(user_id)
    p_dict = dataclasses.asdict(profile)
    user = user_repo.get_by_id(user_id)
    p_dict['avatar_url'] = user.avatar_url if user and user.avatar_url else ""
    return jsonify(p_dict)

# === НОВИЙ МАРШРУТ: ЗАВАНТАЖЕННЯ ФОТО ===
@app.route('/api/profile/<int:user_id>/avatar', methods=['POST'])
def upload_avatar(user_id):
    if 'avatar' not in request.files:
        return jsonify({"error": "Немає файлу"}), 400
        
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({"error": "Файл не обрано"}), 400
        
    if file:
        filename = f"user_{user_id}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        user = user_repo.get_by_id(user_id)
        if user:
            user.avatar_url = f"/{filepath}" 
            user_repo.update()
            return jsonify({"success": True, "avatar_url": user.avatar_url})
            
    return jsonify({"error": "Помилка завантаження"}), 500

@app.route('/api/profile/<int:user_id>', methods=['PUT'])
def edit_profile(user_id):
    data = request.get_json()
    req_model = ProfileUpdateRequestViewModel(
        username=data.get('username'),
        email=data.get('email')
    )
    updated_profile = profile_controller.update_profile(user_id, req_model)
    return jsonify(dataclasses.asdict(updated_profile))

# === НОВИЙ МАРШРУТ: ВИДАЛЕННЯ АКАУНТА ===
@app.route('/api/profile/<int:user_id>', methods=['DELETE'])
def delete_profile_route(user_id):
    user = user_repo.get_by_id(user_id)
    if user:
        # Видаляємо користувача (а всі його збережені збірки видаляться автоматично завдяки cascade="all, delete-orphan")
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": True, "message": "Акаунт видалено"}), 200
    return jsonify({"error": "Акаунт не знайдено"}), 404

@app.route('/api/profile/<int:user_id>/password', methods=['POST'])
def change_pass(user_id):
    data = request.get_json()
    req_model = PasswordChangeRequestViewModel(
        old_password=data.get('old_password', ''),
        new_password=data.get('new_password', '')
    )
    success = profile_controller.change_password(user_id, req_model)
    return jsonify({"success": success})

@app.route('/api/profile/<int:user_id>/favorites', methods=['POST'])
def add_favorite_build(user_id):
    data = request.get_json()
    
    # ФУНКЦІЯ-РЯТІВНИК: перетворює порожні значення на None, щоб БД не видавала помилку!
    def get_fk(key):
        val = data.get(key)
        return None if not val else val

    req_model = SaveBuildRequestViewModel(
        build_name=data.get('build_name', 'Моя нова збірка'),
        cpu_id=get_fk('cpu_id'), gpu_id=get_fk('gpu_id'), motherboard_id=get_fk('motherboard_id'),
        ram_id=get_fk('ram_id'), storage_id=get_fk('storage_id'), psu_id=get_fk('psu_id'),
        cooler_id=get_fk('cooler_id'), case_id=get_fk('case_id'), mouse_id=get_fk('mouse_id'),
        keyboard_id=get_fk('keyboard_id'), headset_id=get_fk('headset_id')
    )
    success = profile_controller.save_build_to_favorites(user_id, req_model)
    return jsonify({"success": success})

@app.route('/api/profile/<int:user_id>/favorites/<int:build_id>', methods=['PUT'])
def rename_favorite_build(user_id, build_id):
    data = request.get_json()
    new_name = data.get('build_name')
    success = profile_controller.rename_saved_build(user_id, build_id, new_name)
    return jsonify({"success": success})

@app.route('/api/profile/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    builds = profile_controller.get_my_saved_builds(user_id)
    # ВИПРАВЛЕНО: builds - це ВЖЕ список словників (dict), 
    # тому dataclasses.asdict() тут більше не потрібен!
    return jsonify(builds)

# ==========================================
# МАРШРУТИ ДЛЯ АВТОРИЗАЦІЇ (AUTH)
# ==========================================
@app.route('/api/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    # Використовуємо поле password_hash з ViewModel для передачі сирого пароля 
    # (сервіс сам його захешує)
    req_model = UserAuthRequestViewModel(
        email=data.get('email'),
        password_hash=data.get('password') 
    )
    
    try:
        profile = auth_controller.register(req_model)
        import dataclasses
        return jsonify({"message": "Успішна реєстрація", "user": dataclasses.asdict(profile)}), 201
    except ValueError as e:
        # Якщо такий email вже є, повертаємо помилку 400 (Bad Request)
        return jsonify({"error": str(e)}), 400

@app.route('/api/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    
    req_model = UserAuthRequestViewModel(
        email=data.get('email'),
        password_hash=data.get('password')
    )
    
    token = auth_controller.login(req_model)
    if token:
        return jsonify({"message": "Успішний вхід", "access_token": token}), 200
    else:
        return jsonify({"error": "Невірний email або пароль"}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout_user():
    # Зазвичай токен передається в заголовках (Headers: Authorization)
    token = request.headers.get('Authorization')
    success = auth_controller.logout(token)
    return jsonify({"success": success})


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
