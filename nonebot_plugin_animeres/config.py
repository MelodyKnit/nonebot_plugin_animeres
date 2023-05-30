from typing import Optional
from pydantic import BaseModel
from nonebot import get_driver


class Config(BaseModel):
    animeres_site: Optional[str] = None
    animeres_proxy: Optional[str] = None
    animeres_forward: bool = False
    animeres_length: int = 3
    animeres_format: str = "{title}\n{magnet}"
    animeres_oneskip: bool = True
    animeres_priority: int = 100


plugin_config = Config(**get_driver().config.dict())
