"""用户管理模块接口用例：列表查询 + 新增->查询->删除闭环。"""
import time
import allure
import pytest

from api.user_api import UserApi


@allure.epic("后台管理平台")
@allure.feature("用户管理模块")
class TestUser:

    @allure.story("分页查询用户列表")
    @pytest.mark.smoke
    def test_user_list(self, login_token):
        """依赖 login_token fixture：先登录拿到 Token 再查询。"""
        with allure.step("查询第一页用户列表"):
            resp = UserApi().list(page_num=1, page_size=10)
            body = resp.json()

        with allure.step("校验业务码与返回结构"):
            assert body["code"] == 200, f"查询失败：{body}"
            assert "rows" in body and isinstance(body["rows"], list)
            assert "total" in body

    @allure.story("新增用户->查询校验->删除用户（数据闭环）")
    @pytest.mark.user
    def test_user_add_query_delete(self, login_token):
        api = UserApi()
        # 时间戳保证用户名/手机号唯一，避免重复数据冲突
        suffix = str(int(time.time()))[-8:]
        username = f"auto{suffix}"

        add_body = {
            "userName": username,
            "nickName": "自动化测试用户",
            "password": "test123456",
            "deptId": 100,
            "phonenumber": f"138{suffix}",
            "email": f"{username}@test.com",
            "sex": "0",
        }

        with allure.step(f"新增用户 {username}"):
            resp = api.add(add_body)
            assert resp.json()["code"] == 200, f"新增失败：{resp.text}"

        with allure.step("按用户名查询，确认写入成功并取出 userId"):
            resp = api.list(user_name=username)
            rows = resp.json()["rows"]
            assert rows, "新增后未查询到该用户"
            user_id = rows[0]["userId"]

        with allure.step(f"删除用户 userId={user_id}（清理测试数据）"):
            resp = api.delete(user_id)
            assert resp.json()["code"] == 200, f"删除失败：{resp.text}"

        with allure.step("再次查询，确认已删除"):
            resp = api.list(user_name=username)
            assert resp.json()["rows"] == [], "删除后仍能查到该用户"
