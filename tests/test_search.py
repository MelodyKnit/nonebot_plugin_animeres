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
            ctx.should_call_send(
                event, "没有找到相关资源！看看是不是哪里写错了？", True
            )
            ctx.should_finished(anime_res_cmd)
