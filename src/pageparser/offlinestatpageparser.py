from src.model.offlinestatspage import OfflineStatsPage

from bs4 import BeautifulSoup
from option import Result

class OfflineStatPageParser:
    def __init__(self, parser: str = 'lxml') -> None:
        self._parser = parser


    def parse_offlinestat_page(self, html: str) -> Result[OfflineStatsPage, str]:
        soup = BeautifulSoup(html, self._parser)
        content = soup.find('div', {'id': 'content'})
        
        if content is None or soup.title is None:
            return Result.Err("Error parsing html")
        
        return OfflineStatPageParser._extract_pagemodel_from_content(content)
    
    [staticmethod]
    def _extract_pagemodel_from_content(contentsoup: BeautifulSoup) -> Result[OfflineStatsPage, str]:
        return Result.Err("ooof")