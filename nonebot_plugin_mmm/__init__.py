from typing import Any
import asyncio

from nonebot import on, get_driver, get_plugin_config
from pydantic import Field, BaseModel
from nonebot.plugin import PluginMetadata
from nonebot.internal.matcher import current_event
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, PrivateMessageEvent


class Config(BaseModel):
    mmm_block: bool = Field(default=True, description="把message_sent后续block!")
    mmm_priority: int = Field(default=0, description="on(message_sent)的priority")


__plugin_meta__ = PluginMetadata(
    name="Bot的消息也是消息",
    description="Bot的消息也是消息!",
    usage="无",
    type="library",
    homepage="https://github.com/eya46/nonebot-plugin-mmm",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

config = get_plugin_config(Config)
tasks: set["asyncio.Task"] = set()


@get_driver().on_shutdown
async def cancel_tasks():
    for task in tasks:
        if not task.done():
            task.cancel()

    await asyncio.gather(
        *(asyncio.wait_for(task, timeout=10) for task in tasks),
        return_exceptions=True,
    )


def push_event(bot: Bot, event: Event):
    task = asyncio.create_task(bot.handle_event(event))
    task.add_done_callback(tasks.discard)
    tasks.add(task)


@on("message_sent", block=config.mmm_block, priority=config.mmm_priority).handle()
async def _(event: Event, bot: Bot):
    data = event.model_dump()
    if data.get("message_type") == "private":
        data["post_type"] = "message"
        push_event(bot, PrivateMessageEvent.model_validate(data))
    elif data.get("message_type") == "group":
        data["post_type"] = "message"
        push_event(bot, GroupMessageEvent.model_validate(data))


@Bot.on_calling_api
async def patch_send(bot: Bot, api: str, data: dict[str, Any]):
    """避免在PrivateMessageEvent事件中发消息时发给自己..."""
    if api not in ["send_msg", "send_private_msg"]:
        return
    event = current_event.get()
    if not isinstance(event, PrivateMessageEvent) or event.self_id != event.user_id:
        return
    data["user_id"] = getattr(event, "target_id", event.user_id)
