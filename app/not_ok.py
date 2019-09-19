from nonebot import on_command, CommandSession
from urllib import parse

@on_command('not_ok', aliases=('彳亍', '好', '行'))
async def getpcip(session: CommandSession):
    await session.send('不彳亍')
