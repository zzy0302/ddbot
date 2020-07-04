from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.select import Select
from ChromePool import chromepool
from collections import defaultdict
from nonebot import on_command, CommandSession
import pymysql
import re
import time
import datetime
import flask


URL = 'http://202.120.163.129:88/'

Black_Hole = '博士留学南北朋'
SELECTORS = ['drlouming', 'drceng', 'dr_ceng', 'drfangjian']

buildings_map = {'西南一号楼': {'belong': '四平路校区ISIMS',
                           'include': ['西南一号楼公用', '西南一号楼4层', '西南一号楼1001-1099', '西南一号楼1100-1199', '西南一号楼2001-2099',
                                       '西南一号楼2100-2199', '西南一号楼3000-3099', '西南一号楼3100-3199']},
                 '西北二号楼': {'belong': '四平路校区ISIMS', 'include': ['西北二号楼1层', '西北二号楼2层', '西北二号楼3层', '西北二号楼4层', '西北二号楼公用']},
                 '学三楼': {'belong': '四平路校区ISIMS', 'include': ['学三楼1层', '学三楼2层', '学三楼3层', '学三楼4层', '学三楼5层', '学三楼6层']},
                 '学四楼': {'belong': '四平路校区ISIMS', 'include': ['学四楼1层', '学四楼2层', '学四楼3层', '学四楼4层', '学四楼5层', '学四楼6层']},
                 '学五楼': {'belong': '四平路校区ISIMS', 'include': ['学五楼1层', '学五楼2层', '学五楼3层', '学五楼4层', '学五楼公用', '学五楼控制端']},
                 '西南7号楼': {'belong': '四平路校区ISIMS',
                           'include': ['西南7号楼1层', '西南7号楼2层', '西南7号楼3层', '西南7号楼4层', '西南7号楼5层', '西南7号楼6层', '西南7号楼公用部分',
                                       '西南7号楼控制']},
                 '西南8号楼': {'belong': '四平路校区ISIMS',
                           'include': ['西南8号楼1层', '西南8号楼2层', '西南8号楼3层', '西南8号楼4层',
                                       '西南8号楼5层', '西南8号楼6层', '西南8号楼公用备用',
                                       '西南8号楼控制端']},
                 '西南9号楼': {'belong': '四平路校区ISIMS',
                           'include': ['西南9号楼1层', '西南9号楼2层', '西南9号楼3层', '西南9号楼4层', '西南9号楼5层', '西南9号楼6层', '西南9号楼公用备用',
                                       '西南9号楼控制']},
                 '西南十号楼': {'belong': '四平路校区ISIMS', 'include': ['西南十号楼1层', '西南十号楼2层', '西南十号楼3层', '西南十号楼4层', '西南十号楼公用']},
                 '西南十一号楼': {'belong': '四平路校区ISIMS',
                            'include': ['西南十一号楼11号楼1层', '西南十一号楼11号楼2层', '西南十一号楼11号楼3层', '西南十一号楼11号楼4层', '西南十一号楼公用']},
                 '西南十二号楼': {'belong': '四平路校区ISIMS',
                            'include': ['西南十二号楼1层', '西南十二号楼2层', '西南十二号楼3层', '西南十二号楼4层', '西南十二号楼5层', '西南十二号楼6层']},
                 '西北一号楼': {'belong': '四平路校区ISIMS', 'include': ['1F', '2F', '3F', '4F', '公用']},
                 '西南二号楼': {'belong': '四平路校区ISIMS',
                           'include': ['西南二号楼1层', '西南二号楼2层', '西南二号楼3层', '西南二号楼4层', '西南二号楼5层', '西南二号楼6层', '西南二号楼公用']},
                 '西南三号楼': {'belong': '四平路校区ISIMS', 'include': ['西南三号楼2层', '西南三号楼3层', '西南三号楼4层', '西南三号楼5层']},
                 '青年楼': {'belong': '四平路校区ISIMS', 'include': ['1F', '2F', '公用']},
                 '解放楼': {'belong': '四平路校区ISIMS', 'include': ['1F', '2F', '公用']},
                 '南校区后勤公寓': {'belong': '四平路校区ISIMS', 'include': ['2F', '公用']},
                 '本部后勤公寓': {'belong': '四平路校区ISIMS', 'include': ['1F', '2F', '公用']},
                 '博士生3号楼': {'belong': '四平路校区ISIMS',
                            'include': ['博士生3号楼1层',
                                        '博士生3号楼2层',
                                        '博士生3号楼3层',
                                        '博士生3号楼4层',
                                        '博士生3号楼5层',
                                        '博士生3号楼6层',
                                        '博士生3号楼7层',
                                        '博士生3号楼8层',
                                        '博士生3号楼9层',
                                        '博士生3号楼10层',
                                        '博士生3号楼11层',
                                        '博士生3号楼12层',
                                        '博士生3号楼13层',
                                        '博士生3号楼14层',
                                        '博士生3号楼15层',
                                        '博士生3号楼16层',
                                        '博士生3号楼17层',
                                        '博士生3号楼18层',
                                        '博士生3号楼控制']},
                 '西北3号楼': {'belong': '四平路校区ISIMS',
                           'include': ['西北3号楼1层', '西北3号楼2层', '西北3号楼3层', '西北3号楼4层', '西北3号楼5层', '西北3号楼6层', '西北三号楼公用']},
                 '西北4号楼': {'belong': '四平路校区ISIMS',
                           'include': ['西北4号楼1层', '西北4号楼2层', '西北4号楼3层', '西北4号楼4层', '西北4号楼5层', '西北4号楼6层', '西北四号楼公用']},
                 '西北5号楼': {'belong': '四平路校区ISIMS',
                           'include': ['西北5号楼1层', '西北5号楼2层', '西北5号楼3层', '西北5号楼4层', '西北5号楼5层', '西北5号楼6层', '西北五号楼公用']},
                 '博士生4号楼': {'belong': '四平路校区ISIMS',
                            'include': ['博士生4号楼1层', '博士生4号楼2层', '博士生4号楼3层', '博士生4号楼4层', '博士生4号楼5层', '博士生4号楼6层',
                                        '博士生4号楼7层', '博士生4号楼8层', '博士生4号楼9层', '博士生4号楼10层', '博士生4号楼11层', '博士生4号楼12层',
                                        '博士生4号楼13层', '博士生4号楼14层', '博士生4号楼15层', '博士生4号楼16层', '博士生4号楼17层', '博士生4号楼18层',
                                        '博士生4号楼控制']}, '留学生1号楼': {'belong': '四平路校区ISIMS',
                                                                 'include': ['留学生1号楼1F', '留学生1号楼2F', '留学生1号楼3F',
                                                                             '留学生1号楼4F', '留学生1号楼5F', '留学生1号楼6F',
                                                                             '留学生1号楼7F', '留学生1号楼8F', '留学生1号楼9F',
                                                                             '留学生1号楼10F', '留学生1号楼11F', '留学生1号楼12F',
                                                                             '留学生1号楼公用']},
                 '留学生2号楼': {'belong': '四平路校区ISIMS',
                            'include': ['留学生2号楼1F', '留学生2号楼2F', '留学生2号楼3F', '留学生2号楼4F', '留学生2号楼5F', '留学生2号楼公用']},
                 '博士生5号楼': {'belong': '四平路校区ISIMS',
                            'include': ['博士生5号楼1层', '博士生5号楼2层', '博士生5号楼3层', '博士生5号楼4层', '博士生5号楼5层', '博士生5号楼6层',
                                        '博士生5号楼7层', '博士生5号楼8层', '博士生5号楼9层', '博士生5号楼10层', '博士生5号楼11层', '博士生5号楼12层',
                                        '博士生5号楼13层', '博士生5号楼14层', '博士生5号楼15层', '博士生5号楼控制']},
                 '行政南楼': {'belong': '四平路校区ISIMS', 'include': ['行政南楼1层', '行政南楼2层', '行政南楼3层', '行政南楼4层', '行政南楼5层']},
                 '行政北楼': {'belong': '四平路校区ISIMS', 'include': ['行政北楼1层', '行政北楼2层', '行政北楼3层', '行政北楼4层', '行政北楼5层']},
                 '07号公寓    ': {'belong': '嘉定校区SIMS',
                               'include': ['一层        ', '二层        ', '备用        ', '三层        ', '四层        ',
                                           '五层        ', '备用1       ', '六层        ']},
                 '08号公寓    ': {'belong': '嘉定校区SIMS',
                               'include': ['一层        ', '二层        ', '三层        ', '四层        ', '五层        ',
                                           '六层        ', '0           ']}, '09号公寓    ': {'belong': '嘉定校区SIMS',
                                                                                         'include': ['一层        ',
                                                                                                     '二层        ',
                                                                                                     '三层        ',
                                                                                                     '四层        ',
                                                                                                     '五层        ',
                                                                                                     '六层        ']},
                 '10号公寓    ': {'belong': '嘉定校区SIMS',
                               'include': ['一层        ', '二层        ', '三层        ', '四层        ', '五层        ',
                                           '六层        ']}, '14号公寓    ': {'belong': '嘉定校区SIMS',
                                                                         'include': ['一层        ', '二层        ',
                                                                                     '三层        ', '四层        ',
                                                                                     '五层        ', '六层        ',
                                                                                     '七层        ', '备用1       ',
                                                                                     '备用        ']},
                 '12号公寓    ': {'belong': '嘉定校区SIMS',
                               'include': ['一层        ', '二层        ', '三层        ', '四层        ', '五层        ',
                                           '六层        ', '七层        ']},
                 '15号公寓    ': {'belong': '嘉定校区SIMS',
                               'include': ['一层        ',
                                           '二层        ',
                                           '三层        ',
                                           '四层        ',
                                           '五层        ',
                                           '六层        ',
                                           '七层        ']},
                 '13号公寓    ': {'belong': '嘉定校区SIMS',
                               'include': ['一层        ', '二层        ', '三层        ', '四层        ', '五层        ',
                                           '六层        ', '七层        ']},
                 '16号公寓    ': {'belong': '嘉定校区SIMS', 'include': ['3单元       ', '2单元       ', '1单元       ']},
                 '17号公寓    ': {'belong': '嘉定校区SIMS', 'include': ['1单元       ', '2单元       ', '3单元       ']},
                 '18号公寓    ': {'belong': '嘉定校区SIMS', 'include': ['1单元       ', '2单元       ']},
                 '友园2号楼': {'belong': '嘉定校区ISIMS', 'include': ['1F', '2F', '3F', '4F', '5F', '公用']},
                 '友园3号楼': {'belong': '嘉定校区ISIMS', 'include': ['2F', '3F', '4F', '5F']},
                 '友园4号楼': {'belong': '嘉定校区ISIMS', 'include': ['2F', '3F', '4F', '5F', '6F']},
                 '友园5号楼': {'belong': '嘉定校区ISIMS',
                           'include': ['1F', '2F', '3F', '4F', '5F', '6F']},
                 '友园6号楼': {'belong': '嘉定校区ISIMS', 'include': ['2F', '3F', '4F', '5F', '6F', '公用']},
                 '19号楼': {'belong': '嘉定校区ISIMS',
                          'include': ['1F', '2F', '3F', '4F', '5F', '6F']},
                 '20号楼': {'belong': '嘉定校区ISIMS', 'include': ['1F', '2F', '3F', '4F', '5F', '6F']},
                 '朋园1号楼   ': {'belong': '嘉定朋园',
                              'include': ['1层         ', '2层         ', '3层         ', '4层         ', '5层         ',
                                          '6层         ']}, '朋园2号楼   ': {'belong': '嘉定朋园',
                                                                        'include': ['1层         ', '2层         ',
                                                                                    '3层         ', '4层         ',
                                                                                    '5层         ', '6层         ']},
                 '朋园3号楼   ': {'belong': '嘉定朋园',
                              'include': ['1层         ', '2层         ', '3层         ', '4层         ', '5层         ',
                                          '6层         ']}, '朋园4号楼   ': {'belong': '嘉定朋园',
                                                                        'include': ['1层         ', '2层         ',
                                                                                    '3层         ', '4层         ',
                                                                                    '5层         ', '6层         ']},
                 '朋园5号楼   ': {'belong': '嘉定朋园',
                              'include': ['1层         ', '2层         ', '3层         ', '4层         ', '5层         ',
                                          '6层         ', '7层         ', '8层         ', '9层         ']}}


