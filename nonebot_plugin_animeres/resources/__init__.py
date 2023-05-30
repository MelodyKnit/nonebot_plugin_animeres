from typing import Dict, Optional, Type
from nonebot.log import logger

from httpx import ConnectError
from .myheartsite import AnimeSearch as MyHeartSiteSearch
from ..internal import BaseAnimeSearch
from ..config import plugin_config

site: Dict[str, Type[BaseAnimeSearch]] = {
    MyHeartSiteSearch.name: MyHeartSiteSearch,
}


async def search(keyword: str) -> Optional[BaseAnimeSearch]:
    """对站点资源进行搜索

    Args:
        keyword (str): 搜索的关键字

    Returns:
        Optional[BaseAnimeSearch]: 搜索对象

    Example:
        ```python
        if animeres := await search("海贼王"):
            tags = await animeres.get_tags()
            print(tags)
            anime_list = await animeres.get_resources(tags[0])
            print(anime_list)
        ```
    """
    if plugin_config.animeres_site is not None:
        if anime_search := site.get(plugin_config.animeres_site):
            try:
                search_ = anime_search()
                if await search_.search(keyword):
                    return search_
            except ConnectError:
                logger.error(
                    f"ConnectError: '{plugin_config.animeres_site}' 资源链接失败，尝试为您切换站点"
                )
    for i in site:
        search_ = site[i]()
        try:
            if await search_.search(keyword):
                plugin_config.animeres_site = i
                logger.success(f"已切换至 '{i}' 站点")
                return search_
        except ConnectError:
            logger.error(f"ConnectError: '{i}' 资源链接失败，尝试为您切换站点")
    else:
        logger.error("所有站点资源链接失败，可能站点失效或者查网络连接的原因！")
        return None
