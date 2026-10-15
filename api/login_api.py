"""登录相关接口封装。"""
from common.request_util import request_util


class LoginApi:
    LOGIN_PATH = "/login"
    INFO_PATH = "/getInfo"

    def login(self, username, password, code=None, uuid=None):
        """
        登录接口。
        自动化环境建议在后端 application.yml 关闭验证码（captchaEnabled: false），
        此时只传 username / password 即可；若开启验证码，则额外传 code / uuid。
        """
        body = {"username": username, "password": password}
        if code is not None:
            body["code"] = code
            body["uuid"] = uuid
        return request_util.send("post", self.LOGIN_PATH, json=body)

    def get_info(self):
        """获取当前登录用户信息（可用来校验 Token 是否生效）。"""
        return request_util.send("get", self.INFO_PATH)
