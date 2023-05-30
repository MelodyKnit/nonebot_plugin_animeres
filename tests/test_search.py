import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "keyword, expected",
    [
        ("你的名字", True),
        ("不存在的关键词", False),
    ],
)
async def test_animeres(keyword, expected):
    """测试资源搜索"""
    from nonebot_plugin_animeres.resources import search
    from nonebot_plugin_animeres.internal import BaseAnimeSearch

    anime = await search(keyword)
    assert isinstance(anime, BaseAnimeSearch) == expected
