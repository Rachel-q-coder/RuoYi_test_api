"""读取 YAML 配置 / 测试数据的工具模块。"""
import yaml
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"


def read_yaml(path):
    """读取任意 yaml 文件，返回 dict / list。"""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class Config:
    """配置单例，全局通过 Config.get() 拿当前环境配置。"""
    _data = None

    @classmethod
    def get(cls):
        if cls._data is None:
            cls._data = read_yaml(CONFIG_PATH)["test"]
        return cls._data
