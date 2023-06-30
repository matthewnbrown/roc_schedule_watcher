from src.watchlistvalidator import WatchlistValidator
from src.offlinestatpageparser import OfflineStatPageParser
from src.watcher import Watcher
from src.playerlogsaver import PlayerLogSaver

import asyncio
import asyncclick as click
import logging

VALID_FORMAT_OPTIONS=[ 'timestamp', 'online', 'username', 'rank', 'allianceid', 'tff', 'tfftype', 'commanderid', 'topofchainid', 'officers' ]
class Config(object):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group(invoke_without_command=True)
@click.option('-v', '--verbose', is_flag=True)
@click.option('-f', '--watchidfile', default='watchlist.txt', type=click.File('r'), help='file to read ids from')
@click.option('-o', '--outdir', default='./watchlogs/', type=click.Path(writable=True, file_okay=False, exists=True), help='directory to place logs in.', show_default=True)
@click.option('-l', '--watchidlist', default='', type=str, help='overrides watchlist file. comma seperated list of ids i.e., 3102,231,33')
@click.option('-f', '--printformat', default='timestamp,online,username,rank,allianceid,tff,tfftype,commanderid,topofchainid,officers',
              type=str, show_default=True,
              help='comma seperated list order to print details')
@pass_config
async def cli(config: Config, verbose: bool, watchidfile: click.File, outdir: click.Path, watchidlist: str, printformat: str):

    loglevel = logging.DEBUG if verbose else logging.INFO

    config.logger.setLevel(loglevel)
    handler = logging.StreamHandler()
    handler.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    config.logger.addHandler(handler)

    if len(watchidlist) == 0:
        config.logger.debug('No watch id list given, reading file')
        with open(watchidfile) as f:
            ids = f.readlines()
            config.logger.debug('Read %s ids from file', len(ids))
    else:
        ids = watchidlist.split(',')

    if not is_watchlist_valid(config.logger, ids):
        return
    
    formatoptions = printformat.split(',')
    
    if any(x not in VALID_FORMAT_OPTIONS for x in formatoptions):
        config.logger.error('Invalid logger format options')
        
    pageparser = OfflineStatPageParser('lxml')
    playerlogsaver = PlayerLogSaver(config.logger, outdir)
    
    watcher = Watcher(config.logger, pageparser, playerlogsaver)
    await watcher.watch(ids, 30, 0)


def is_watchlist_valid(logger: logging.Logger, watchlist_ids: list[str]) -> bool:
    validator = WatchlistValidator(logger=logger)
    
    result = validator.is_list_valid(watchlist_ids)
    
    if result.is_some:
        print("Error validating user ids")
        for error in result.value:
            print(error)
        print("-----------------")
        
        return False
    return True
    

 

if __name__ == "__main__":
    asyncio.run(cli())