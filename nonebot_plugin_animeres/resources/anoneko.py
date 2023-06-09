from typing import List

from lxml import etree

from ..schemas import Tag, AnimeRes
from ..internal import BaseAnimeSearch


class AnimeSearch(BaseAnimeSearch):
    name: str = "anoneko"
    base_url: str = "https://dmhy.anoneko.com"

    async def search(self, keyword: str) -> bool:
        response = await self.client.get("/topics/list", params={"keyword": keyword})
        data: List[etree._Element] = etree.HTML(
            response.text, etree.HTMLParser()
        ).xpath("//table[@class='tablesorter']//tbody//tr")
        for value in data:
            anime = AnimeRes(
                title=value.xpath("string(./td[@class='title'])").replace("\n", ""),
                tag=value.xpath("string(./td/a//font)"),
                magnet=value.xpath(
                    "string(./td/a[@class='download-arrow arrow-magnet']/@href)"
                ).split("&")[0],
                size=value.xpath("./td")[4].text,
            )
            self.anime_res.setdefault(anime.tag, []).append(anime)
        return bool(self.anime_res)

    async def get_resources(self, tag: Tag) -> List[AnimeRes]:
        return self.anime_res.get(tag.name, [])
