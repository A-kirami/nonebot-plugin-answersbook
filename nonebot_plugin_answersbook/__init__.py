import random
from pathlib import Path

from nonebot import get_driver, on_keyword
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.params import EventPlainText
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule
from nonebot.typing import T_State

default_start: str = tuple(get_driver().config.command_start)[0]
__plugin_meta__ = PluginMetadata(
    name='答案之书',
    description='这是一本治愈系的心灵解惑书，它将带给你的不止是生活的指引，还有心灵的慰藉。',
    usage=(
        f'· {default_start}翻看答案 <问题>  # 翻看这个问题的答案\n'
        f'· <回复一条消息> 翻看答案  # 翻看这个问题的答案\n'
    )
)
answers_path: Path = Path(__file__).parent / 'answersbook.txt'
answers: list[str] = answers_path.read_text('utf-8').splitlines()


def get_answer() -> str:
    return random.choice(answers)


@Rule
def startswith_or_endswith(message: str = EventPlainText()) -> bool:
    return message.startswith('翻看答案') or message.endswith('翻看答案')


look_answer = on_keyword({'翻看答案'}, rule=startswith_or_endswith)


@look_answer.handle()
async def answersbook(state: T_State,
                      event: MessageEvent,
                      message: str = EventPlainText()) -> None:
    state['user_id'] = event.user_id
    if event.reply is not None:
        state['reply'] = event.reply
        state['question'] = True
    elif message.replace('翻看答案', '').replace(' ', ''):
        state['question'] = True


@look_answer.got('question', prompt=Message.template('{user_id:at}你想问什么问题呢？'))
async def anwsersbook(state: T_State, event: MessageEvent) -> None:
    answer: str = get_answer()
    reply = state['reply'].message_id if 'reply' in state else event.message_id
    await look_answer.finish(Message([MessageSegment.reply(reply),
                                      MessageSegment.at(event.user_id),
                                      MessageSegment.at(event.user_id),
                                      MessageSegment.text(answer)]))
