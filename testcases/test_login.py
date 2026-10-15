"""登录模块接口用例（数据驱动）。"""
import allure
import pytest
from pathlib import Path

from api.login_api import LoginApi
from common.yaml_util import read_yaml

login_data = read_yaml(Path(__file__).parent.parent / "data" / "login_data.yaml")


@allure.epic("后台管理平台")
@allure.feature("登录模块")
class TestLogin:

    @allure.story("登录接口-正常/异常/边界")
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", login_data, ids=[c["case_name"] for c in login_data])
    def test_login(self, case):
        with allure.step(f"执行用例：{case['case_name']}"):
            resp = LoginApi().login(case["username"], case["password"])
            body = resp.json()

        with allure.step("校验业务码"):
            assert body["code"] == case["expect_code"], \
                f"期望 {case['expect_code']}，实际 {body['code']}，msg={body.get('msg')}"

        with allure.step("校验是否返回 token"):
            if case["expect_has_token"]:
                assert body.get("token"), "登录成功但未返回 token"
            else:
                assert not body.get("token"), "失败场景不应返回 token"
