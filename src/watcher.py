from src.offlinestatpageparser import OfflineStatPageParser, OfflineStatsPage
from src.playerlogsaver import PlayerLogSaver
from src.urlgenerator import ROCUrlGenerator

import asyncio
import aiohttp
from datetime import datetime
import humanfriendly as hf
from logging import Logger
from option import Result


class Watcher:
    def __init__(
            self, logger: Logger,
            pageparse: OfflineStatPageParser,
            logsaver: PlayerLogSaver,
            url_generator: ROCUrlGenerator
            ) -> None:
        self._logger = logger
        self._pageparser = pageparse
        self._logssaver = logsaver
        self._urlgenerator = url_generator
        self._lastonlinemap = {}

    async def watch(self, watchidlist: list[int],
                    delaytime_s: float,
                    iterations: int = 0):
        iter_count = 0

        while iterations <= 0 or iter_count < iterations:
            async with aiohttp.ClientSession() as session:
                self._logger.debug('Starting log iteration %i', iter_count)
                await asyncio.gather(*(self._perform_user_log(
                    session, id) for id in watchidlist))
            self._logger.debug('Finished log iteration')

            iter_count += 1
            self._logger.info('Sleeping for %s seconds'
                              + '\n-----------------------', delaytime_s)
            await asyncio.sleep(delaytime_s)

    async def _perform_user_log(self,
                                session: aiohttp.ClientSession,
                                userId: str) -> None:
        self._logger.debug('Starting user log for id %s', userId)
        try:
            await self.get_user_page(session, userId)
        except aiohttp.ClientConnectorError as e:
            self._logger.error('ClientConnectorError: %s', e)
        except Exception as e:
            self._logger.error("Unknown error: %s", e)

        self._logger.debug('Finished logging userid %s', userId)

    async def get_user_page(self,
                            session: aiohttp.ClientSession, id: str
                            ) -> Result[OfflineStatsPage, str]:
        url = self._urlgenerator.get_stats(id)

        async with session.get(url) as resp:
            self._logger.debug('Received response %s for id %s',
                               resp.status, id)

            if resp.status != 200:
                return Result.Err(f'Received response code {resp.status}')
            html = await resp.text("utf8")

            self._logger.debug('Reading file for id %s', id)
            timestamp = datetime.now()

            pageresult = self._pageparser.parse_offlinestat_page(html)
            if pageresult.is_err:
                self._logger.warning('Failed to lookup user ID %s: %s',
                                     id, pageresult.unwrap_err())
                return pageresult
            page = pageresult.unwrap()
            self._logssaver.save_log(id, timestamp, page)
            self._log_user(id, page, timestamp)
            return pageresult

    def _log_user(self,
                  userid: int,
                  page: OfflineStatsPage,
                  timestamp: datetime) -> None:
        if page.is_online:
            self._lastonlinemap[userid] = timestamp

        if page.is_online:
            onlinestatus = 'online'
        else:
            onlinestatus = self._get_useronlinestatus_str(userid, timestamp)
        self._logger.info('%s: %s', page.username, onlinestatus)

    def _get_useronlinestatus_str(
            self, userid: int, timestamp: datetime) -> str:
        if userid in self._lastonlinemap:
            laston = self._lastonlinemap[userid]
            time_since_online = hf.format_timespan(timestamp - laston) + ' ago'
        else:
            time_since_online = 'unknown'

        return f'last online: {time_since_online}'
