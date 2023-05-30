import pytest


@pytest.mark.asyncio
async def test_site(name: str):
    from nonebot_plugin_animeres.resources import site

    for name, search in site.items():
        s = search()
        print(name)
        assert await s.search("你的名字") == True
