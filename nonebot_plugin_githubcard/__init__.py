from nonebot.rule import T_State
from nonebot import get_driver
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from .config import Config
from .data_source import get_github_reposity_information
from nonebot.plugin import on_regex, PluginMetadata

import re

__plugin_meta__ = PluginMetadata(
    name="githubcard",
    description="检测GitHub仓库链接并自动发送卡片信息（适用于Onebot V11）",
    usage='通过正则表达式检测Github链接',
    type='application',
    homepage='https://github.com/ElainaFanBoy/nonebot_plugin_githubcard',
    supported_adapters={"~onebot.v11"},
    extra={
        "unique_name": "githubcard",
        "author": "Nanako <demo0929@vip.qq.com>",
        "version": "0.2.1",
    },
)

global_config = get_driver().config
config = Config(**global_config.dict())
github = on_regex(r"https?://github\.com/([^/]+/[^/]+)", priority=10, block=False)

def match_link_parts(link):
    pattern = r'https?://github\.com/([^/]+/[^/]+)'
    match = re.search(pattern, link)
    if match:
        return match.group(0)
    else:
        return None
    
@github.handle()
async def github_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    url = match_link_parts(event.get_plaintext())
    imageUrl = await get_github_reposity_information(url)
    assert(imageUrl != "获取信息失败")
    await github.send(MessageSegment.image(imageUrl))
    
