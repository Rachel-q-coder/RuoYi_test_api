# RuoYi 后台管理平台 - 接口自动化测试框架

基于 **Python + Pytest + Requests + Allure** 的接口自动化框架，覆盖登录、用户管理模块，
演示「配置管理 → 请求封装 → 接口层 → 数据驱动 → Token 鉴权 → 日志 → Allure 报告」完整链路。

---

## 一、目录结构

```
ruoyi_api_autotest/
├── config/
│   └── config.yaml        # 环境配置（base_url、账号、超时），切换环境只改这里
├── common/                # 公共封装层
│   ├── yaml_util.py       # 读取 yaml 配置/数据
│   ├── log_util.py        # 日志封装（控制台 + logs/run.log）
│   └── request_util.py    # 请求基类（统一 base_url、超时、Token、日志）
├── api/                   # 接口对象层：每个模块的接口封装成类
│   ├── login_api.py       # 登录、getInfo
│   └── user_api.py        # 用户增删改查
├── testcases/             # 测试用例层（test_*.py）
│   ├── test_login.py      # 登录：数据驱动（正常/异常/边界）
│   └── test_user.py       # 用户：列表查询 + 新增->查询->删除闭环
├── data/
│   └── login_data.yaml    # 数据驱动用例数据
├── demo/
│   └── test_demo.py       # 零环境手感练习（联网打 httpbin，不依赖 RuoYi）
├── mock_server.py         # RuoYi 接口 Mock 服务器（纯标准库，离线跑通整套框架）
├── logs/                  # 运行日志（自动生成）
├── reports/               # Allure 原始数据（自动生成）
├── conftest.py            # 全局 fixture：会话级登录，自动注入 Token
├── pytest.ini             # pytest 配置
├── run.py                 # 一键执行入口
└── requirements.txt
```

**分层思想（面试讲这个）**：
- 接口层（api）只管"怎么调接口"；用例层（testcases）只管"测什么、断言什么"；
- 公共能力（请求、日志、配置）下沉到 common；数据和用例分离（data/）。
- 好处：接口变了只改 api，用例变了只改 testcases，数据变了只改 yaml，**互不影响、易维护**。

---

## 二、环境准备

### 1. 安装 Python 依赖
```bash
pip install -r requirements.txt
# 国内网络慢可加镜像：
# pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 启动 RuoYi 后端（被测系统）
确保 MySQL、Redis 已启动，然后启动 RuoYi 后端（默认 8080 端口）。
本框架直接请求后端，**base_url 用 `http://localhost:8080`，不要带 `/dev-api` 前缀**。

### 3. 关闭登录验证码（自动化关键）
在后端 `ruoyi-admin/src/main/resources/application.yml` 中找到：
```yaml
captcha:
  enabled: false   # 把 true 改成 false，重启后端
```
> 不关验证码的话，登录还需先调 `/captchaImage` 拿 uuid 并识别图片验证码，不适合自动化。
> 面试可答："通过关闭测试环境验证码 / 万能验证码 / 接口绕过的方式处理。"

### 4. 核对账号
RuoYi 默认管理员 `admin / admin123`，如改过请同步修改 `config/config.yaml`。

---

## 三、执行用例

```bash
# 方式一：一键执行并（如已装 allure）自动打开报告
python run.py

# 方式二：pytest 命令
pytest                      # 跑全部
pytest -m smoke             # 只跑冒烟用例
pytest testcases/test_login.py            # 只跑登录模块
pytest -k test_user_list                  # 按关键字跑
pytest --alluredir=./reports --clean-alluredir

# 生成并查看 Allure 报告（需本机安装 Allure 命令行）
allure serve ./reports
```

- **没装 Allure 不影响用例执行**，只是没有可视化报告；也可以直接交给 Jenkins 的 Allure 插件展示。
- 运行日志在 `logs/run.log`。

---

## 四、零环境练手（还没搭 RuoYi 时）

**方式一：用内置 Mock 服务器跑通整套框架（推荐，离线可用）**
```bash
# 终端 A：启动 Mock（默认 8080，与 config.yaml 一致；账号 admin/admin123）
python mock_server.py

# 终端 B：跑全部用例
pytest
```
> Mock 用 Python 标准库实现了登录、用户列表、增删改查，能完整演示 Token 鉴权、
> 数据驱动和「新增->查询->删除」闭环，**无需安装 RuoYi / MySQL / Redis**。
> 如 8080 被占用：`PORT=8090 python mock_server.py`，并把 `config/config.yaml` 的 base_url 改成 `http://127.0.0.1:8090`。

**方式二：联网请求公开测试站点 httpbin（只验证 pytest 链路）**
```bash
cd demo
pytest -vs test_demo.py
```

---

## 五、接入 Jenkins（对应简历里的"定时回归 + Allure 报告"）

1. 新建自由风格 / Pipeline 任务，配置 Git 仓库（或直接把代码放工作目录）；
2. 构建步骤执行：
   ```bash
   pip install -r requirements.txt
   pytest --alluredir=./reports --clean-alluredir
   ```
3. 「构建触发器 → Build periodically」配置定时，例如 `H 2 * * *`（每天凌晨 2 点跑回归）；
4. 「构建后操作 → Allure Report」，Results 路径填 `reports`；
5. 可配置失败邮件/钉钉通知。

---

## 六、常见问题

| 现象 | 原因 / 处理 |
|---|---|
| 登录返回需要验证码 / code 为空 | 没关验证码，按第二节第 3 步设置 `captcha.enabled: false` 并重启 |
| 连接拒绝 `Connection refused` | 后端没启动 / 端口不对，检查 `config.yaml` 的 base_url 与后端端口 |
| 401 / 未授权 | Token 未生效，确认 `login_token` fixture 已被用例引用、请求头带了 Authorization |
| 新增用户提示手机号/用户名重复 | 用例已用时间戳保证唯一；若仍冲突，检查环境残留数据 |
| 找不到模块 `ModuleNotFoundError: common` | 在项目根目录（pytest.ini 所在目录）执行 pytest，不要在子目录里跑 |

---

## 七、可以继续扩展的方向（面试可聊的优化点）
- 用 `pytest-xdist` 做并行执行；`pytest-rerunfailures` 做失败重跑；
- 接入 conftest 钩子实现失败用例自动截图/保存响应；
- 用例与数据完全分离，数据统一放 yaml/excel，支持多环境切换；
- 接入企业微信/钉钉机器人推送测试结果；
- 结合 Git + Jenkins 实现提交即触发的 CI 流水线。
