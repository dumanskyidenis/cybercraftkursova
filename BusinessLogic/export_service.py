import os
import uuid
from fpdf import FPDF
from Domain.ViewModels.pc_viewmodels import ShareableLinkViewModel

from Repositories.saved_build_repository import SavedBuildRepository
from Repositories.hardware_repository import (
    CpuRepository, GpuRepository, MotherboardRepository, RamRepository,
    StorageRepository, PsuRepository, MouseRepository, KeyboardRepository, HeadsetRepository
)

class ExportService:
    def __init__(self, build_repo: SavedBuildRepository, cpu_repo: CpuRepository, 
                 gpu_repo: GpuRepository, mb_repo: MotherboardRepository, 
                 ram_repo: RamRepository, storage_repo: StorageRepository, 
                 psu_repo: PsuRepository, mouse_repo: MouseRepository, 
                 keyboard_repo: KeyboardRepository, headset_repo: HeadsetRepository):
        self.build_repo = build_repo
        self.cpu_repo = cpu_repo
        self.gpu_repo = gpu_repo
        self.mb_repo = mb_repo
        self.ram_repo = ram_repo
        self.storage_repo = storage_repo
        self.psu_repo = psu_repo
        self.mouse_repo = mouse_repo
        self.keyboard_repo = keyboard_repo
        self.headset_repo = headset_repo

    # ФУНКЦІЯ-РЯТІВНИК: Транслітерація кирилиці в латиницю для FPDF
    def _safe_str(self, text):
        if not text: return "N/A"
        text = str(text)
        
        # Словник для заміни українських/російських літер на англійські
        cyrillic_to_latin = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye',
            'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l',
            'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'yu',
            'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E',
            'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K',
            'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
            'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '',
            'Ю': 'Yu', 'Я': 'Ya', 'ы': 'y', 'э': 'e', 'ъ': ''
        }
        
        res = ""
        for char in text:
            res += cyrillic_to_latin.get(char, char)
            
        # Видаляємо всі інші символи, які FPDF все одно не зрозуміє (наприклад, емодзі)
        return res.encode('latin-1', 'ignore').decode('latin-1')

    def generate_pdf_specification(self, build_id: int) -> str:
        export_dir = "static/exports"
        os.makedirs(export_dir, exist_ok=True)
        file_path = f"{export_dir}/build_{build_id}_full_spec.pdf"

        build = self.build_repo.get_by_id(build_id)
        if not build:
            raise ValueError("Збірку не знайдено в базі даних")

        cpu = self.cpu_repo.get_by_id(build.cpu_id) if build.cpu_id else None
        gpu = self.gpu_repo.get_by_id(build.gpu_id) if build.gpu_id else None
        mb = self.mb_repo.get_by_id(build.motherboard_id) if build.motherboard_id else None
        ram = self.ram_repo.get_by_id(build.ram_id) if build.ram_id else None
        st = self.storage_repo.get_by_id(build.storage_id) if build.storage_id else None
        psu = self.psu_repo.get_by_id(build.psu_id) if build.psu_id else None
        ms = self.mouse_repo.get_by_id(build.mouse_id) if build.mouse_id else None
        kb = self.keyboard_repo.get_by_id(build.keyboard_id) if build.keyboard_id else None
        hs = self.headset_repo.get_by_id(build.headset_id) if build.headset_id else None

        components = [
            ("Processor (CPU)", f"{cpu.brand} {cpu.model}" if cpu else "Not selected", f"{cpu.price if cpu else 0}"),
            ("Graphics (GPU)", f"{gpu.brand} {gpu.model}" if gpu else "Not selected", f"{gpu.price if gpu else 0}"),
            ("Motherboard", f"{mb.brand} {mb.model}" if mb else "Not selected", f"{mb.price if mb else 0}"),
            ("Memory (RAM)", f"{ram.brand} {ram.model}" if ram else "Not selected", f"{ram.price if ram else 0}"),
            ("Storage", f"{st.brand} {st.model}" if st else "Not selected", f"{st.price if st else 0}"),
            ("Power Supply", f"{psu.brand} {psu.model}" if psu else "Not selected", f"{psu.price if psu else 0}"),
            ("Mouse", f"{ms.brand} {ms.model}" if ms else "Not selected", f"{ms.price if ms else 0}"),
            ("Keyboard", f"{kb.brand} {kb.model}" if kb else "Not selected", f"{kb.price if kb else 0}"),
            ("Headset", f"{hs.brand} {hs.model}" if hs else "Not selected", f"{hs.price if hs else 0}")
        ]

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        
        # ВИПРАВЛЕННЯ: Очищаємо назву збірки перед записом
        safe_title = self._safe_str(build.build_name)
        pdf.cell(190, 10, txt=f"Full PC Build Specification (Name: {safe_title})", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Helvetica", 'B', 11)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(45, 10, "Category", border=1, fill=True)
        pdf.cell(105, 10, "Model Name", border=1, fill=True)
        pdf.cell(40, 10, "Price (UAH)", border=1, fill=True)
        pdf.ln()

        pdf.set_font("Helvetica", size=10)
        total_price = 0

        for category, model, price in components:
            pdf.cell(45, 10, category, border=1)
            # ВИПРАВЛЕННЯ: Очищаємо назви деталей (на випадок, якщо там затесалася кирилиця)
            pdf.cell(105, 10, self._safe_str(model), border=1)
            pdf.cell(40, 10, str(price), border=1)
            pdf.ln()
            total_price += float(price)

        pdf.ln(5)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(190, 10, txt=f"GRAND TOTAL: {total_price} UAH", ln=True, align='R')

        pdf.output(file_path)
        return f"/{file_path}"

    def generate_reddit_markdown(self, build_id: int) -> str:
        build = self.build_repo.get_by_id(build_id)
        if not build: return "Build not found."
        
        cpu = self.cpu_repo.get_by_id(build.cpu_id) if build.cpu_id else None
        gpu = self.gpu_repo.get_by_id(build.gpu_id) if build.gpu_id else None
        ram = self.ram_repo.get_by_id(build.ram_id) if build.ram_id else None
        
        markdown = f"### My Setup: {build.build_name}\n\n"
        markdown += "| Category | Component |\n|---|---|\n"
        markdown += f"| **CPU** | {cpu.brand if cpu else ''} {cpu.model if cpu else 'N/A'} |\n"
        markdown += f"| **GPU** | {gpu.brand if gpu else ''} {gpu.model if gpu else 'N/A'} |\n"
        markdown += f"| **RAM** | {ram.brand if ram else ''} {ram.model if ram else 'N/A'} |\n"
        return markdown

    def create_shareable_shortlink(self, build_id: int) -> ShareableLinkViewModel:
        share_url = f"https://cybercraft-app.onrender.com/?build={build_id}"
        return ShareableLinkViewModel(short_url=share_url, expires_in_days=30)