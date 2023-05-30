from typing import List
from ..config import plugin_config
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

        data = response.json()["data"]["searchData"]
        for i in data:
            anime = AnimeRes.parse_obj(
                {
                    "title": i["title"],
                    "tag": i["type"],
                    "link": i["link"],
                    "size": i["size"],
                    "id": i["id"],
                }
            )
            self.add_resource(anime)
        return bool(self)

    async def get_resources(self, tag: Tag) -> List[AnimeRes]:
        anime_list = self.anime_res.get(tag.name, [])
        if plugin_config.animeres_length != 0:
            anime_list = anime_list[: plugin_config.animeres_length]
        for anime in anime_list:
            response = await self.client.post(
                "/api/acg/detail",
                data={"link": anime.link, "id": anime.id},  # type: ignore
            )
            anime.magnet = response.json()["data"]["magnetLink1"]
        return anime_list
