from src.offlinestatpageparser import OfflineStatsPage

import csv
from datetime import datetime
from logging import Logger
import os
from pathlib import Path

class PlayerLogSaver:
    def __init__(self, logger: Logger, save_path_base) -> None:
        self._logger = logger
        self._savepathbase = save_path_base
    
    def save_log(self, userId: str, timestamp: datetime, page: OfflineStatsPage ) -> None:
        filepath = os.path.join(self._savepathbase, f'{userId}.csv')
        if not os.path.exists(filepath):
            self._logger.debug('Creating logfile for userid %s', userId)
        
        with open(filepath, 'a+', newline='', encoding='utf-8') as f:    
            csvwriter = csv.writer(f)
            
            allianceid = -1 if page.alliance_id.is_none else page.alliance_id.value
            commanderid = -1 if page.commander_id.is_none else page.commander_id.value
            commandertopid = -1 if page.commandchain_top_id.is_none else page.commandchain_top_id.value
            onlinestatus = 'online' if page.is_online else 'offline'
            
            csvwriter.writerow([
                timestamp, onlinestatus,
                page.username, page.rank, allianceid, page.tff,
                page.tff_type, commanderid, commandertopid, 
                page.officers,])
        