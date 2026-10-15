"""pytest 全局 fixture：统一管理登录态（整个测试会话只登录一次）。"""
import pytest
from common.request_util import request_util
from common.yaml_util import Config
from api.login_api import LoginApi


@pytest.fixture(scope="session")
def login_token():
    """会话级：所有需要登录的用例共用同一个 Token，避免重复登录。"""
    cfg = Config.get()
    resp = LoginApi().login(cfg["username"], cfg["password"])
    body = resp.json()
    token = body.get("token")
    assert token, f"登录失败，未获取到 token，响应：{resp.text}"
    request_util.set_token(token)  # 注入到后续所有请求头
    yield token
    request_util.clear_token()    # 用例结束清理
