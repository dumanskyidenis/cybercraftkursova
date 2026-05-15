from Domain.ViewModels.pc_viewmodels import ShareableLinkViewModel
from BusinessLogic.export_service import ExportService

class ExportController:
    # === DEPENDENCY INJECTION ===
    def __init__(self, export_service: ExportService):
        # Контролер отримує готовий сервіс і зберігає його
        self._export_service = export_service

    def generate_pdf_specification(self, build_id: int) -> str:
        """Генерує PDF-документ з таблицею деталей, цінами та графіками продуктивності (повертає шлях до файлу)"""
        return self._export_service.generate_pdf_specification(build_id)

    def generate_reddit_markdown(self, build_id: int) -> str:
        """Створює відформатований текст (Markdown) для швидкої публікації збірки на форумах (напр. Reddit)"""
        return self._export_service.generate_reddit_markdown(build_id)

    def create_shareable_shortlink(self, build_id: int) -> ShareableLinkViewModel:
        """Генерує коротке посилання (унікальний хеш) для того, щоб поділитися своєю конфігурацією з друзями"""
        return self._export_service.create_shareable_shortlink(build_id)