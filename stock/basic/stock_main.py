import time
from stock.util import *
from stock.basic import stock_data
from datetime import datetime

class stock:
    def __init__(self):
        self.cybos_connect_module = Connect.cybos_connect()
        self.analysis_stock_module = analysis_stock.analysis_stock()
        self.stock_data_module = stock_data.stock_data()
        self.stock_recommend_module = recommend.stock_recommend()
        self.stock_data, self.kospi, self.kosdaqm ,self.user_inform_data = dict(), dict(), dict(), dict()
        self.id, self.pwd, self.pwdcert = '', '', ''
        self.stock_code = list()
        self.buy_times ,self.sell_times = True, False

    def load_data(self, kind):
        try:
            self.user_inform_data['my stock'] = self.stock_data_module.load_user_stock_data()
        except FileNotFoundError:
            self.user_inform_data['my stock'] = self.stock_data_module.my_sotck_inform()

        self.stock_code = self.load_codes(kind)
    
    def load_codes(self, kind):
        all_kospi_code = self.stock_recommend_module.check_all_stocks_code()['kospi codes']
        if kind == 'all':
            return all_kospi_code
        elif kind == 'kospi200':
            return self.stock_recommend_module.check_kospi200(all_kospi_code)
        elif kind == 'auto':
            return 0

    def save_data(self):
        data = self.user_inform_data['my stock']
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

    def get_times(self):
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

    def set_up(self, path):
        status = self.cybos_connect_module.get_user_inform(path) 
        if status == 1:
            return 'fail'
        self.user_inform_data['key'] = status

        return 'complete'

            
