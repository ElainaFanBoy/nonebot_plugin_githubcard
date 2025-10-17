"""
配置模块
"""
from typing import Optional, Literal
import nonebot
from pydantic import BaseModel, Extra

from .models import GitHubCardConfig


class Config(BaseModel, extra=Extra.ignore):
    """插件配置"""
    github_token: Optional[str] = None
    github_type: Literal[0, 1] = 1


def get_config() -> GitHubCardConfig:
    """获取GitHub卡片配置"""
    global_config = nonebot.get_driver().config
    config = Config(**global_config.dict())

    return GitHubCardConfig(
        github_token=config.github_token,
        github_type=config.github_type
    )


# 向后兼容
global_config = nonebot.get_driver().config
githubcard_config = Config(**global_config.dict())