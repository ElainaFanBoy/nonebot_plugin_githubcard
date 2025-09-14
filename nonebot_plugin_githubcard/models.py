"""
GitHub链接解析相关的数据模型
"""
from typing import Optional, Literal
from enum import Enum
from pydantic import BaseModel
from urllib.parse import urlparse


class GitHubLinkType(str, Enum):
    """GitHub链接类型枚举"""
    REPO = "repo"
    ISSUE = "issues"
    PULL = "pull"
    RELEASE = "releases"


class GitHubLink(BaseModel):
    """GitHub链接解析结果"""
    url: str
    username: str
    repository: str
    link_type: GitHubLinkType
    identifier: Optional[str] = None  # issue/pr number 或 release tag/id


class GitHubCardConfig(BaseModel):
    """GitHub卡片配置"""
    github_token: Optional[str] = None
    github_type: Literal[0, 1] = 0  # 0: socialify, 1: opengraph


def parse_github_url(url: str) -> Optional[GitHubLink]:
    """
    解析GitHub URL

    Args:
        url: GitHub URL

    Returns:
        解析结果或None（如果解析失败）
    """
    try:
        parsed = urlparse(url)
        if parsed.netloc != "github.com":
            return None

        path_parts = [p for p in parsed.path.split("/") if p]

        if len(path_parts) < 2:
            return None

        username = path_parts[0]
        repository = path_parts[1]

        # 默认为仓库链接
        if len(path_parts) == 2:
            return GitHubLink(
                url=url,
                username=username,
                repository=repository,
                link_type=GitHubLinkType.REPO
            )

        # 解析子路径
        if len(path_parts) >= 4:
            sub_type = path_parts[2]
            identifier = path_parts[3]

            # 处理release的tag格式
            if sub_type == "releases" and identifier == "tag" and len(path_parts) >= 5:
                identifier = f"tag/{path_parts[4]}"

            if sub_type in ["issues", "pull", "releases"]:
                return GitHubLink(
                    url=url,
                    username=username,
                    repository=repository,
                    link_type=GitHubLinkType(sub_type),
                    identifier=identifier
                )

        return None

    except Exception:
        return None