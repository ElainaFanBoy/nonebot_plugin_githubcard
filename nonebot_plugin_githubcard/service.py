"""
GitHub卡片生成服务
"""
import asyncio
from typing import Optional, Dict, Any
from urllib.parse import quote
import aiohttp
from nonebot.log import logger

from .models import GitHubLink, GitHubLinkType, GitHubCardConfig


class GitHubCardService:
    """GitHub卡片服务类"""

    def __init__(self, config: GitHubCardConfig):
        self.config = config
        self.headers = self._build_headers()

    def _build_headers(self) -> Dict[str, str]:
        """构建请求头"""
        base_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        if self.config.github_token:
            base_headers.update({
                "Authorization": f"Bearer {self.config.github_token}",
                "Accept": "application/vnd.github+json"
            })

        return base_headers

    async def generate_card_url(self, github_link: GitHubLink) -> str:
        """
        生成GitHub卡片URL

        Args:
            github_link: 解析后的GitHub链接信息

        Returns:
            卡片图片URL
        """
        try:
            if github_link.link_type == GitHubLinkType.REPO:
                return await self._generate_repo_card(github_link)
            elif github_link.link_type == GitHubLinkType.ISSUE:
                return self._generate_issue_card(github_link)
            elif github_link.link_type == GitHubLinkType.PULL:
                return self._generate_pull_card(github_link)
            elif github_link.link_type == GitHubLinkType.RELEASE:
                return self._generate_release_card(github_link)
            else:
                raise ValueError(f"Unsupported link type: {github_link.link_type}")

        except Exception as e:
            logger.error(f"生成GitHub卡片失败: {e}")
            raise

    async def _generate_repo_card(self, github_link: GitHubLink) -> str:
        """生成仓库卡片URL"""
        if self.config.github_type == 0:
            # Socialify样式
            avatar_url = await self._get_user_avatar(github_link.username)
            if not avatar_url:
                # 如果获取头像失败，使用默认参数
                avatar_url = ""

            encoded_avatar = quote(avatar_url) if avatar_url else ""
            logo_param = f"&logo={encoded_avatar}" if encoded_avatar else ""

            return (
                f"https://socialify.git.ci/{github_link.username}/{github_link.repository}/png?"
                f"description=1&font=Rokkitt&forks=1&issues=1&language=1&name=1&owner=1"
                f"&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light{logo_param}"
            )
        else:
            # GitHub OpenGraph样式
            return f"https://opengraph.githubassets.com/githubcard/{github_link.username}/{github_link.repository}"

    def _generate_issue_card(self, github_link: GitHubLink) -> str:
        """生成Issue卡片URL"""
        return f"https://opengraph.githubassets.com/1/{github_link.username}/{github_link.repository}/issues/{github_link.identifier}"

    def _generate_pull_card(self, github_link: GitHubLink) -> str:
        """生成PR卡片URL"""
        return f"https://opengraph.githubassets.com/1/{github_link.username}/{github_link.repository}/pull/{github_link.identifier}"

    def _generate_release_card(self, github_link: GitHubLink) -> str:
        """生成Release卡片URL"""
        if github_link.identifier and github_link.identifier.startswith('tag/'):
            tag_name = github_link.identifier[4:]  # 移除 'tag/' 前缀
            return f"https://opengraph.githubassets.com/1/{github_link.username}/{github_link.repository}/releases/tag/{tag_name}"
        else:
            return f"https://opengraph.githubassets.com/1/{github_link.username}/{github_link.repository}/releases/{github_link.identifier}"

    async def _get_user_avatar(self, username: str) -> Optional[str]:
        """
        获取用户头像URL

        Args:
            username: GitHub用户名

        Returns:
            头像URL或None
        """
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    f"https://api.github.com/users/{username}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        return user_data.get("avatar_url")
                    else:
                        logger.warning(f"获取用户 {username} 头像失败: HTTP {response.status}")
                        return None

        except asyncio.TimeoutError:
            logger.warning(f"获取用户 {username} 头像超时")
            return None
        except Exception as e:
            logger.error(f"获取用户 {username} 头像异常: {e}")
            return None