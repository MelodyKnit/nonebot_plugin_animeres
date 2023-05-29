from typing import Dict, Optional, Type
from .anoneko import AnimeSearch as AnonekoSearch
from .myheartsite import AnimeSearch as MyHeartSiteSearch
from ..internal import BaseAnimeSearch
from ..config import plugin_config

site: Dict[str, Type[BaseAnimeSearch]] = {
    AnonekoSearch.name: AnonekoSearch,
    MyHeartSiteSearch.name: MyHeartSiteSearch,
}


async def search(keyword: str) -> Optional[BaseAnimeSearch]:
    if plugin_config.animeres_site is not None:
        if anime_search := site.get(plugin_config.animeres_site):
            search_ = anime_search()
            if await search_.search(keyword):
                return search_
    for i in site:
        search_ = site[i]()
        if await search_.search(keyword):
            plugin_config.animeres_site = i
            return search_



__all__ = ["AnonekoSearch"]
