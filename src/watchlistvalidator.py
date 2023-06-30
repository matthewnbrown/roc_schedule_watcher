from logging import Logger
from option import Option


class WatchlistValidator:
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def is_list_valid(self, idlist: list[str]) -> Option[list[str]]:
        self._logger.debug("validating watchlist ids")
        
        if idlist is None:
            return Option.Some(["Id list cannot be nothing"])
        if type(idlist) != list:
            return Option.Some(["Id list must be a list"])
        if len(idlist) == 0:
            return Option.Some(["Id list must contain elements"])
        
        errors = []
        for id in idlist:
            res = self._is_id_valid(id)
            
            if res.is_some:
                errors.append(res.value)

        if any(errors):
            return Option.Some(errors)
        
        return Option.NONE()
            
    def _is_id_valid(self, id: str) -> Option[str]:
        try:
            int(id)
        except ValueError:
            self._logger.debug("%s was invalid", id)
            return Option.Some(f'User ID "{id}" not in valid format')
        return Option.NONE()