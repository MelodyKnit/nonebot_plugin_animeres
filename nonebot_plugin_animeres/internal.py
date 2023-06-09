from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from httpx import AsyncClient
from fake_useragent import UserAgent

from .config import plugin_config
from .schemas import Tag, AnimeRes


class BaseAnimeSearch(ABC):
    """动漫资源搜索基类"""

    name: str = ""
    base_url: Optional[str] = None
    _client: Optional[AsyncClient] = None

    def __init__(self) -> None:
        self.tags: List[Tag] = []
        self.anime_res: Dict[str, List[AnimeRes]] = {}
        self.headers = {
            "User-Agent": UserAgent().chrome,
        }

    def set_header(self, key: str, value: str):
        """修改请求头

        Args:
            key (str): key
            value (str): value
        """
        self.headers[key] = value

    @property
    def client(self) -> AsyncClient:
        if self._client is None:
            self._client = AsyncClient(
                headers=self.headers,
                base_url=self.base_url or "",
                proxies=plugin_config.animeres_proxy,
                trust_env=True,
                timeout=600,
            )
        return self._client

    @abstractmethod
    async def search(self, keyword: str) -> bool:
        """搜索
        在进行搜索时会先调用这个方法，如果返回 True 则会进行 get_tags 和 get_resources 方法

        Args:
            keyword (str): 关键字

        Returns:
            bool: 是否搜索成功
        """

    @abstractmethod
    async def get_resources(self, tag: Tag) -> List[AnimeRes]:
        """获取资源

        Args:
            tag (str): 关键字

        Returns:
            List[AnimeRes]: 资源
        """

    async def get_tags(self) -> List[Tag]:
        """获取类型
        在询问用户需要哪种类型的资源时会调用这个方法

        Args:
            keyword (str): 关键字

        Returns:
            List[Tag]: 类型
        """
        self.tags = [
            Tag(id=i, name=tag) for i, tag in enumerate(self.anime_res.keys(), 1)
        ]
        return self.tags

    def oneskip(self) -> bool:
        """如果只有一种类型的资源，跳过选项"""
        return plugin_config.animeres_oneskip and len(self.tags) == 1

    def add_resource(self, anime_res: AnimeRes):
        """添加资源"""
        self.anime_res.setdefault(anime_res.tag, []).append(anime_res)

    async def get_tag(self, index: str):
        tags = await self.get_tags()
        for tag in tags:
            if tag == index or index.isdigit() and tag == int(index):
                return tag

    def __bool__(self) -> bool:
        return bool(self.anime_res)
