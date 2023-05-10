from nonebot.rule import T_State
from nonebot import on_message, get_driver
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
import re
from .config import Config
from .data_source import get_github_reposity_information


global_config = get_driver().config
config = Config(**global_config.dict())
github = on_message(priority=50,block=False)


@github.handle()
async def github_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    url = event.get_plaintext()
    if re.match("https://github.com/.*?/.*?", url) != None:
        imageUrl = await get_github_reposity_information(url)
        assert(imageUrl != "获取信息失败")
        await github.send(Message(f"[CQ:image,file={imageUrl}]"))