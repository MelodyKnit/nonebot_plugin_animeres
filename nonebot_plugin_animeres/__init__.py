from nonebot import on_command
from nonebot.typing import T_State
from nonebot.params import CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.adapters import Message, Bot, Event

from .config import Config, plugin_config
from .resources import search
from .internal import BaseAnimeSearch
from .utils import send_forward

anime_res_cmd = on_command(
    "资源", aliases={"动漫资源"}, priority=plugin_config.animeres_priority
)


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
            if anime_search.oneskip():
                msg: Message = state["param"].copy()
                msg.clear()
                matcher.set_arg("index", msg + tags[0].name)
            else:
                await matcher.send("选择哪种呢？\n" + "\n".join(repr(tag) for tag in tags))
        else:
            await matcher.finish("没有找到相关资源！看看是不是哪里写错了？")
    else:
        await matcher.finish()


@anime_res_cmd.got("index")
async def _(
    bot: Bot,
    matcher: Matcher,
    event: Event,
    state: T_State,
    index: str = ArgPlainText(),
):
    anime_search: BaseAnimeSearch = state["anime_search"]
    if tag := await anime_search.get_tag(index):
        anime_list = await anime_search.get_resources(tag)
        if plugin_config.animeres_length != 0:
            anime_list = anime_list[: plugin_config.animeres_length]
        if plugin_config.animeres_forward and bot.adapter.get_name().startswith(
            "OneBot"
        ):
            if forward_msg := send_forward(event, anime_list):
                await bot.call_api(**forward_msg)
        else:
            await matcher.finish("\n\n".join(i.to_string() for i in anime_list))
    else:
        await matcher.finish("我有说过有这个选项吗？看看是不是哪里写错了？")


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