num_map = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十',
           11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五', 16: '十六', 17: '十七', 18: '十八', 19: '十九', 20: '二十'}


options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
chrome_pool = chromepool(options=options, maxsize=10, timeout=5)


def get_left_eletr(params: list):
    _temp = chrome_pool.get()
    while type(_temp) == bool:
        _temp = chrome_pool.get()
    _temp.get(URL)
    for selector, param in zip(SELECTORS, params):
        Select(_temp.find_element_by_name(selector)
               ).select_by_visible_text(param)
    _temp.find_element_by_id('buyR').click()
    _temp.find_element_by_id('ImageButton1').click()
    res = _temp.find_element_by_tag_name(
        'h6').find_element_by_tag_name('span').text
    # browser.close()
    _temp.delete_all_cookies()
    chrome_pool.release(_temp)
    return res


CN_NUM = {
    '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
}

CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}


def chinese_to_arabic(cn: str):
    unit = 0   # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val


def fuck_xn1(num):
    if num[:2] == '10' or num[:2] == '20':
        return num[:2]+'01-'+num[:2]+'99'
    else:
        return num[:2]+'00-'+num[:2]+'99'


def ai_get_number(S):
    # print(re.findall('(\d+)$',S))
    number = re.findall('(\d+)$', S)[0]
    building = S.replace(str(number), '')
    building = building.replace(' ', '')
    return [building, number]
    # print(re.findall('^(.+?(\..+?)*)$',S))


