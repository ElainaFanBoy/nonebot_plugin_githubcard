import nonebot
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    github_token : str

global_config = nonebot.get_driver().config
githubcard_config = Config(**global_config.dict())