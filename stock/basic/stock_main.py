import time
from util import *
from basic import stock_data
from datetime import datetime

class stock:
    def __init__(self):
        self.cybos_connect_module = Connect.cybos_connect()
        self.analysis_stock_module = analysis_stock.analysis_stock()
        self.stock_data_module = stock_data.stock_data()
        self.stock_data, self.kospi, self.kosdaqm ,self.user_inform_data = dict(), dict(), dict(), dict()
        self.id, self.pwd, self.pwdcert = '', '', ''
        self.stock_code = list()
        self.buy_times ,self.sell_times = True, False
        self.set_up()

    def load_data(self):
        try:
            self.user_inform_data['my stock'] = self.stock_data_module.load_user_stock_data()
        except FileNotFoundError:
            self.user_inform_data['my stock'] = self.stock_data_module.my_sotck_inform()

        self.stock_code = self.stock_data_module.check_all_stocks_code()['kospi codes']

    def save_data(self):
        data = self.user_inform_data['my stock']
        self.analysis_stock_module.stock_buy_sell_module.save_log()
        self.stock_data_module.save_user_stock_data(data)

    def judgment(self, code, times):
        try:
            if times == 'sell':
                self.buy_times ,self.sell_times = False, True
            stc = self.stock_data_module.get_Stochastic_Slow(code)['SLOW K']
            bb = self.stock_data_module.get_bollinger_bands(code)
            data = self.analysis_stock_module.analysis_data(bb, stc)      
            user_data = self.user_inform_data['my stock']
            status = self.analysis_stock_module.judgment_B_S(code, data, user_data, self.sell_times, self.buy_times)
            return status

        except Exception as e:
            print(e)
            return None

    def get_times(self, times):
        now_h = datetime.now().hour
        now_m = datetime.now().minute
        sell_time_h = 14
        sell_time_m = 30
        if now_m >= sell_time_m and now_h >= sell_time_h:
            self.stock_code = list(self.user_inform_data['my stock'].keys())
            status = 'sell'
        else:
            status = 'buy'
        return status

    def set_up(self):
        self.cybos_connect_module.login() 
        print('start load data')
        self.load_data()
        print('load data complete')

    def run(self):
        stock_len = len(self.stock_code)
        full_stock = False
        times = 'buy'
        print('check time', end='')
        while True:
            stock_number = 0
            if type(self.stock_code) != list:
                print('error')
                break
            
            if full_stock:
                times = 'sell'

            print('\nstart')
            for code in self.stock_code:
                stock_len = len(self.stock_code)
                times = self.get_times()

                if times == 'buy' and len(self.user_inform_data['my stock']) == 50:
                    full_stock = True
                    break
                status = self.judgment(code, times)
                if status == None:
                    self.stock_code.remove(code)
                    pass
                elif status[0] == 'buy success':
                    self.user_inform_data['my stock'][code] = {'amount': status[1], 'buy location' : status[2]}
                    self.stock_code.remove(code)
                    self.save_data()
                elif status[0] == 'sell success':
                    del self.user_inform_data['my stock'][code]
                    self.stock_code.remove(code)
                    self.save_data()
                stock_number += 1
                print(f'\r{stock_number}/{stock_len}       ', end='')
                time.sleep(0.251)
            self.save_data()
            print('\nend')
            
