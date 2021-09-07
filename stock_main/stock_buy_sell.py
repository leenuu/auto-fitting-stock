import win32com.client

class stock_buy_sell:        
    def __init__(self):
        self.stock_trade_client =  win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.Stock_Order_client = win32com.client.Dispatch("CpTrade.CpTd0311")

    def buy(self, code, number, location):
        initCheck = self.stock_trade_client.TradeInit(0)
        if (initCheck != 0):
            print("주문 초기화 실패")
            exit()
        
        price = self.get_buy_price(code)

        acc = self.stock_trade_client.AccountNumber[0]
        accFlag = self.stock_trade_client.GoodsList(acc, 1)  
        print(acc, accFlag[0])
        
        self.Stock_Order_client.SetInputValue(0, "2")   
        self.Stock_Order_client.SetInputValue(1, acc )  
        self.Stock_Order_client.SetInputValue(2, accFlag[0])   
        self.Stock_Order_client.SetInputValue(3, code)  
        self.Stock_Order_client.SetInputValue(4, number)  
        self.Stock_Order_client.SetInputValue(5, price)   
        self.Stock_Order_client.SetInputValue(7, "0")   
        self.Stock_Order_client.SetInputValue(8, "12")  
        
        self.Stock_Order_client.BlockRequest()
        
        rqStatus = self.Stock_Order_client.GetDibStatus()
        rqRet = self.Stock_Order_client.GetDibMsg1()
        print("\n통신상태", rqStatus, rqRet)
        if rqStatus == -1:
            print('불가')
        else:
            print('buy : ' + code, location)
            self.add_log(f'buy {code} : {number}, {location}')
            return 0

    def sell(self, code, number):
        initCheck = self.stock_trade_client.TradeInit(0)
        if (initCheck != 0):
            print("주문 초기화 실패")
            exit()
        
        price = self.get_sell_price(code)

        # print(self.stock_trade_client.AccountNumber)
        acc = self.stock_trade_client.AccountNumber[0]
        accFlag = self.stock_trade_client.GoodsList(acc, 1)  
        print(acc, accFlag[0])

        self.Stock_Order_client.SetInputValue(0, "1")   
        self.Stock_Order_client.SetInputValue(1, acc )  
        self.Stock_Order_client.SetInputValue(2, accFlag[0])   
        self.Stock_Order_client.SetInputValue(3, code)  
        self.Stock_Order_client.SetInputValue(4, number)  
        self.Stock_Order_client.SetInputValue(5, price)   
        self.Stock_Order_client.SetInputValue(7, "0")   
        self.Stock_Order_client.SetInputValue(8, "12")  
        
        self.Stock_Order_client.BlockRequest()
        
        rqStatus = self.Stock_Order_client.GetDibStatus()
        rqRet = self.Stock_Order_client.GetDibMsg1()
        print("\n통신상태", rqStatus, rqRet)
        if rqStatus == -1:
            print('불가')
        else:
            print('sell : ' + code)
            self.add_log(f'sell {code} : {number}')
            return 0
        
    def add_log(self, st):
        self.log_data += st + '\n'

    def save_log(self):
        f = open("log.txt",'w')
        f.write(self.log_data)
        f.close()