from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.select import Select
import time


class chromepool():

    def __init__(self, maxsize=5, minsize=1, timeout=10, options=ChromeOptions()):
        self.pool = []
        self.maxsize = maxsize
        self.current = 0
        self.minsize = minsize
        self.timeout = timeout
        self.options = options
        self.new(minsize, options=options)
        self.getting = False

    def new(self, cut=1, options=ChromeOptions()):
        for i in range(cut):
            if self.current+1 < self.maxsize:
                _ch = Chrome(options=options)
                id = _ch.session_id
                _temp = {'num': i, 'id': id, 'd': _ch, 'buzy': False,
                         'st': time.perf_counter()}
                self.current += 1
                self.pool.append(_temp)
            else:
                return False
        return True

    def delete(self, _target):
        for i in self.pool[:]:
            if i['id'].session_id == _target.session_id:
                i['d'].quit()
                self.pool.remove(i)
                self.current -= 1
                return True
        return False

    def delete_all(self):
        while self.getting:
            time.sleep(0.01)
        self.getting = True
        try:
            for i in self.pool[:]:
                i['d'].quit()
                self.pool.remove(i)
                self.getting = False
            return True
        except Exception:
            self.getting = False
            return False

    def get(self):
        while self.getting:
            time.sleep(0.01)
        self.getting = True
        for i in self.pool:
            if i['buzy'] == False:
                i['st'] = time.perf_counter()
                i['buzy'] = True
                self.getting = False
                return i['d']
        else:
            if self.new(options=self.options):
                self.getting = False
                self.pool[-1]['buzy'] = True
                return self.pool[-1]['d']
            else:
                self.getting = False
                return False

    def release(self, _target=''):
        if _target == '':
            return False
        for i in self.pool:
            if i['id'] == _target.session_id:
                _target.delete_all_cookies()
                i['buzy'] = False
                return True

    def monitor(self, level=1):
        while True:
            for i in self.pool:
                _time = time.perf_counter()
                if _time - i['st'] >= self.timeout:
                    self.release(i)
