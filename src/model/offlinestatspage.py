from dataclasses import dataclass
from datetime import datetime
from option import Option

@dataclass
class OfflineStatsPage:
    username: str
    rank: int
    alliance_id: Option[int]
    tff: int
    tff_type: str
    commander_id: Option[int]
    commandchain_top_id: Option[int]
    officers: list[int]
    is_online: bool