from src.watchlistvalidator import WatchlistValidator
from src.offlinestatpageparser import OfflineStatPageParser
from src.watcher import Watcher
from src.playerlogsaver import PlayerLogSaver
from src.urlgenerator import ROCDecryptUrlGenerator

import asyncio
import asyncclick as click
import logging


class Config(object):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(invoke_without_command=True)
@click.option('-v', '--verbose', is_flag=True)
@click.option('-f', '--watchidfile', default='watchlist.txt',
              type=click.File('r'), help='file to read ids from')
@click.option('-o', '--outdir', default='./watchlogs/',
              type=click.Path(writable=True, file_okay=False, exists=True),
              help='directory to place logs in.', show_default=True)
@click.option('-l', '--watchidlist', default='', type=str,
              help='overrides watchlist file.'
              + ' comma seperated list of ids i.e., 3102,231,33')
@click.option('-f', '--printformat',
              default='timestamp,online,username,rank,allianceid,'
              + 'tff,tfftype,commanderid,topofchainid,officers',
              type=str, show_default=True,
              help='comma seperated list order to print details')
@click.option('-d', '--delay-time', type=click.FloatRange(0, None),
              default='30', show_default=True,
              help='time to wait before each lookup (seconds)')
@pass_config
async def cli(config: Config, verbose: bool, watchidfile: click.File,
              outdir: click.Path, watchidlist: str, printformat: str,
              delay_time: float):

    loglevel = logging.DEBUG if verbose else logging.INFO

    config.logger.setLevel(loglevel)
    handler = logging.StreamHandler()
    handler.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    config.logger.addHandler(handler)

    if len(watchidlist) == 0:
        config.logger.debug('No watch id list given, reading file')
        ids = watchidfile.read().splitlines()
        config.logger.debug('Read %s ids from file', len(ids))
    else:
        ids = watchidlist.split(',')

    if not is_watchlist_valid(config.logger, ids):
        return

    config.logger.debug('watchlist ids: %s', ids)
    formatoptions = printformat.lower().split(',')

    if any(x not in PlayerLogSaver.FORMAT_OPTIONS for x in formatoptions):
        config.logger.error('Invalid logger format options')
        return

    pageparser = OfflineStatPageParser('lxml')
    playerlogsaver = PlayerLogSaver(config.logger, outdir, formatoptions)
    urlgen = ROCDecryptUrlGenerator()

    watcher = Watcher(config.logger, pageparser, playerlogsaver, urlgen)
    await watcher.watch(ids, delay_time, 0)


def is_watchlist_valid(
        logger: logging.Logger, watchlist_ids: list[str]) -> bool:
    validator = WatchlistValidator(logger=logger)

    result = validator.is_list_valid(watchlist_ids)

    if result.is_some:
        logger.error("Error validating user ids")
        for error in result.value:
            logger.error(error)

        return False
    return True


if __name__ == "__main__":
    asyncio.run(cli())
