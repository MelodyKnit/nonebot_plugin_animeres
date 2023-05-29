from typing import List, Union
from ..internal import BaseAnimeSearch
from ..schemas import AnimeRes, Tag


class AnimeSearch(BaseAnimeSearch):
    name: str = "myheartsite"
    base_url: str = "https://dmhy.myheartsite.com"

    async def search(self, keyword: str) -> bool:
        response = await self.client.post(
            "/api/acg/search",
            data={
                "keyword": keyword,
                "page": 1,
                "searchType": 0,
                "serverType": "server1",
            },
        )

        print(response.json()["searchData"])
        return False

    async def get_resources(self, tag: Union[int, str, Tag]) -> List[AnimeRes]:
        ...

    async def get_tags(self) -> List[Tag]:
        ...
