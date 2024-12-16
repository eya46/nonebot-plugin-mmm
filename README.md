<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Plugin MMM

![License](https://img.shields.io/github/license/eya46/nonebot-plugin-mmm)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![NoneBot](https://img.shields.io/badge/nonebot-2.3.0+-red.svg)
<a href="https://pypi.org/project/nonebot-plugin-mmm/">
<img src="https://img.shields.io/pypi/v/nonebot-plugin-mmm?logo=python&logoColor=edb641" alt="pypi">
</a>
</div>

<div align="center">

![:eya46](https://count.getloli.com/get/@:eya46-plugin-mmm?theme=gelbooru)

</div>

## 作用

让 `onebot v11` 协议中 `bot` 的消息作为正常事件进行处理

> 使用 `plugin-alconna` 记得添加 `ALCONNA_RESPONSE_SELF=True` 配置
>
> 原因: https://github.com/nonebot/plugin-alconna/releases/tag/v0.53.0

## 注意事项

> [!WARNING]
> - 小心死循环！
> - 在 `PrivateMessageEvent` 事件中, 使用 `send_msg` 给bot自己发消息会重定向到 `target_id`(如果存在的话)
    (👆请使用 `send_private_msg` 给bot自己发消息)
>

## 安装方式

### 依赖管理

- `pip install nonebot-plugin-mmm`
- `poetry add nonebot-plugin-mmm`
- `pdm add nonebot-plugin-mmm`

> 在 `bot.py` 中添加 `nonebot.load_plugin("nonebot_plugin_mmm")`

### nb-cli

- `nb plugin install nonebot-plugin-mmm`

## 配置项

### 非必要配置项

- `mmm_block`: 是否block `message_sent` 后续matcher, 默认为 `True`
- `mmm_priority`: on `message_sent` 的优先级, 默认为 `0`
- `mmm_private`: 是否处理私聊消息, 默认为 `True`
- `mmm_group`: 是否处理群聊消息, 默认为 `True`
- `mmm_self`: 是否处理自己发给自己的消息, 默认为 `False`
- `mmm_only_text`: 是否只处理文本消息, 默认为 `False`
- `mmm_text_check`: 是否只处理符合指定开头的消息, 默认为 `False`
- `mmm_use_nb_start` 是否使用 `nonebot2` 的 `COMMAND_START`, 默认为 `False`
- `mmm_text_start`: 检查的消息开头, 默认为 `{"",}` 即任何消息都通过
- `mmm_lstrip`: 是否去除消息前缀, 默认为 `False`
- `mmm_lstrip_num`: 去除消息前缀的数量, 默认为 `1`

```toml
mmm_block = True
mmm_priority = 0
mmm_private = True
mmm_group = True
mmm_self = False

mmm_only_text = False # 只处理文本消息
mmm_text_check = False # 只处理符合指定开头的消息
mmm_use_nb_start = False # 使用 nonebot2 的 COMMAND_START
mmm_text_start = [".", "/"] # 检查的消息开头 默认为 ["",] 即任何消息都通过
mmm_lstrip = False # 去除消息前缀
mmm_lstrip_num = 1 # 去除消息前缀的数量
```

## 依赖项

```toml
python = "^3.9"
nonebot2 = "^2.3.0"
nonebot-adapter-onebot = "^2.1.0"
```
