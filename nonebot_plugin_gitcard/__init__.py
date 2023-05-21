from nonebot.rule import T_State
from nonebot import on_message, get_driver
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
import re
from .config import Config
from .data_source import get_github_reposity_information
from nonebot.plugin import on_regex

global_config = get_driver().config
config = Config(**global_config.dict())
github = on_regex(r"github.com\/(.+)?\/([^\/\s]+)", priority=10, block=False)

@github.handle()
async def github_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    url = event.get_plaintext()
    imageUrl = await get_github_reposity_information(url)
    assert(imageUrl != "获取信息失败")
    await github.send(Message(f"[CQ:image,file={imageUrl}]"))