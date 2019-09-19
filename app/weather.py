from nonebot import on_command, CommandSession
from urllib import parse
import json
import requests
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    # 获取城市的天气预报
    weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    await session.send(weather_report)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def get_weather_of_city(city: str) -> str:

    url = 'https://free-api.heweather.com/s6/weather/forecast?key=b72c096413d24bd7935fe23a35894abb&location='+parse.quote(city)
    # print(url)
    res = requests.get(url)
    result = json.loads(res.text)
    w = ''
    if result['HeWeather6'][0]['status'] == 'ok' :
        w += '更新时间: ' + ' '.join(result['HeWeather6'][0]['update']['loc'].split('-'))
        if result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d'] == result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n']:
            w += '\n今日天气:  ' + result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d']
        else:
            w += '\n今日天气:  ' + result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d'] + ' 转 '+ result['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n']
        w += '\n气温 ' + result['HeWeather6'][0]['daily_forecast'][0]['tmp_min'] + ' ~ ' + result['HeWeather6'][0]['daily_forecast'][0]['tmp_max'] + ' 度'
        w += '\n有 ' + result['HeWeather6'][0]['daily_forecast'][0]['wind_sc'] + ' 级 ' + result['HeWeather6'][0]['daily_forecast'][0]['wind_dir']
        w += '\n紫外线指数: ' + result['HeWeather6'][0]['daily_forecast'][0]['uv_index']
        if result['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d'] == result['HeWeather6'][0]['daily_forecast'][1]['cond_txt_n']:
            w += '\n明日预报:  ' + result['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d']
        else:
            w += '\n明日预报:  ' + result['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d'] + ' 转 '+ result['HeWeather6'][0]['daily_forecast'][1]['cond_txt_n']
        w += '\n气温 ' + result['HeWeather6'][0]['daily_forecast'][1]['tmp_min'] + ' ~ ' + result['HeWeather6'][0]['daily_forecast'][1]['tmp_max'] + ' 度'
        w += '\n有 ' + result['HeWeather6'][0]['daily_forecast'][1]['wind_sc'] + ' 级 ' + result['HeWeather6'][0]['daily_forecast'][1]['wind_dir']
        w += '\n紫外线指数: ' + result['HeWeather6'][0]['daily_forecast'][1]['uv_index']
    else:
        w += '查询错误或达到上限，请稍后再试'
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    return f'{city}\n{w}'