from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from httpx import AsyncClient
from .config import plugin_config
from .schemas import AnimeRes, Tag


class BaseAnimeSearch(ABC):
    """动漫资源搜索基类"""

    name: Optional[str] = None
    base_url: Optional[str] = None
    _client: Optional[AsyncClient] = None

    def __init__(self) -> None:
        self.tags: List[Tag] = []
        self.anime_res: Dict[str, List[AnimeRes]] = {}

    @property
    def client(self) -> AsyncClient:
        if self._client is None:
            self._client = AsyncClient(
                base_url=self.base_url or "",
                proxies=plugin_config.animeres_proxy,
            )
        return self._client

    @abstractmethod
    async def search(self, keyword: str) -> bool: 
        """搜索

        Args:
            keyword (str): 关键字

        Returns:
            bool: 是否搜索成功
        """

    @abstractmethod
    async def get_tags(self) -> List[Tag]:
        """获取类型

        Args:
            keyword (str): 关键字

        Returns:
            List[Tag]: 类型
        """

    @abstractmethod
    async def get_resources(self, tag: Tag) -> List[AnimeRes]:
        """获取资源

        Args:
            tag (str): 关键字

        Returns:
            List[AnimeRes]: 资源
        """

    def __bool__(self) -> bool:
        return bool(self.anime_res)
