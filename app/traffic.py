import json
from nonebot import on_command, CommandSession
import time
import requests

import re



'''使用格式说明：

    回城 [时间][日期]-> 那一天（休假或者工作日）从xx:xx开始的出行方式
    日期 : (工作日|休假日|周末|..) 默认为当天
    时间 : (xx:xx) 默认为当前
    
'''
@on_command('traffic', aliases=('去四平', '回城', '进城'))
async def traffic(session: CommandSession):
    #plan_time = session.get('time', prompt='几点出发？')
    #workday_tag = session.get('is_worday', prompt='是工作日吗？[Y/n]') == 'Y' or 'y'
    traffic_plan = await get_traffic_plan(session.state['plan_time'], session.state['workday_tag'])
    await session.send(traffic_plan)


# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@traffic.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    arg = session.current_arg_text.strip()
    local_time = time.localtime()
    plan_date = time.strftime("%Y%m%d", local_time)
    workday_tag = await is_workday(plan_date)
    plan_time = time.strftime("%H:%M", local_time)

    # 然而实际上pm_tag并没有作用，咕咕咕
    pm_tag = False
    workday_tag = True

    #时间
    arg = arg.replace('：', ':')
    if '下午' in arg:
        pm_tag = True
        arg = arg.replace('下午', '')
    search_2 = re.search(r'\d{2}:\d{2}', arg)
    if search_2:
        plan_time = search_2.group()
    else:
        search_1 = re.search(r'\d:\d{2}', arg)
        if search_1:
            plan_time = '0' + search_1.group()
    for tag in ('工作日',):
        if tag in arg:
            workday_tag = True
    for tag in ('休息日', '休息', '休假日', '休假', '节假日', '放假', '周末', '假期'):
        if tag in arg:
            workday_tag = False

    session.state['plan_time'] = plan_time
    session.state['workday_tag'] = workday_tag
    return plan_time, workday_tag




async def is_workday(date: str) -> bool:
    url = 'http://api.goseek.cn/Tools/holiday?date' + date
    res = requests.get(url)
    result = json.loads(res.text)
    return result["data"] in (0, 2)


async def get_traffic_plan(departure_time: str, is_workday: bool) -> str:
    holiday_show = '工作日' if is_workday else '休假日'
    w = f'{departure_time} {holiday_show}'
    for traffic_way, traffic_info in traffic_table.items():
        current = []
        time_tuple = traffic_info['timetable']['workday' if is_workday else 'holiday']['departure']
        for t in time_tuple:
            if t > departure_time:
            #直接字典序
            #if time.strptime(t, '%H:%M') > time.strptime(departure_time, '%H:%M'):
                current.append(t)
        if current:
            times = ' '.join(current)
            w += f'\n{traffic_way} {times}'
    return w


traffic_table = {
    '教师班车中环': {
        'info': '同心云预约（中环直达）',
        'price': '元',
        'address': 'F楼',
        'timetable': {'workday': {'departure': (
        '06:40', '08:00', '10:00', '14:00', '15:30', '16:30',
        '17:20'),
            'return': ('06:45', '07:05', '08:00', '08:45', '10:00', '12:05', '14:00','15:30', '16:40', '17:20')
        },
            'holiday':{'departure':(), 'return': ()}
        }
    },
    '教师班车内环': {
        'info': '同心云预约（内环）',
        'price': '元',
        'address': 'F楼',
        'timetable': {'workday': {'departure': (
            '12:15', '20:05', '20:50', '21:40'),
            'return': ('12:15',)
        },
            'holiday': {'departure': ('16:30',), 'return': ('7:00')}
        }
    },
    '北安跨': {
        'info': '北安跨',
        'price': '2元',
        'address': '南门外',
        'timetable': {'workday': {'departure': (
        '06:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '15:30', '16:00', '16:45',
        '17:30', '18:00', '19:00', '20:00', '20:50'),
                                  'return': ()},
                      'holiday': {'departure': (
                      '06:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '15:30', '16:00',
                      '16:45', '17:30', '18:00', '19:00', '20:00', '20:50'),
                                  'return': ()}}},
    '定班车': {
        'info': '定班车刷学生卡',
        'price': '10元',
        'address': '广楼南侧',
        'timetable': {
            'workday': {'departure': ('06:30', '12:15', '16:30'),
                        'return': ('08:45', '14:00', '20:30')},
            'holiday': {'departure': ('07:00', '12:15'),
                        'return': ('11:00', '17:00')}}},
    '昌吉东路短驳车': {
        'info': '11号线昌吉东路',
        'price': '2+7元',
        'address': '北门口',
        'timetable': {'workday': {'departure': (
            '06:15', '06:35', '06:55', '07:15', '07:35', '07:55', '08:15', '08:35', '09:10', '10:10', '11:10', '12:15', '13:15',
            '14:15', '15:15', '16:15', '17:15', '18:15', '19:15', '19:45', '20:15'),
            'return': (
                '06:25', '06:45', '07:05', '07:25', '07:45', '08:05', '08:25', '09:00', '10:00', '11:00',
                '12:05', '13:05', '14:05', '15:05', '16:05', '17:05', '18:05', '19:05', '19:35')},
            'holiday': {'departure': (
                '06:15', '06:35', '06:55', '07:15', '07:35', '07:55', '08:15', '08:35', '09:10', '10:10', '11:10', '12:15',
                '13:15', '14:15', '15:15', '16:15', '17:15', '18:15', '19:15', '19:45', '20:15'),
                'return': (
                    '06:25', '06:45', '07:05', '07:25', '07:45', '08:05', '08:25', '09:00', '10:00', '11:00',
                    '12:05', '13:05', '14:05', '15:05', '16:05', '17:05', '18:05', '19:05', '19:35')}
        },
    },
    '上海汽车城短驳车': {
        'info': '11号线上海汽车城',
        'price': '2+7元',
        'address': '嘉三路7号楼',
        'timetable': {'workday': {'departure': (
            '06:15', '06:30', '06:45', '07:00', '07:20', '07:40', '08:00', '08:30', '09:00', '09:50', '10:50', '11:50', '12:30',
            '13:00', '13:35', '14:05', '14:35', '15:35', '16:35', '17:15', '17:45', '18:15', '19:25', '20:45', '21:25',
            '22:00'),
            'return': (
                '06:30', '06:45', '70:00', '07:15', '07:35', '07:55', '08:15', '08:45', '09:15', '10:05',
                '11:05', '12:05', '12:45', '13:15', '13:50', '14:20', '14:50', '15:50', '16:50',
                '17:30', '18:00', '18:30', '19:00', '19:40', '20:20', '21:00', '21:40', '22:15')},
            'holiday': {'departure': (
                '06:30', '06:45', '07:00', '07:20', '07:40', '08:00', '08:30', '09:00', '09:50', '10:50', '11:50', '12:30',
                '13:00', '13:35', '14:05', '14:35', '16:35', '17:15', '17:45', '18:15', '19:25', '20:45',
                '21:25',),
                'return': (
                    '06:45', '07:00', '07:15', '07:35', '07:55', '08:15', '08:45', '09:15', '10:05', '11:05',
                    '12:05', '12:45', '13:15', '13:50', '14:20', '14:50', '16:50', '17:30', '18:00',
                    '18:30', '19:00', '19:40', '20:20', '21:00', '21:40')}
        }
    }

}
