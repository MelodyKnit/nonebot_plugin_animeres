from aiohttp import ClientConnectorError
from nonebot.typing import T_State
from nonebot import on_command
from nonebot.params import CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import (
    Message,
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
    MessageEvent,
    MessageSegment,
)
from .config import Config
from .resources import search
from .internal import BaseAnimeSearch

anime_res_cmd = on_command("资源", aliases={"动漫资源"})


@anime_res_cmd.handle()
async def _(state: T_State, msg: Message = CommandArg()):
    if text := msg.get("text"):
        state["param"] = text


@anime_res_cmd.got("param", prompt="动漫名字叫什么呀！")
async def _(matcher: Matcher, state: T_State, param: str = ArgPlainText()):
    if param:
        anime_search = await search(param)
        if anime_search:
            state["anime_search"] = anime_search
            tags = await anime_search.get_tags()
            await matcher.send("选择哪种呢？：\n" + "\n".join(repr(tag) for tag in tags))
        else:
            await matcher.finish("没有找到相关资源！看看是不是哪里写错了？")
    else:
        await matcher.finish()


@anime_res_cmd.got("index")
async def _(bot: Bot, matcher: Matcher, state: T_State, index: str = ArgPlainText()):
    anime_search: BaseAnimeSearch = state["anime_search"]
    if tag := await anime_search.get_tag(index):
        
        anime_list = await anime_search.get_resources(tag)


__helper__ = {
    "cmd": "资源",
    "params": "动漫名字",
    "tags": "搜索 动漫 动漫资源",
    "use": "资源 [动漫名字]",
    "doc": "根据一些动漫的关键字进行资源搜索，具体搜索是依靠关键字哦，例如：资源 天气之子，这时候会根据名字就行搜索\n"
    "如果搜索的结果不理想，可以换个方式搜索，例如需要搜索的天气之子资源需要是mkv格式的生肉资源，就可以这样写\n"
    "资源 天气之子 mkv raws\n"
    "将这些关键字以空格的方式分开搜索，可以提高搜索结果的精准度。",
}

__plugin_meta__ = PluginMetadata(
    name="动漫资源插件",
    description="根据关键字搜索动漫资源",
    usage="资源 你的名字",
    config=Config,
)