def get_info(S):
    # sample 西南七 233
    ai_get_number(S)
    ans = []
    temp = ai_get_number(S)
    # print(temp)
    temp[0] = temp[0].replace('号', '').replace('楼', '')
    for key, value in buildings_map.items():
        if temp[0] in key:
            flag = 0
            for i in Black_Hole:
                if (i in temp[0] and i not in key) or (i in key and i not in temp[0]):
                    flag = 1
            if flag == 1:
                continue
            ans.append(value['belong'])
            ans.append(key)
            break
    if len(ans) == 0:
        if re.findall('\d+', temp[0]):
            temp[0] = temp[0].replace(str(re.findall(
                '\d+', temp[0])[0]), str(num_map[int(re.findall('\d+', temp[0])[0])]))
        for key, value in buildings_map.items():
            if temp[0] in key:
                flag = 0
                for i in Black_Hole:
                    if (i in temp[0] and i not in key) or (i in key and i not in temp[0]):
                        flag = 1
                if flag == 1:
                    continue
                ans.append(value['belong'])
                ans.append(key)
                break
    if len(ans) == 0:
        if re.findall('(一|二|三|四|五|六|七|八|九|十)', temp[0]):
            # print(''.join(re.findall('(一|二|三|四|五|六|七|八|九|十)',temp[0])))
            temp[0] = temp[0].replace(''.join(re.findall('(一|二|三|四|五|六|七|八|九|十)', temp[0])), str(
                chinese_to_arabic(''.join(re.findall('(一|二|三|四|五|六|七|八|九|十)', temp[0])))))
            for key, value in buildings_map.items():
                if temp[0] in key:
                    flag = 0
                    for i in Black_Hole:
                        if (i in temp[0] and i not in key) or (i in key and i not in temp[0]):
                            flag = 1
                    if flag == 1:
                        continue
                    ans.append(value['belong'])
                    ans.append(key)
                    break
    # print( buildings_map[ans[1]])
    if ans[1] == '西南一号楼':
        ans.append(ans[1]+fuck_xn1(temp[1]))
        ans.append(ans[1]+temp[1])
    else:
        for i in buildings_map[ans[1]]['include']:
            if len(ans) == 4:
                break
           # print(re.findall('\d+',i))
            try:
                if re.findall('\d+', i)[-1] == temp[1][0]:
                    ans.append(i)
                    if '公寓' in ans[1]:
                        ans.append(temp[1])
                    elif '西北一' in ans[1]:
                        ans.append('西北1号楼'+temp[1])
                    elif '西北' in ans[1] and len(re.findall('\d', ans[1])) == 1:
                        temp_ans = ans[1].replace(str(re.findall(
                            '\d+', ans[1])[0]), str(num_map[int(re.findall('\d+', ans[1])[0])]))
                        ans.append(temp_ans+temp[1])
                    else:
                        ans.append(ans[1]+temp[1])
                    break
            except Exception:
                try:
                    # print(chinese_to_arabic(''.join(re.findall('(一|二|三|四|五|六|七|八|九|十)',i))),'????',temp[1][0])
                    if str(chinese_to_arabic(''.join(re.findall('(一|二|三|四|五|六|七|八|九|十)', i)))) == temp[1][0]:
                        ans.append(i)
                        if '公寓' in ans[1]:
                            ans.append(temp[1])
                        elif '西北一' in ans[1]:
                            ans.append('西北1号楼'+temp[1])
                        elif '西北' in ans[1] and len(re.findall('\d', ans[1])) == 1:
                            temp_ans = ans[1].replace(str(re.findall(
                                '\d+', ans[1])[0]), str(num_map[int(re.findall('\d+', ans[1])[0])]))
                            ans.append(temp_ans+temp[1])
                        else:
                            ans.append(ans[1]+temp[1])
                        break
                except Exception:
                    pass

