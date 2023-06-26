from dataclasses import dataclass
from datetime import datetime
from option import Option

@dataclass
class OfflineStatsPage:
    userid: int
    username: str
    rank: int
    alliance_id: Option[int]
    tff: int
    tff_type: str
    commander_id: Option[int]
    commandchain_top_id: Option[int]
    officers: list[int]
    user_last_online: datetime