from nonebot import on_command, CommandSession
import base64
import random


# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('d', aliases=('随机', '生成随机数'))
async def get_random(session: CommandSession):
    # 获取城市的天气预报
    seed = session.get('seed', prompt='参数?')
    result = await go_random(seed)
    # 向用户发送天气预报
    await session.send(result)
@get_random.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['seed'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('指令错误，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg

async def go_random(seed:str):

	temp=seed.split(' ')
	q=''
	w=''
	sed=0
	if len(temp)==1:
		w=temp[0]
		t=base64.b64encode(temp[0].encode()).decode()
		for i in t:
			sed+=ord(i)
		random.seed(sed)
		q=random.randint(0,99)
	return f'由于{w}生成了  {q}'