# sample：['四平路校区ISIMS', '西南7号楼', '西南7号楼2层', '西南7号楼233']
    return ans


def cache(qq):
# TO-DO replace follow context
    db = pymysql.connect("localhost", "username", "userpassword", "tablename")
    cursor = db.cursor()
    try:
        db.set_charset('utf8')
        sql = "select * from `backend` where `room` = '%s' order by id desc limit 1" % (
            qq)
        cursor.execute(sql)
        data = cursor.fetchone()
        if (datetime.datetime.now()-data[3]).seconds > 180:
            return []
        else:
            return data[4]
    except Exception as e:
        print(e)
    db.close()


def qq2cache(qq):
    try:
        if not qq.isdigit:
            return False
    except Exception:
        return False
# TO-DO replace follow context
    db = pymysql.connect("localhost", "username", "userpassword", "tablename")
    cursor = db.cursor()
    try:
        db.set_charset('utf8')
        sql = "select room from backend where ip = '%s' order by id desc limit 1" % (
            qq)
        cursor.execute(sql)
        data = cursor.fetchone()
        db.close()
        if data:
           # print(list(filter(None, str(data)[2:-3].split(' '))))
            return list(filter(None, str(data)[2:-3].split(' ')))
        else:
            return False
    except Exception as e:
        db.close()
        print(e)
        return False


