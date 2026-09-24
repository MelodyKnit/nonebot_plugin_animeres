from typing import List
from unittest.mock import AsyncMock, patch

import pytest
import nonebot
from nonebug import App
from nonebot.adapters.onebot.v11 import Bot, Adapter, Message, MessageEvent


@pytest.mark.asyncio
async def test_search_not_found(app: App):
    """测试没有找到资源的情况"""
    from nonebot_plugin_animeres import anime_res_cmd

    with patch("nonebot_plugin_animeres.search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = None
        async with app.test_matcher(anime_res_cmd) as ctx:
            adapter = nonebot.get_adapter(Adapter)
            bot = ctx.create_bot(base=Bot, adapter=adapter, self_id="11")
            event = MessageEvent(
                time=1122,
                self_id=11,
                post_type="message",
                sub_type="group",
                user_id=22,
                message_type="group",
                message_id=1,
                message=Message("资源 呜呜呜找不到的动漫"),
                original_message=Message("资源 呜呜呜找不到的动漫"),
                raw_message="资源 呜呜呜找不到的动漫",
                font=1,
                sender={"user_id": 22},
                group_id=33,
            )

            ctx.receive_event(bot, event)
            ctx.should_pass_rule()
            ctx.should_pass_permission()
            ctx.should_call_send(event, "没有找到相关资源！看看是不是哪里写错了？", True)
            ctx.should_finished(anime_res_cmd)


@pytest.mark.asyncio
async def test_dongmanhuayuan_magnet_and_search():
    """测试 dongmanhuayuan 站点解析，验证 magnet 提取与字符串渲染"""
    from nonebot_plugin_animeres.resources.dongmanhuayuan import AnimeSearch
    from nonebot_plugin_animeres.schemas import AnimeRes, Tag

    searcher = AnimeSearch()

    mock_search_html = """
    <html>
        <body>
            <a class="uk-text-break" title="测试动画 第01话" href="/detail/123.html"></a>
            <b>250MB</b>
            <span class="down_txt"><a href="/detail/123.html">下载</a></span>
        </body>
    </html>
    """

    mock_detail_html = """
    <html>
        <body>
            <input id="magnet_one" value="magnet:?xt=urn:btih:ABCDEF123456" />
        </body>
    </html>
    """

    mock_resp_search = AsyncMock()
    mock_resp_search.text = mock_search_html

    mock_resp_detail = AsyncMock()
    mock_resp_detail.text = mock_detail_html

    with patch.object(searcher.client, "get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = [mock_resp_search, mock_resp_detail]

        res = await searcher.search("测试动画")
        assert res is True
        assert "动漫花园" in searcher.anime_res
        assert len(searcher.anime_res["动漫花园"]) == 1

        resources = await searcher.get_resources(Tag(id=1, name="动漫花园"))
        assert len(resources) == 1
        anime = resources[0]
        assert anime.magnet == "magnet:?xt=urn:btih:ABCDEF123456"
        assert not anime.magnet.startswith("[")
        assert anime.to_string() == "测试动画 第01话\nmagnet:?xt=urn:btih:ABCDEF123456"

        # 验证 validate_assignment 起效：若赋非 str 类型应报错
        with pytest.raises(Exception):
            anime.magnet = ["magnet:?xt=urn:btih:INVALID"]

