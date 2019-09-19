from nonebot import on_command, CommandSession
from urllib import parse

@on_command('baidu', aliases=('baidu', '百度', '百度搜','搜'))
async def getpcip(session: CommandSession):
    await session.send("http://baidu.washingpatrick.cn?"+parse.quote(session.current_arg_text.strip()))
