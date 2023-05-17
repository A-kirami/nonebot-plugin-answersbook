import random
from pathlib import Path

from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State


default_start: str = list(get_driver().config.command_start)[0]
__plugin_meta__ = PluginMetadata(
    name='答案之书',
    description='这是一本治愈系的心灵解惑书，它将带给你的不止是生活的指引，还有心灵的慰藉。',
    usage=(
        f'· {default_start}翻看答案 <问题>  # 翻看这个问题的答案\n'
        f'· <回复一条消息> 翻看答案  # 翻看这个问题的答案\n'
    )
)
answers_path: Path = Path(__file__).parent / "answersbook.txt"
answers: list[str] = answers_path.read_text("utf-8").splitlines()


def get_answers() -> str:
    return random.choice(answers)


look_answer = on_command("翻看答案")


@look_answer.handle()
async def answersbook(state: T_State,
                      event: MessageEvent,
                      command_arg: Message = CommandArg()) -> None:
    state['user_id'] = event.user_id
    if event.original_message[0].type == 'reply':
        state['reply'] = event.original_message[0].data['id']
        state['question'] = True
    if command_arg.extract_plain_text():
        state['question'] = True


@look_answer.got('question', prompt=Message.template('{user_id:at}你想问什么问题呢？'))
async def anwsersbook(state: T_State, event: MessageEvent) -> None:
    answer: str = get_answers()
    if 'reply' in state:
        reply: int = state['reply']
    else:
        reply = event.message_id
    await look_answer.finish(Message([MessageSegment.reply(reply),
                                      MessageSegment.at(event.user_id),
                                      MessageSegment.at(event.user_id),
                                      MessageSegment.text(answer)]))
