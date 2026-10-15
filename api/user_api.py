"""用户管理模块接口封装（增删改查）。"""
from common.request_util import request_util


class UserApi:
    BASE_PATH = "/system/user"

    def list(self, page_num=1, page_size=10, user_name=None):
        """分页查询用户列表，可按用户名模糊搜索。"""
        params = {"pageNum": page_num, "pageSize": page_size}
        if user_name:
            params["userName"] = user_name
        return request_util.send("get", f"{self.BASE_PATH}/list", params=params)

    def add(self, data):
        """新增用户。data 示例：
        {"userName":"auto001","nickName":"测试用户","password":"test123456",
         "deptId":100,"phonenumber":"13800000000"}
        """
        return request_util.send("post", self.BASE_PATH, json=data)

    def update(self, data):
        """修改用户（需带 userId）。"""
        return request_util.send("put", self.BASE_PATH, json=data)

    def delete(self, user_ids):
        """删除用户，user_ids 可传单个 id 或逗号拼接的多个 id。"""
        return request_util.send("delete", f"{self.BASE_PATH}/{user_ids}")