def log(qqq):
    # TO-DO replace follow context
    db = pymysql.connect("localhost", "username", "userpassword", "tablename")
    cursor = db.cursor()
    try:
        db.set_charset('utf8')
        sql = "insert into `backend` (`ip`,`room`,`elec`) values ('%s','%s','%s')" % (
            qqq['ip'], qqq['room'], qqq['elec'])
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    db.close()


def shouldCache(useCache, S):
    array = qq2cache(useCache)
    if S:
        array2 = get_info(S)
    else:
        array2 = []
    if array == array2 or array2 == []:
        if len(array) == 4:
            _temp = cache(' '.join(array))
            if _temp:
                elec = _temp
            else:
                elec = get_left_eletr(array)
            _temp = {'ip': useCache, 'room': ' '.join(array), 'elec': elec}
            log(_temp)
            return str(elec)
    return False


if __name__ == '__main__':
    server = flask.Flask(__name__)

    @server.route('/elec', methods=['post', 'get'])
    def get_elec():
        try:
            # flask.Response.headers['Access-Control-Allow-Origin']='*'
            headers = {'Access-Control-Allow-Origin': '*'}
            useCache = flask.request.args.get("qq")
            S = flask.request.args.get("room")
            Flag = shouldCache(useCache, S)
            if Flag == False:
                o = flask.request.args.get("o")
                _ip = flask.request.remote_addr
                array = get_info(S)
                # print(array)
                if len(array) == 4:
                    _temp = cache(' '.join(array))
                    if _temp:
                        elec = _temp
                    else:
                        elec = get_left_eletr(array)
                    _temp = {'ip': _ip, 'room': ' '.join(array), 'elec': elec}
                    if _ip == '192.168.50.1':
                        _temp['ip'] = flask.request.args.get("qq")
                    log(_temp)
                    if o == '1':
                        return str(elec), 200, headers
                    # for arduino show
                    q = f'{str(datetime.datetime.now())[:-7]} {elec}'
                    q = q.split(' ')
                    q[0] = '      '+q[0]
                    q[1] = ' '+q[1]
                    q.append(q[2])
                    q[2] = '  last: '
                    q[3] = '  '+q[3]
                    q = '\n      '.join(q)
                    # print(q)
                    return q
                else:
                    return 'Error', 200, headers
            else:
                return Flag, 200, headers

        except Exception as e:
            print(e)
            return 'Error', 200, headers
    server.run(host='0.0.0.0', port=2333)
