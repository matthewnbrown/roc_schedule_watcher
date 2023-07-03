from src.offlinestatpageparser import OfflineStatsPage

from collections import defaultdict
import csv
from datetime import datetime
from logging import Logger
import os


class PlayerLogSaver:
    FORMAT_OPTIONS = ['timestamp', 'online', 'username', 'rank',
                      'allianceid', 'tff', 'tfftype', 'commanderid',
                      'topofchainid', 'officers']

    FORMAT_TO_ENCODEDVALUE_MAP = defaultdict(lambda: 'xx', {
        'timestamp': 'ts',
        'online': 'os',
        'username': 'un',
        'rank': 'rk',
        'allianceid': 'ai',
        'tff': 'tf',
        'tfftype': 'tt',
        'commanderid': 'ci',
        'topofchainid': 'tc',
        'officers': 'of'
    })

    VERSION_NUMBER = 'V2'

    def __init__(self, logger: Logger,
                 save_path_base: str,
                 formatoptions: list[str]) -> None:
        self._logger = logger
        self._savepathbase = save_path_base
        self._formatoptions = formatoptions

    def save_log(
            self, userId: str,
            timestamp: datetime,
            page: OfflineStatsPage) -> None:
        filepath = os.path.join(
            self._savepathbase, f'{userId}-{self.VERSION_NUMBER}.csv')
        if not os.path.exists(filepath):
            self._logger.info('Creating logfile for userid %s', userId)

        formatted_csv_input = self._get_formatted_csv_input(
            timestamp, page, self._formatoptions)

        with open(filepath, 'a+', newline='', encoding='utf-8') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(formatted_csv_input)

    def _get_formatted_csv_input(
            self,
            timestamp: datetime,
            page: OfflineStatsPage,
            format: list[str]) -> list[str]:

        allianceid = -1 if page.alliance_id.is_none else page.alliance_id.value
        commanderid = -1 if page.commander_id.is_none \
            else page.commander_id.value
        commandertopid = -1 if page.commandchain_top_id.is_none \
            else page.commandchain_top_id.value
        onlinestatus = 'online' if page.is_online else 'offline'

        value_map = defaultdict(lambda: 'unknown format option')
        value_map.update({
                'timestamp': timestamp,
                'online': onlinestatus,
                'username': page.username,
                'rank': page.rank,
                'allianceid': allianceid,
                'tff': page.tff,
                'tfftype': page.tff_type,
                'commanderid': commanderid,
                'topofchainid': commandertopid,
                'officers': page.officers
        })
        form = [PlayerLogSaver.FORMAT_TO_ENCODEDVALUE_MAP[x] for x in format]
        formatinfo = ''.join(form)
        return [formatinfo] + [value_map[x] for x in format]
