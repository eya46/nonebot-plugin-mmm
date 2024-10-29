<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Plugin MMM

![License](https://img.shields.io/github/license/eya46/nonebot-plugin-mmm)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![NoneBot](https://img.shields.io/badge/nonebot-2.3.0+-red.svg)
</div>

<div align="center">

![:eya46](https://count.getloli.com/get/@:eya46-plugin-mmm?theme=gelbooru)

</div>

## 作用

让 `onebot v11` 协议中 `bot` 的消息作为正常事件进行处理
> 小心死循环!

> 使用 `plugin-alconna` 记得添加 `ALCONNA_RESPONSE_SELF=True` 配置
>
> 原因: https://github.com/nonebot/plugin-alconna/releases/tag/v0.53.0

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

- `mmm_block`: 是否block `message_sent` 后续matcher
- `mmm_priority`: on `message_sent` 的优先级

## 依赖项

```toml
python = "^3.9"
nonebot2 = "^2.3.0"
nonebot-adapter-onebot = "^2.1.0"
```
