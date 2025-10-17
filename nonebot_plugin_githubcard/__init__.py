from typing import Union
from nonebot import get_driver
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, PrivateMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata, on_message
from nonebot.matcher import Matcher
from nonebot import require

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import on_alconna, AlconnaMatcher, Args, Match
from arclet.alconna import Alconna, CommandMeta

from .config import get_config
from .models import parse_github_url
from .service import GitHubCardService

__plugin_meta__ = PluginMetadata(
    name="githubcard",
    description="检测GitHub仓库链接并自动发送卡片信息，支持仓库、Issue、Pull Request、Release",
    usage="自动识别消息中的GitHub链接并发送对应的卡片图片，支持：仓库、Issue、Pull Request、Release",
    type="application",
    homepage="https://github.com/ElainaFanBoy/nonebot_plugin_githubcard",
    supported_adapters={"~onebot.v11"},
    extra={
        "unique_name": "githubcard",
        "author": "Nanako <demo0929@vip.qq.com>",
        "version": "0.4.1",
    },
)

# 初始化配置和服务
config = get_config()
service = GitHubCardService(config)

# 自动检测GitHub链接的消息处理器
github_auto = on_message(priority=10, block=False)

# Alconna命令处理器
github_cmd = on_alconna(
    Alconna(
        "github",
        Args["url", str],
        meta=CommandMeta(
            description="GitHub链接卡片生成",
            usage="github <GitHub链接>",
            example="github https://github.com/nonebot/nonebot2"
        )
    )
)


async def extract_github_urls(message: str) -> list[str]:
    """从消息中提取GitHub URL"""
    import re
    pattern = r'https?://github\.com/[^\s]+'
    return re.findall(pattern, message)


async def process_github_url(url: str, matcher: Matcher) -> bool:
    """处理单个GitHub URL"""
    try:
        github_link = parse_github_url(url)
        if not github_link:
            logger.warning(f"无法解析GitHub URL: {url}")
            return False

        image_url = await service.generate_card_url(github_link)

        if image_url:
            await matcher.send(MessageSegment.image(image_url))
            logger.info(f"发送GitHub卡片: {github_link.link_type.value} - {url}")
            return True
        else:
            logger.error(f"生成GitHub卡片失败: {url}")
            return False

    except Exception as e:
        logger.error(f"处理GitHub链接失败 {url}: {e}")
        return False


@github_auto.handle()
async def handle_github_auto(
    bot: Bot,
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    matcher: Matcher
) -> None:
    """自动处理消息中的GitHub链接"""
    message_text = event.get_message().extract_plain_text()
    github_urls = await extract_github_urls(message_text)

    if not github_urls:
        return

    # 处理所有找到的GitHub链接
    success_count = 0
    for url in github_urls:
        if await process_github_url(url, matcher):
            success_count += 1

    # 如果没有成功处理任何链接，发送错误提示
    if github_urls and success_count == 0:
        await matcher.send("获取GitHub信息失败")


@github_cmd.handle()
async def handle_github_cmd(
    bot: Bot,
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    matcher: AlconnaMatcher,
    url: Match[str]
) -> None:
    """处理GitHub命令"""
    if url.available:
        github_url = url.result
        if not await process_github_url(github_url, matcher):
            await matcher.send("获取GitHub信息失败")
    else:
        await matcher.send("请提供有效的GitHub链接")
    
