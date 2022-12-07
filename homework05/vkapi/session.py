import typing as tp

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.http_req_sess = requests.Session()
        retry_strategy = Retry(
            backoff_factor=backoff_factor,
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        self.adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http_req_sess.mount("https://", self.adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        if "timeout" not in kwargs.keys():
            timeout = self.timeout
        else:
            timeout = kwargs.pop("timeout")
        r = self.http_req_sess.get(url=f"{self.base_url}/{url}", params=kwargs, timeout=timeout)
        return r

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        if "timeout" not in kwargs.keys():
            timeout = self.timeout
        else:
            timeout = kwargs.pop("timeout")
        return self.http_req_sess.post(url=f"{self.base_url}/{url}", **kwargs, timeout=timeout)


if __name__ == "__main__":
    s = Session(base_url="https://httpbin.org", timeout=3)
    r = s.get("get")
    r = s.get("delay/2")
    r = s.get("delay/2", timeout=1)
    ...
