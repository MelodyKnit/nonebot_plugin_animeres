from typing import List

from nonebot.adapters import Event

from .schemas import AnimeRes


def forward(user_id: int, anime_res: List[AnimeRes]):
    """合并转发消息"""
    return [
        {
            "type": "node",
            "data": {
                "name": "nonebot-plugin-animeres",
                "uin": user_id,
                "content": anime.to_string(),
            },
        }
        for anime in anime_res
    ]


def send_forward(event: Event, anime_res: List[AnimeRes]):
    """发送合并转发消息

    Args:
        event (Event): OneBot 消息类型
        anime_res (List[AnimeRes]): 动漫资源

    Returns:
        dict: 合并转发的内容

    Example:
        ```python
        await bot.call_api(
            **send_forward(event, anime_res)
        )
        ```
    """
    try:
        from nonebot.adapters.onebot.v11 import (
            MessageEvent,
            GroupMessageEvent,
            PrivateMessageEvent,
        )

        if isinstance(event, MessageEvent):
            msg: dict = {
                "messages": forward(event.self_id, anime_res),
            }
            if isinstance(event, GroupMessageEvent):
                msg["api"] = "send_group_forward_msg"
                msg["group_id"] = event.group_id
            elif isinstance(event, PrivateMessageEvent):
                msg["api"] = "send_private_forward_msg"
                msg["user_id"] = event.user_id
            return msg
    except ImportError:
        ...
