from typing import Optional

from nonebot import get_driver
from pydantic import BaseModel


class Config(BaseModel):
    animeres_site: Optional[str] = None
    animeres_proxy: Optional[str] = None
    animeres_forward: bool = False
    animeres_length: int = 3
    animeres_format: str = "{title}\n{magnet}"
    animeres_oneskip: bool = True
    animeres_priority: int = 100
    animeres_block: bool = True


plugin_config = Config(**get_driver().config.dict())
