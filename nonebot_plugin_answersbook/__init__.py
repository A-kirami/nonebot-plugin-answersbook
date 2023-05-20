import random
from collections.abc import Callable
from pathlib import Path

from nonebot import on_message
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.params import EventPlainText
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

__plugin_meta__ = PluginMetadata(
    name="答案之书",
    description="这是一本治愈系的心灵解惑书，它将带给你的不止是生活的指引，还有心灵的慰藉。",
    usage=("· 翻看答案 <问题>  # 翻看这个问题的答案\n· <回复一条消息> 翻看答案  # 翻看这个问题的答案\n"),
)

answers_path = Path(__file__).parent / "answersbook.txt"
answers = answers_path.read_text("utf-8").splitlines()


def startswith_or_endswith(msg: str) -> Callable[[str], bool]:
    def rule(message: str = EventPlainText()) -> bool:
        return message.startswith(msg) or message.endswith(msg)

    return rule


look_answer = on_message(rule=startswith_or_endswith("翻看答案"))


@look_answer.handle()
async def answersbook(
    event: MessageEvent, state: T_State, message: str = EventPlainText()
) -> None:
    state["user_id"] = event.user_id
    if event.reply or message.strip() != "翻看答案":
        state["question"] = True


@look_answer.got("question", prompt=Message.template("{user_id:at}你想问什么问题呢？"))
async def question(event: MessageEvent) -> None:
    reply_id = event.reply.message_id if event.reply else event.message_id
    await look_answer.finish(
        MessageSegment.reply(reply_id)
        + MessageSegment.at(event.user_id)
        + MessageSegment.text(random.choice(answers))
    )
