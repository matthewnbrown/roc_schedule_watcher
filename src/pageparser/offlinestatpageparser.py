from src.model.offlinestatspage import OfflineStatsPage

from bs4 import BeautifulSoup
from datetime import datetime
from option import Result, Option

class OfflineStatPageParser:
    def __init__(self, parser: str = 'lxml') -> None:
        self._parser = parser


    def parse_offlinestat_page(self, html: str) -> Result[OfflineStatsPage, str]:
        soup = BeautifulSoup(html, self._parser)
        content = soup.find('div', {'id': 'content'})
        
        if content is None or soup.title is None:
            return Result.Err("Error parsing html")
        
        if "Stats for" not in soup.title.text:
            return Result.Err(f"Page has unexpected title {soup.title.text}")
        
        return OfflineStatPageParser._extract_pagemodel_from_content(content)
    
    [staticmethod]
    def _extract_pagemodel_from_content(contentsoup: BeautifulSoup) -> Result[OfflineStatsPage, str]:
        is_online = contentsoup.find('div', {"class": "playercard_name oindicator"}) is not None
        
        playerstats = OfflineStatPageParser._extract_playerstats(contentsoup)
        
        if playerstats.is_err:
            return Result.Err(playerstats.Err())
        
        rank, alliance, tff, tff_type = playerstats.Ok()
        if is_online:
            last_online = datetime.now()
        else:
            pass
        return Result.Ok(
            OfflineStatsPage(
                user_id, user_name, rank, alliance, tff, tff_type, commander_id, commanderchain_top_id, officers, last_online))
    
    [staticmethod]
    def _extract_playerstats(contentsoup: BeautifulSoup) -> Result[tuple(int, Option(int), str, str), str]:
        statssoup = contentsoup.find('div', {"class": "playercard_stats"})
        rank = int(statssoup.find("div", {"class": "playercard_rank"}).text[1:])
        tff, tff_type = statssoup.find("div", {"class": "playercard_size"}).text.split(' ')
        tff = int(tff.replace(',', ''))
        
        alliancesoup = statssoup.find("div", {"class": "playercard_alliance"})
        alliancelinksoup = alliancesoup.find("a")
        
        if alliancelinksoup is None:
            alliance = Option.NONE()
        else:
            alliancelink = alliancelinksoup.get("href")
            allianceid = int(alliancelink.split("?a=")[1])
            alliance = Option.Some(allianceid)
        
        return Result.Ok(rank, alliance, tff, tff_type)
        
    [staticmethod]
    def _extract_playercommandchain(contentsoup: BeautifulSoup) -> Result(tuple(Option(int), Option(int), list[int])):
        
        commandsoup = contentsoup.find("div", {"class": "playercard_commandchain"})
        top = commandsoup.find("div", {"class": "playercard_topofchain"})
        if top is None:
            topid = Option.NONE()
        else:
            tophref = top.find("a").get("href")
            top_idval = int(tophref.split("?a=")[1])
            topid = Option.Some(top_idval)
        
        commandersoup = commandsoup.find("div", {"class": "playercard_commander"})
        
        if commandersoup is not None:
            commander_id = Option.NONE()
        else:
            commanderhref = commandersoup.find("a").get("href")
            commanderid_val = int(commanderhref.split("?a=")[1])
            commander_id = Option.Some(commanderid_val)
        
        officersoup = commandsoup.find("div", {"class": "players"})
        
        if officersoup is None:
            officers = []
        else:
            officers_soup = officersoup.find_all("li", {"class": "player_cell"})
            officers = [int(x.get("id").split('_')[1]) for x in officers_soup]
            
        return Result.Ok(tuple(topid, commander_id, officers))