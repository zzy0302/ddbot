import time
import re
import requests
from collections import defaultdict
from nonebot import on_command, CommandSession


@on_command('Elec', aliases=('电费', '电量', '查电费', '查电量', '剩余电量', '剩余电费', '我要查电费','查询电费','查询电量'), only_to_me=False)
async def elec(session: CommandSession):
    S = session.get('S')
    elec_report = await elec(S, session.ctx['user_id'])
    await session.send(elec_report)


@elec.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['S'] = stripped_arg
    if not stripped_arg:
        session.state['S'] = ''
    return


async def elec(S: str, qq) -> str:
    # try:
    #     r = requests.get(
    #         'http://pc.washingpatrick.cn:2345/elec?room='+S+'&qq='+str(qq))
    #     if r.status_code == 200:
    #         temp = r.content.split()[-1].decode()
    #         if S == '':
    #             S = '上次查询宿舍:'
    #         return f'{S} \n剩余电量: {temp} 度'
    #     else:
    #         return '查询失败，请换关键词'
    # except Exception as e:
    #     print(e)
    #     return '查询失败，请换关键词'
    return '由于主人毕业，该功能已下线'
