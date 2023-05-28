from typing import List, Union
from lxml import etree

from ..internal import BaseAnimeSearch
from ..schemas import AnimeRes, Tag


class AnimeSearch(BaseAnimeSearch):
    name: str = "动漫花园"
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

    async def get_resources(self, tag: Union[int, str, Tag]) -> List[AnimeRes]:
        return self.anime_res.get(self.get_tag(tag).name, [])

    async def get_tags(self) -> List[Tag]:
        self.tags = [Tag(id=i, name=v) for i, v in enumerate(self.anime_res.keys())]
        return self.tags

    def get_tag(self, key: Union[int, str, Tag]) -> Tag:
        for tag in self.tags:
            if tag == key:
                return tag
        raise ValueError("tag not found")
