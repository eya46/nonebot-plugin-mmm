from typing import Any, Union
import asyncio

from nonebot import on, get_driver, get_plugin_config
from pydantic import Field, BaseModel
from nonebot.compat import model_dump, type_validate_python
from nonebot.plugin import PluginMetadata
from nonebot.internal.matcher import current_event
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, PrivateMessageEvent


class Config(BaseModel):
    mmm_block: bool = Field(default=True, description="把message_sent后续block!")
    mmm_priority: int = Field(default=0, description="on(message_sent)的priority")
    mmm_private: bool = Field(default=True, description="是否处理私聊消息")
    mmm_group: bool = Field(default=True, description="是否处理群聊消息")
    mmm_self: bool = Field(default=False, description="是否处理对自己的私聊消息")

    mmm_only_text: bool = Field(default=False, description="是否只处理文本消息")
    mmm_text_check: bool = Field(default=False, description="是否检查文本消息")
    mmm_use_nb_start: bool = Field(default=False, description="是否使用COMMAND_START的前缀")
    mmm_text_start: set[str] = Field(
        default_factory=lambda: {
            "",
        },
        description="文本消息的开头",
    )
    mmm_lstrip: bool = Field(default=False, description="是否去除消息开头字符")
    mmm_lstrip_num: int = Field(default=1, ge=1, description="去除消息开头字符的数量")


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

cmd_start_tuple = tuple(get_driver().config.command_start if config.mmm_use_nb_start else config.mmm_text_start)
cmd_start = " ".join(cmd_start_tuple)


@get_driver().on_shutdown
async def cancel_tasks():
    for task in tasks:
        if not task.done():
            task.cancel()

    await asyncio.gather(
        *(asyncio.wait_for(task, timeout=10) for task in tasks),
        return_exceptions=True,
    )


def push_event(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent]):
    message = event.message
    if config.mmm_only_text and not message.only("text"):
        # 只处理文本消息 and 不是纯文本消息
        return

    if config.mmm_text_check and message.has("text") and (text_message := message[0]).type == "text":
        text = str(text_message)

        if not text.startswith(cmd_start_tuple):
            return

        if config.mmm_lstrip:
            message[0] = MessageSegment.text(
                text[: config.mmm_lstrip_num].lstrip(cmd_start) + text[config.mmm_lstrip_num :]
            )

    task = asyncio.create_task(bot.handle_event(event))
    task.add_done_callback(tasks.discard)
    tasks.add(task)
    return event


@on("message_sent", block=config.mmm_block, priority=config.mmm_priority).handle()
async def patch_event(event: Event, bot: Bot):
    data = model_dump(event)
    if data.get("message_type") == "private":
        if not config.mmm_private:
            return
        if str(data.get("target_id")) == bot.self_id and not config.mmm_self:
            return
        data["post_type"] = "message"
        return push_event(bot, type_validate_python(PrivateMessageEvent, data))
    elif data.get("message_type") == "group":
        if not config.mmm_group:
            return
        data["post_type"] = "message"
        return push_event(bot, type_validate_python(GroupMessageEvent, data))


@Bot.on_calling_api
async def patch_send(bot: Bot, api: str, data: dict[str, Any]):
    """避免在PrivateMessageEvent事件中发消息时发给自己..."""
    if api not in ["send_msg", "send_private_msg"]:
        return
    try:
        event = current_event.get()
    except LookupError:
        return
    if not isinstance(event, PrivateMessageEvent) or event.self_id != event.user_id:
        return
    data["user_id"] = getattr(event, "target_id", event.user_id)
