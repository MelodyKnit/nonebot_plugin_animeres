from typing import Optional
from pydantic import BaseModel
from nonebot import get_driver


class Config(BaseModel):
    animeres_site: str = "动漫花园"
    animeres_proxy: Optional[str] = None
    animeres_forward: bool = False
    animeres_length: int = 3
    animeres_format: str = "{title}\n{magnet}"
    animeres_oneskip: bool = True


plugin_config = Config(**get_driver().config.dict())
