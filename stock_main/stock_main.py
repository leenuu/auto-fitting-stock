import Connect
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from security.encryption_process import encryption_pro
import win32com.client

class stock:
    def __init__(self, status):
        self.id = ''
        self.pwd = ''
        self.pwdcert = ''
        self.user_inform = dict()
        self.fild = []
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

    def all_stocks_data(self, code):
        stock_data = win32com.client.Dispatch("CpSysDib.MarketEye")
        stock_data.SetInputValue(0, self.fild)    
        stock_data.SetInputValue(1, [code])
        stock_data.BlockRequest()
 
        
        
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

test = stock(False)
# test.login()
test.all_stocks_data('A302440')
print(test.stock_data)


