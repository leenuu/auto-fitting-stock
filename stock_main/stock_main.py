import numpy, Connect, os, sys, win32com.client, analysis_stock
import pandas as pd
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from security.encryption_process import encryption_pro

class stock(analysis_stock.analysis_stock, Connect.cybos_connect):
    def __init__(self, status):
        self.id, self.pwd, self.pwdcert = '', '', ''
        self.user_inform, self.stock_data, self.kospi, self.kosdaq = dict(), dict(), dict(), dict()
        self.fild = [17]
        self.fild_dict = {}
        self.stock_code = list()
        self.status = status
        self.chart_data = win32com.client.Dispatch("CpSysDib.StockChart")
        self.stock_mst = win32com.client.Dispatch('DsCbo1.StockMst')
        self.stock_trade =  win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.Stock_Order = win32com.client.Dispatch("CpTrade.CpTd0311")
        self.log_data = ''
        
    def login(self):
        login_system = encryption_pro()
        self.user_inform = login_system.get_key_file()
        
        if self.user_inform == 0:
            print("Invalid Key")
            exit()

        print("Correct Key")
        self.taskkill()
        self.connect(self.user_inform["id"], self.user_inform["pwd"], self.user_inform["pwdcert"], self.status) #true online 
        self.connect_test()

        # print("connect test complete")
    
    def add_code(self, codes):
        if type(codes) == list:
            for code in codes:
                if code not in self.stock_code:
                    self.stock_code.append(code)
        elif type(codes) == str: 
            if codes not in self.stock_code:
                self.stock_code.append(codes)    

    def check_all_stocks_code(self):
        objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        kospi = objCpCodeMgr.GetStockListByMarket(1)
        kosdaq = objCpCodeMgr.GetStockListByMarket(2)
        self.codes = []
        for code in kospi:
            name = objCpCodeMgr.CodeToName(code)
            self.kospi.update({code : name})
            
            self.codes.append(code)
            # print(code)
        print(len(self.codes))
        # self.codes = self.codes[:]
        self.get = dict()
        for code in self.codes:
            self.get[code] = False
        
        # for code in kosdaq:
        #     name = objCpCodeMgr.CodeToName(code)
        #     self.kosdaq.update({code : name})

    def get_stock_data(self, code, day):
        self.chart_data.SetInputValue(0, code)   
        self.chart_data.SetInputValue(1, ord('2')) 
        self.chart_data.SetInputValue(4, day)
        self.chart_data.SetInputValue(5, [0,2,3,4,5, 8]) 
        self.chart_data.SetInputValue(6, ord('D')) 
        self.chart_data.SetInputValue(9, ord('1')) 
        self.chart_data.BlockRequest()

        count = self.chart_data.GetHeaderValue(3)
        columns = ['open', 'high', 'low', 'close']
        index = []
        rows = []
        for i in range(count): 
            index.append(self.chart_data.GetDataValue(0, i)) 
            rows.append([self.chart_data.GetDataValue(1, i), self.chart_data.GetDataValue(2, i), self.chart_data.GetDataValue(3, i), self.chart_data.GetDataValue(4, i)]) 

        stock_data = pd.DataFrame(rows, columns=columns, index=index)

        return stock_data

    def get_bollinger_bands(self, code):
        stock_data = self.get_stock_data(code, 30)
        # print(stock_data)
        data = stock_data['close']
        # print(data)
        high_line, low_line, mid_line, width, price = float(), float(), float(), float(), float()
        temp_data = dict()
        i = 0
        
        while True:
            # print(data.values[0:20])
            start = i
            end = start + 20
            if end > 30:
                break
            try: 
                avg = numpy.mean(data.values[start : end])
                std = numpy.std(data.values[start : end])
                date = data.index[i]
                price = data.values[start]
                high_line = avg + (2 * std)
                mid_line = avg
                low_line = avg - (2 * std)
                width = (high_line - low_line) / mid_line 
                temp_data[date] = {'high' : high_line, 'mid' : mid_line, 'low' : low_line, 'width' : width, 'price' : price}
                i += 1
            
            except IndexError:
                self.codes.remove(code)
                return 1

        # print(temp_data)
        self.stock_data[code] = temp_data

    def get_sell_price(self, code):
        self.stock_mst.SetInputValue(0, code)  
        self.stock_mst.BlockRequest() 
        return self.stock_mst.GetHeaderValue(16)
    
    def get_buy_price(self, code):
        self.stock_mst.SetInputValue(0, code)   
        self.stock_mst.BlockRequest()
        return self.stock_mst.GetHeaderValue(17)
         
    def buy(self, code, number):
        initCheck = self.stock_trade.TradeInit(0)
        if (initCheck != 0):
            print("주문 초기화 실패")
            exit()
        
        price = self.get_buy_price(code)

        acc = self.stock_trade.AccountNumber[0]
        accFlag = self.stock_trade.GoodsList(acc, 1)  
        print(acc, accFlag[0])
        
        self.Stock_Order.SetInputValue(0, "2")   
        self.Stock_Order.SetInputValue(1, acc )  
        self.Stock_Order.SetInputValue(2, accFlag[0])   
        self.Stock_Order.SetInputValue(3, code)  
        self.Stock_Order.SetInputValue(4, number)  
        self.Stock_Order.SetInputValue(5, price)   
        self.Stock_Order.SetInputValue(7, "0")   
        self.Stock_Order.SetInputValue(8, "01")  
        
        self.Stock_Order.BlockRequest()
        
        rqStatus = self.Stock_Order.GetDibStatus()
        rqRet = self.Stock_Order.GetDibMsg1()
        print("\n통신상태", rqStatus, rqRet)
        if rqStatus == -1:
            print('불가')
        else:
            print('buy : ' + code)
            self.add_log(f'buy {code} : {number}')

    def sell(self, code, number):
        initCheck = self.stock_trade.TradeInit(0)
        if (initCheck != 0):
            print("주문 초기화 실패")
            exit()
        
        price = self.get_sell_price(code)

        # print(self.stock_trade.AccountNumber)
        acc = self.stock_trade.AccountNumber[0]
        accFlag = self.stock_trade.GoodsList(acc, 1)  
        print(acc, accFlag[0])

        self.Stock_Order.SetInputValue(0, "2")   
        self.Stock_Order.SetInputValue(1, acc )  
        self.Stock_Order.SetInputValue(2, accFlag[0])   
        self.Stock_Order.SetInputValue(3, code)  
        self.Stock_Order.SetInputValue(4, number)  
        self.Stock_Order.SetInputValue(5, price)   
        self.Stock_Order.SetInputValue(7, "0")   
        self.Stock_Order.SetInputValue(8, "01")  
        
        self.Stock_Order.BlockRequest()
        
        rqStatus = self.Stock_Order.GetDibStatus()
        rqRet = self.Stock_Order.GetDibMsg1()
        print("\n통신상태", rqStatus, rqRet)
        if rqStatus == -1:
            print('불가')
        else:
            print('sell : ' + code)
            self.add_log(f'sell {code} : {number}')

    def judgment(self, code):
        data = self.analysis_data(code, self.stock_data)
        jg = self.judgment_B_S(data, self.get[code])
        num = 1
        if jg == "buy":
            self.buy(code, num)
            self.get[code] = True

        elif jg == "sell":
            self.sell(code, num)

        elif jg == "stay":
            pass
            # print("stay : " + code)

    def add_log(self, st):
        self.log_data += st + '\n'

    def save_log(self):
        f = open("log.txt",'w')
        f.write(self.log_data)
        f.close()
