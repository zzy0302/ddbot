import time
import re
import requests
from collections import defaultdict
from nonebot import on_command, CommandSession
if __name__ == '__main__':
    S = '西南七202'


@on_command('Elec', aliases=('电费', '查电费', '我要查电费'))
async def weather(session: CommandSession):
    S = session.get('S', prompt='你想查询哪个宿舍的电费呢？')
    elec_report = await elec(S, session.ctx['user_id'])
    await session.send(elec_report)


@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['S'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的寝室不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def elec(S: str, qq) -> str:
    try:
        r = requests.get(
            'http://pc.washingpatrick.cn:2345/elec?room='+S+'&qq='+str(qq))
        if r.status_code == 200:
            temp = r.content.split()[-1].decode()
            return f'{S} \n剩余电量: {temp} 度'
        else:
            return '查询失败，请换关键词'
    except Exception as e:
        print(e)
        return '查询失败，请换关键词'
