import abc
import base64


class URLNotFoundError(Exception):
    pass

class ROCUrlGenerator(abc.ABC):
    @abc.abstractmethod
    def get_page_url(self, page: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_home() -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_armory() -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_training() -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_base() -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_recruit() -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_login() -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_keep() -> str:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_stats(self, id: str) -> str:
        raise NotImplementedError()


class ROCDecryptUrlGenerator(ROCUrlGenerator):
    def __init__(self) -> None:
        rocurlb64 = 'aHR0cHM6Ly9ydWluc29mY2hhb3MuY29tLw=='
        rocurlbytes = base64.b64decode(rocurlb64)
        self._rocburl = rocurlbytes.decode('ascii')

        self._urls = {
            'roc_home': self._rocburl,
            'roc_base': self._rocburl  + 'base.php',
            'roc_armory': self._rocburl + 'armory.php',
            'roc_login': self._rocburl + 'login.php',
            'roc_training': self._rocburl + 'train.php',
            'roc_recruit': self._rocburl + 'recruiter.php',
            'roc_keep': self._rocburl + 'keep.php'
        }

    def get_page_url(self, page: str) -> str:
        if page not in self._urls:
            raise URLNotFoundError(f'{page} url not known')
        return self._urls[page]

    def get_home(self) -> str:
        return self.get_page_url('roc_home')

    def get_armory(self) -> str:
        return self.get_page_url('roc_armory')

    def get_training(self) -> str:
        return self.get_page_url('roc_training')

    def get_base(self) -> str:
        return self.get_page_url('roc_home')

    def get_recruit(self) -> str:
        return self.get_page_url('roc_recruit')

    def get_login(self) -> str:
        return self.get_page_url('roc_login')

    def get_keep(self) -> str:
        return self.get_page_url('roc_keep')
    
    def get_stats(self, id: str) -> str:
        return self.get_page_url('roc_home') + f'stats.php?id={id}'