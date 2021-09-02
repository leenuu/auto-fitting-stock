import numpy, Connect, os, sys, win32com.client
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from security.encryption_process import encryption_pro

class stock:
    def __init__(self, status):
        self.id, self.pwd, self.pwdcert = '', '', ''
        self.user_inform, self.stock_data, self.kospi, self.kosdaq = dict(), dict(), dict(), dict()
        self.fild = [17]
        self.fild_dict = {}
        self.stock_code = list()
        self.status = status
        self.chart_data = win32com.client.Dispatch("CpSysDib.StockChart")


    def login(self):
        login_system = encryption_pro()
        self.user_inform = login_system.get_key_file()
        
        if self.user_inform == 0:
            print("Invalid Key")
            exit()

        print("Correct Key")
        self.connection = Connect.cybos_connect()
        self.connection.taskkill()
        self.connection.connect(self.user_inform["id"], self.user_inform["pwd"], self.user_inform["pwdcert"], self.status) #true online 
        self.connection.connect_test()

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
        for code in kospi:
            name = objCpCodeMgr.CodeToName(code)
            self.kospi.update({code : name})

        for code in kosdaq:
            name = objCpCodeMgr.CodeToName(code)
            self.kosdaq.update({code : name})

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
        stock_data = self.get_stock_data(code, 400)
        data = stock_data['close']
        high_line, low_line, mid_line, width, price = float(), float(), float(), float(), float()
        temp_data = dict()
        i = 0
        while True:
            start = i
            end = start + 20
            if end > 400:
                break
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
        return {code : temp_data}
