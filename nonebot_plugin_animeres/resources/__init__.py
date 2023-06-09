from typing import Dict, Type, Optional

from httpx import ConnectError
from nonebot.log import logger

from ..config import plugin_config
from ..internal import BaseAnimeSearch
from .anoneko import AnimeSearch as AnonekoSearch
from .myheartsite import AnimeSearch as MyHeartSiteSearch
from .dongmanhuayuan import AnimeSearch as DongManHuaYuanSearch

site: Dict[str, Type[BaseAnimeSearch]] = {
    MyHeartSiteSearch.name: MyHeartSiteSearch,
    DongManHuaYuanSearch.name: DongManHuaYuanSearch,
    AnonekoSearch.name: AnonekoSearch,
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
    if plugin_config.animeres_site is not None:  # 当配置项中有填写资源站点的情况下
        logger.info(f"使用资源站点 '{plugin_config.animeres_site}'")
        if anime_search := site.get(plugin_config.animeres_site):  # 获取对应资源站点
            try:
                search_ = anime_search()
                if await search_.search(keyword):  # 进行搜索
                    return search_
            except ConnectError:
                logger.error(
                    f"ConnectError: '{plugin_config.animeres_site}' 资源链接失败，尝试为您切换站点"
                )
    for i in site:  # 如果未能搜索到资源则依次搜索
        search_ = site[i]()
        try:
            if await search_.search(keyword):
                plugin_config.animeres_site = i  # 当搜索成功后切换站点
                logger.success(f"已切换至 '{i}' 站点")
                return search_
        except ConnectError:
            logger.error(f"ConnectError: '{i}' 资源链接失败，尝试为您切换站点")
    else:
        logger.error("所有站点资源链接失败，可能站点失效或者查网络连接的原因！")
        return None
