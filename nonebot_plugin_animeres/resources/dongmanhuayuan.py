from typing import List
from urllib.parse import quote

from lxml import etree

from ..config import plugin_config
from ..schemas import Tag, AnimeRes
from ..internal import BaseAnimeSearch


class AnimeSearch(BaseAnimeSearch):
    name = "dongmanhuayuan"
    base_url = "https://www.dongmanhuayuan.com"

    async def search(self, keyword: str) -> bool:
        response = await self.client.get(f"search/{quote(keyword.strip())}/")
        html = etree.HTML(response.text, None)
        for title, size, link in zip(
            html.xpath("//a[@class='uk-text-break']/@title"),
            html.xpath("//b/text()"),
            html.xpath("//span[contains(@class, 'down_txt')]/a/@href"),
        ):
            self.add_resource(
                AnimeRes(title=title, tag="动漫花园", size=size, link=link)
            )
        return bool(self)

    async def get_resources(self, tag: Tag) -> List[AnimeRes]:
        anime_list = self.anime_res.get(tag.name, [])[: plugin_config.animeres_length]
        for anime in anime_list:
            if anime.link:
                response = await self.client.get(anime.link)
                html = etree.HTML(response.text, None)
                magnets = html.xpath("//input[@id='magnet_one']/@value")
                anime.magnet = str(magnets[0]).strip() if magnets else ""
        return anime_list
