import numpy, Connect, os, sys, win32com.client
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from security.encryption_process import encryption_pro

class stock:
    def __init__(self, status):
        self.id = ''
        self.pwd = ''
        self.pwdcert = ''
        self.user_inform = dict()
        self.fild = [17]
        self.fild_dict = {}
        self.stock_data = dict()
        self.stock_code = list()
        self.status = status

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

    def check_all_stocks(self):
        objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        codeList = objCpCodeMgr.GetStockListByMarket(1) #거래소, 코스피
        strr = ''
        for i, code in enumerate(codeList):
            secondCode = objCpCodeMgr.GetStockSectionKind(code)
            name = objCpCodeMgr.CodeToName(code)
            stdPrice = objCpCodeMgr.GetStockStdPrice(code)
            strr += str(name) + ' ' + str(secondCode) + ' ' + str(stdPrice) + '\n'
        print(i, code, secondCode, stdPrice, name)

    def get_stock_data(self, code, day):
        chart_data = win32com.client.Dispatch("CpSysDib.StockChart")
 
        chart_data.SetInputValue(0, code)   
        chart_data.SetInputValue(1, ord('2')) 
        chart_data.SetInputValue(4, day)
        chart_data.SetInputValue(5, [0,2,3,4,5, 8]) 
        chart_data.SetInputValue(6, ord('D')) 
        chart_data.SetInputValue(9, ord('1')) 
        chart_data.BlockRequest()

        count = chart_data.GetHeaderValue(3)
        columns = ['open', 'high', 'low', 'close']
        index = []
        rows = []
        for i in range(count): 
            index.append(chart_data.GetDataValue(0, i)) 
            rows.append([chart_data.GetDataValue(1, i), chart_data.GetDataValue(2, i), chart_data.GetDataValue(3, i), chart_data.GetDataValue(4, i)]) 

        stock_data = pd.DataFrame(rows, columns=columns, index=index)

        return stock_data

    def get_bollinger_bands(self, code):
        stock_data = self.get_stock_data(code, 20)
        data = stock_data['close']
        avg = numpy.mean(data)
        std = numpy.std(data)
        
        high_line = avg + (2 * std)
        mid_line = avg
        low_line = avg - (2 * std)
        
        return {'high' : high_line, 'mid' : mid_line, 'low' : low_line}
