from Connect import cybos_connect
from analysis_stock import analysis_stock
from stock_buy_sell import stock_buy_sell
from stock_data import get_stock_data
import time

class stock:
    def __init__(self, status):
        self.connection = cybos_connect()
        self.analysis = analysis_stock()
        self.B_S = stock_buy_sell()
        self.S_data = get_stock_data()
        self.stock_data, self.kospi, self.kosdaqm ,self.user_inform_data = dict(), dict(), dict(), dict()
        self.id, self.pwd, self.pwdcert, self.log_data = '', '', '', ''
        self.stock_code = list()
        self.status = status
        try:
            self.user_inform_data['my stock'] = self.S_data.load_user_stock_data()
        except FileNotFoundError:
            self.user_inform_data['my stock'] = self.S_data.my_sotck_inform()

    def judgment(self, code):
        data = self.analysis.analysis_data(code, self.stock_data)
        user_data = self.user_inform_data['stock']
        jg = self.analysis.judgment_B_S(data,user_data)
        num = self.user_inform_data['stock'][code]['amount']
        if jg[0] == "buy":
            st = self.B_S.buy(code, num, jg[1])
            if st == 0:
                self.user_inform_data['stock'][code] = {'amount': num, 'buy location' : jg[1]}

        elif jg[0] == "sell":
            st = self.B_S.sell(code, num)
            if st == 0:
                del self.user_inform_data['stock'][code]

        elif jg[0] == "stay":
            pass
            # print("stay : " + code)
    
    def run(self):
        st = len(test.codes)
        while True:
            print('strat')
            i = 0 
            for code in test.codes:
                i += 1
                time.sleep(0.251)
                error = self.S_data.get_bollinger_bands(code)
                if error == 1:
                    st = len(test.codes)
                    continue
                self.judgment(code)
                print(f"\r{i}/{st}          " ,end='')
            print('end')
            self.B_S.save_log()
            self.S_data.save_user_stock_data(test.user_inform_data['my stock'])
            time.sleep(10)


# code = 'A005930'
# codes = ['A011000', 'A035720', 'A011200', 'A005930', 'A068270', 'A051910', 'A055550', 'A032830', 'A361610']
get = dict()
test = stock(False)
# print(test.user_inform_data)
# test.user_inform = test.login()
# test.save_user_stock_data(test.user_inform_data['my stock'])
# print(test.get_buy_price(code))
# test.check_all_stocks_code()
# test.get_bollinger_bands(code)
# test.run()
# test.judgment(code)
# print(test.code)



