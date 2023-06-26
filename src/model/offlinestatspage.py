from dataclasses import dataclass
from datetime import datetime

@dataclass
class OfflineStatsPage:
    userid: int
    username: str
    rank: int
    tff: int
    commander_id: int
    commandchain_top_id: int
    officers: list[int]
    user_last_online: datetime