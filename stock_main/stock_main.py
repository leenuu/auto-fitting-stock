import Connect, analysis_stock, stock_buy_sell, stock_data, win32com.client
import pandas as pd
import time

class stock(analysis_stock.analysis_stock, Connect.cybos_connect, stock_buy_sell.stock_buy_sell, stock_data.get_stock_data):
    def __init__(self, status):
        self.chart_data_client = win32com.client.Dispatch("CpSysDib.StockChart")
        self.stock_mst_client = win32com.client.Dispatch('DsCbo1.StockMst')
        self.user_inform_client = win32com.client.Dispatch("CpTrade.CpTd6033")
        self.stock_trade_client =  win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.Stock_Order_client = win32com.client.Dispatch("CpTrade.CpTd0311")
        self.stock_data, self.kospi, self.kosdaqm ,self.user_inform_data = dict(), dict(), dict(), dict()
        self.id, self.pwd, self.pwdcert, self.log_data = '', '', '', ''
        self.stock_code = list()
        self.status = status
        try:
            self.user_inform_data['my stock'] = self.load_user_stock_data()
        except FileNotFoundError:
            self.user_inform_data['my stock'] = self.my_sotck_inform()

    def judgment(self, code):
        data = self.analysis_data(code, self.stock_data)
        user_data = self.user_inform_data['stock']
        jg = self.judgment_B_S(data,user_data)
        num = 1
        if jg[0] == "buy":
            st = self.buy(code, num, jg[1])
            if st == 0:
                self.user_inform_data['stock'][code] = {'amount': num, 'buy location' : jg[1]}

        elif jg[0] == "sell":
            st = self.sell(code, num)
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
                error = test.get_bollinger_bands(code)
                if error == 1:
                    st = len(test.codes)
                    continue
                test.judgment(code)
                print(f"\r{i}/{st}          " ,end='')
            print('end')
            test.save_log()
            test.save_user_stock_data(test.user_inform_data['my stock'])
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



