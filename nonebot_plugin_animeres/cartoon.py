from typing import List, Optional, Callable
from aiohttp import ClientSession, TCPConnector
from lxml import etree
from nonebot.log import logger

from .config import Cartoon, Cartoons, global_config

methods: List[Callable] = []


async def GetCartoons(name: str) -> Optional[Cartoons]:
    """获取对应的资源

    Returns:
        Cartoons: 资源列表
    """
    async with ClientSession(connector=TCPConnector(ssl=False), trust_env=True) as session:
        for method in methods:
            try:
                if cartoons := await method(session, name):
                    return cartoons
            except Exception as err:
                logger.error(f"{method.__name__}获取失败：{err}")
                continue


@methods.append
async def dmhy(session: ClientSession, name: str) -> Cartoons:
    main_url = "https://dmhy.anoneko.com/topics/list"
    async with session.get(main_url, params={"keyword": name}, proxy=global_config.cartoon_proxy) as res:
        data: List[etree._Element] = etree.HTML(await res.text(), etree.HTMLParser()).xpath("//table[@class='tablesorter']//tbody//tr")
        return Cartoons([Cartoon(
            title=value.xpath("string(./td[@class='title'])").replace("\n", ""),
            tag=value.xpath("string(./td/a//font)"),
            magnet=value.xpath("string(./td/a[@class='download-arrow arrow-magnet']/@href)").split("&")[0],
            size=value.xpath("./td")[4].text,
        ) for value in data])
