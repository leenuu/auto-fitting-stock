from Connect import cybos_connect
from analysis_stock import analysis_stock
from stock_data import stock_data
import time
from datetime import datetime

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

        self.stock_code = self.stock_data_module.check_all_stocks_code()['kospi codes']

    def save_data(self):
        data = self.user_inform_data['my stock']
        self.analysis_stock_module.stock_buy_sell_module.save_log()
        self.stock_data_module.save_user_stock_data(data)

    def judgment(self, code):
        try:

            sell_on = False
            buy_on = True
            now = datetime.now().hour
            sell_time = 15
            if now >= sell_time :
                sell_on = True
                buy_on = False
            stc = self.stock_data_module.get_Stochastic_Slow(code)['SLOW K']
            bb = self.stock_data_module.get_bollinger_bands(code)
            data = self.analysis_stock_module.analysis_data(bb, stc)      
            user_data = self.user_inform_data['my stock']
            status = self.analysis_stock_module.judgment_B_S(code, data, user_data, sell_on, buy_on)
            return status
        except Exception as e:
            print(e)
            return None

    def run(self):
        self.cybos_connect_module.login() 
        self.load_data()
        st = len(self.stock_code)
        i = 0
        while True:
            now = datetime.now().hour
            sell_time = 15
            if now >= sell_time :
                self.stock_data = list(self.user_inform_data['my stock'].keys())

            if datetime.now().hour < 9:
                print('not time')
                time.sleep(60)
                continue

            if type(self.stock_code) != list:
                print('err')
                self.stock_code.remove(code)
                continue
            
            print('start')
            for code in self.stock_code:
                status = self.judgment(code)
                # print(status)
                if status == None:
                    pass
                elif status[0] == 'buy success':
                    self.user_inform_data['my stock'][code] = {'amount': status[1], 'buy location' : status[2]}
                elif status[0] == 'sell success':
                    del self.user_inform_data['my stock'][code]
                i += 1
                print(f'\r {i}/{st}       ', end='')
                time.sleep(0.251)

            i = 0
            print('end')
            self.save_data()
code = 'A005930'
get = dict()
test = stock(False)
# test.cybos_connect_module.login()
# test.user_inform_data['my stock'] = test.stock_data_module.my_sotck_inform()
# test.save_data()
test.run()
# print(test.stock_data_module.get_Stochastic_Slow(code)["SLOW K"])

# a = test.stock_data_module.get_Stochastic_Slow('A014915')['SLOW K']
# print(a[len(a)-1])
# print(a[len(a)-2])
# test.stock_data_module.check_all_stocks_code()
# test.load_data()
# test.judgment(code)
# test.load_data()
# print(test.user_inform_data['my stock'])
# test.cybos_connect_module.login()
# print(test.stock_data_module.get_Stochastic_Slow(code))



