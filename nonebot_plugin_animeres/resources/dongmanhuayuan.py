from typing import List

from lxml import etree

from ..config import plugin_config
from ..schemas import Tag, AnimeRes
from ..internal import BaseAnimeSearch


class AnimeSearch(BaseAnimeSearch):
    name = "dongmanhuayuan"
    base_url = "https://www.dongmanhuayuan.com"

    async def search(self, keyword: str) -> bool:
        response = await self.client.get(f"search/{keyword}/")
        html = etree.HTML(response.text, None)
        for title, size, link in zip(
            html.xpath("//a[@class='uk-text-break']/@title"),
            html.xpath("//b/text()"),
            html.xpath("//span[contains(@class, 'down_txt')]/a/@href"),
        ):
            self.add_resource(AnimeRes(title=title, tag="动漫花园", size=size, link=link))
        return bool(self)

    async def get_resources(self, tag: Tag) -> List[AnimeRes]:
        anime_list = self.anime_res.get(tag.name, [])[: plugin_config.animeres_length]
        for anime in anime_list:
            if anime.link:
                response = await self.client.get(anime.link)
                html = etree.HTML(response.text, None)
                anime.magnet = html.xpath("//input[@id='magnet_one']/@value")
        return anime_list
