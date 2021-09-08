from json import load
from Connect import cybos_connect
from analysis_stock import analysis_stock
from stock_data import stock_data
import time

class stock:
    def __init__(self, status):
        self.cybos_connect_module = cybos_connect()
        self.analysis_stock_module = analysis_stock()
        self.stock_data_module = stock_data()
        self.stock_data, self.kospi, self.kosdaqm ,self.user_inform_data = dict(), dict(), dict(), dict()
        self.id, self.pwd, self.pwdcert = '', '', ''
        self.stock_code = list()
        self.status = status

    def load_data(self):
        try:
            self.user_inform_data['my stock'] = self.stock_data_module.load_user_stock_data()
        except FileNotFoundError:
            self.user_inform_data['my stock'] = self.stock_data_module.my_sotck_inform()

        self.stock_code = self.stock_data_module.check_all_stocks_code()

    def save_data(self):
        data = self.user_inform_data['my stock']
        self.analysis_stock_module.stock_buy_sell_module.save_log()
        self.stock_data_module.save_user_stock_data(data)

    def judgment(self, code):
        stc = self.stock_data_module.get_Stochastic_Slow(code)['SLOW K']
        bb = self.stock_data_module.get_bollinger_bands(code)
        data = self.analysis_stock_module.analysis_data(bb, stc)      
        user_data = self.user_inform_data['my stock']
        self.analysis_stock_module.judgment_B_S(code, data, user_data)

    def run(self):
        self.cybos_connect_module.login()
        self.load_data()

        while True:
            for code in self.stock_code:
                self.judgment(code)
                time.sleep(0.251)


# code = 'A005930'
get = dict()
test = stock(False)
test.run()
# test.load_data()
# test.judgment(code)
# test.load_data()
# print(test.user_inform_data['my stock'])
# test.cybos_connect_module.login()
# print(test.stock_data_module.get_Stochastic_Slow(code))



