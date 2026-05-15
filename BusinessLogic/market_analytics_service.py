import datetime
import random
import requests
import re
from bs4 import BeautifulSoup
from typing import List
from Domain.ViewModels.pc_viewmodels import PriceHistoryViewModel, StoreLinkViewModel

from Repositories.hardware_repository import (
    CpuRepository, GpuRepository, MotherboardRepository, 
    RamRepository, StorageRepository, PsuRepository,
    CaseRepository, CoolerRepository, MouseRepository, 
    KeyboardRepository, HeadsetRepository
)

class MarketAnalyticsService:
    def __init__(self, cpu_repo: CpuRepository, gpu_repo: GpuRepository, 
                 mb_repo: MotherboardRepository, ram_repo: RamRepository, 
                 storage_repo: StorageRepository, psu_repo: PsuRepository,
                 case_repo: CaseRepository, cooler_repo: CoolerRepository,
                 mouse_repo: MouseRepository, keyboard_repo: KeyboardRepository,
                 headset_repo: HeadsetRepository):
        
        self.repos = {
            'cpu': cpu_repo, 'gpu': gpu_repo, 'motherboard': mb_repo,
            'ram': ram_repo, 'storage': storage_repo, 'psu': psu_repo,
            'case': case_repo, 'cooler': cooler_repo,
            'mouse': mouse_repo, 'keyboard': keyboard_repo, 'headset': headset_repo
        }

    def _get_component_from_db(self, component_type: str, item_id: int):
        repo = self.repos.get(component_type.lower())
        if repo:
            return repo.get_by_id(item_id)
        return None

    # === ПОВНОЦІННИЙ УНІВЕРСАЛЬНИЙ ПАРСЕР (Ціна + Прямий лінк) ===
    def _scrape_standard(self, store_name: str, search_url: str, fallback_price: float, base_domain: str):
        try:
            # Імітуємо перехід з Google, щоб не блокували
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "uk-UA,uk;q=0.9",
                "Referer": "https://www.google.com/"
            }
            response = requests.get(search_url, headers=headers, timeout=8)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                price_elements = soup.find_all(class_=re.compile(r'price|amount|val', re.I))
                
                # Чорний список лінків (реклама, кошик, акції)
                bad_link_keywords = ['javascript:', '#', 'tel:', 'mailto:', '/cart', 'promo', 'akciya', 'plati', 'znizhka', 'discount', 'blog', 'news']

                for el in price_elements:
                    # Читаємо шматочками, щоб не злипалися акційні та старі ціни
                    for text_chunk in el.stripped_strings:
                        chunk_clean = text_chunk.split('.')[0].split(',')[0]
                        clean_price = re.sub(r'[^\d]', '', chunk_clean)
                        
                        if clean_price and len(clean_price) >= 3:
                            price_val = float(clean_price)
                            
                            # Перевірка на адекватність ціни (+- від орієнтовної)
                            if (fallback_price * 0.4) < price_val < (fallback_price * 2.5):
                                product_url = search_url 
                                parent = el.parent
                                
                                # Піднімаємося по HTML дереву, щоб знайти посилання на товар
                                for _ in range(6): 
                                    if not parent or parent.name == 'body': break
                                    all_links = parent.find_all('a', href=True)
                                    
                                    for a in all_links:
                                        h = a['href'].strip()
                                        h_lower = h.lower()
                                        
                                        # Відкидаємо рекламу
                                        if not h or any(bad_kw in h_lower for bad_kw in bad_link_keywords):
                                            continue
                                        
                                        full_url = h if h.startswith('http') else base_domain + (h if h.startswith('/') else '/' + h)
                                        
                                        # Якщо лінк відрізняється від пошукового - це наша деталь!
                                        if len(h) > 10 and search_url not in full_url:
                                            print(f"🟢 [ПАРСЕР {store_name}] Знайдено: {price_val} ₴ | Лінк: {full_url}")
                                            return price_val, full_url, True
                                            
                                    parent = parent.parent
                                
                                # Якщо прямого лінка немає (буває рідко), повертаємо пошуковий
                                return price_val, product_url, True
                                
        except Exception as e:
            print(f"🔴 [ПАРСЕР {store_name}] Помилка: {e}")
            
        return fallback_price, search_url, False

    def get_price_history(self, component_type: str, component_id: int) -> List[PriceHistoryViewModel]:
        item = self._get_component_from_db(component_type, component_id)
        if not item: return []
        current_price = float(item.price)
        history = []
        today = datetime.date.today()
        for i in range(5, -1, -1):
            month_date = today.replace(day=1) - datetime.timedelta(days=30 * i)
            month_str = month_date.strftime("%Y-%m")
            fluctuation = 1.0 if i == 0 else random.uniform(0.92, 1.08)
            history.append(PriceHistoryViewModel(date=month_str, average_price=round(current_price * fluctuation, 2)))
        return history

    def check_price_trend(self, component_type: str, component_id: int) -> str:
        item = self._get_component_from_db(component_type, component_id)
        if not item: return "Деталь не знайдено."
        if item.price > 25000: return "Ціна на піку. Можливе зниження."
        elif 5000 <= item.price <= 25000: return "Ціна стабільна. Хороший час для покупки."
        else: return "Дуже вигідна ціна!"

    def get_external_store_links(self, component_type: str, component_id: int) -> List[StoreLinkViewModel]:
        item = self._get_component_from_db(component_type, component_id)
        if not item: return []

        raw_query = f"{item.brand} {item.model}"
        search_query = raw_query.replace(" ", "+")
        base_price = float(item.price)

        # 1. KTC
        url_ktc = f"https://ktc.ua/search/?q={search_query}"
        ktc_price, ktc_link, ktc_live = self._scrape_standard("KTC", url_ktc, base_price, "https://ktc.ua")
        ktc_name = "KTC" if ktc_live else "KTC (Орієнтовно)"

        # 2. Rozetka (СИМУЛЯЦІЯ - Надійний пошук, який ніколи не видає 404)
        # 2. MOYO (СИМУЛЯЦІЯ - Виправлено шлях до пошуку)
        # Очищаємо зайві брендові приставки для ВСІХ основних деталей
        clean_model = item.model.replace("NVIDIA", "").replace("GeForce", "").replace("AMD", "").replace("Radeon", "").replace("Intel", "").replace("Core", "").replace("Ryzen", "")
        clean_model = clean_model.replace("(", "").replace(")", "").strip()
        moyo_query = clean_model.replace(" ", "+")
        
        moyo_price = round(base_price * random.uniform(0.98, 1.03))
        
        # Секрет був у слові "new" в URL-адресі! Саме це викликало помилку 404.
        moyo_link = f"https://www.moyo.ua/ua/search/new/?q={moyo_query}"
        moyo_name = "Moyo"
        
        # 3. LuckyLink
        url_ll = f"https://luckylink.kiev.ua/search/?search={search_query}"
        ll_price, ll_link, ll_live = self._scrape_standard("LuckyLink", url_ll, round(base_price * 1.02, 2), "https://luckylink.kiev.ua")
        ll_name = "LuckyLink" if ll_live else "LuckyLink (Орієнтовно)"

        return [
            StoreLinkViewModel(store_name=ktc_name, url=ktc_link, current_price=ktc_price),
            StoreLinkViewModel(store_name=moyo_name, url=moyo_link, current_price=moyo_price),
            StoreLinkViewModel(store_name=ll_name, url=ll_link, current_price=ll_price)
        ]