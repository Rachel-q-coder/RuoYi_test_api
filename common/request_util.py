"""请求基类封装：统一 base_url、超时、Token 注入、请求/响应日志。"""
import requests
from common.log_util import get_logger
from common.yaml_util import Config

logger = get_logger()


class RequestUtil:
    def __init__(self):
        # 使用 Session 自动复用连接、Cookie
        self.session = requests.Session()
        self.base_url = Config.get()["base_url"]
        self.timeout = Config.get().get("timeout", 10)

    def set_token(self, token):
        """登录后把 Token 写入全局请求头（RuoYi 鉴权方式）。"""
        self.session.headers["Authorization"] = f"Bearer {token}"

    def clear_token(self):
        self.session.headers.pop("Authorization", None)

    def send(self, method, path, **kwargs):
        url = self.base_url + path
        kwargs.setdefault("timeout", self.timeout)
        # 打印请求日志（参数、json、headers）
        logger.info(f"--> {method.upper()} {url} | kwargs={kwargs}")
        resp = self.session.request(method, url, **kwargs)
        # 响应日志截断，避免超长刷屏
        logger.info(f"<-- {resp.status_code} | {resp.text[:500]}")
        return resp


# 全局单例，所有接口对象共用同一个 session（携带同一份 Token）
request_util = RequestUtil()
