from typing import List
from Domain.ViewModels.pc_viewmodels import PriceHistoryViewModel, StoreLinkViewModel
from BusinessLogic.market_analytics_service import MarketAnalyticsService

class MarketAnalyticsController:
    # === DEPENDENCY INJECTION ===
    def __init__(self, market_service: MarketAnalyticsService):
        self._market_service = market_service

    def get_price_history(self, component_type: str, component_id: int) -> List[PriceHistoryViewModel]:
        """Повертає масив даних для побудови графіка зміни ціни за останні 6 місяців"""
        return self._market_service.get_price_history(component_type, component_id)

    def check_price_trend(self, component_type: str, component_id: int) -> str:
        """Аналізує ринок і видає вердикт щодо покупки"""
        return self._market_service.check_price_trend(component_type, component_id)

    def get_external_store_links(self, component_type: str, component_id: int) -> List[StoreLinkViewModel]:
        """Парсить актуальні ціни та видає посилання на магазини"""
        return self._market_service.get_external_store_links(component_type, component_id)