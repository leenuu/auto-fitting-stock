from time import sleep
import win32com.client
from datetime import datetime
from stock.util import stock_request

class stock_buy_sell:        
    def __init__(self):
        self.stock_trade_client =  win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.Stock_Order_client = win32com.client.Dispatch("CpTrade.CpTd0311")
        self.stock_mst_client = win32com.client.Dispatch('DsCbo1.StockMst')

    def buy(self, code, number, location):
        initCheck = self.stock_trade_client.TradeInit(0)
        if (initCheck != 0):
            print("reset fail")
            exit()
        
        price = self.get_buy_price(code)

        acc = self.stock_trade_client.AccountNumber[0]
        accFlag = self.stock_trade_client.GoodsList(acc, 1)  
        # print(acc, accFlag[0])
        objReply = stock_request.CpCurReply(self.Stock_Order_client, "CpTd0311")
        objReply.Subscribe()
                
        self.Stock_Order_client.SetInputValue(0, "2")   
        self.Stock_Order_client.SetInputValue(1, acc )  
        self.Stock_Order_client.SetInputValue(2, accFlag[0])   
        self.Stock_Order_client.SetInputValue(3, code)  
        self.Stock_Order_client.SetInputValue(4, number)  
        self.Stock_Order_client.SetInputValue(5, price)   
        self.Stock_Order_client.SetInputValue(7, "0")   
        self.Stock_Order_client.SetInputValue(8, "12")  
        
        self.Stock_Order_client.Request()
        stock_request.MessagePump(10000)
        
        sleep(1)

        rqStatus = self.Stock_Order_client.GetDibStatus()
        rqRet = self.Stock_Order_client.GetDibMsg1()
        print("\nstatus : ", rqStatus, rqRet)
        if rqStatus == -1:
            print('fail : ' + code)
        else:
            print('buy : ' + code, location)
            self.add_log(f'{datetime.now()}-buy {code} : {number}, {location}')
        
        return rqStatus

    def sell(self, code, number):
        initCheck = self.stock_trade_client.TradeInit(0)
        if (initCheck != 0):
            print("reset fail")
            exit()
        
        price = self.get_sell_price(code)

        # print(self.stock_trade_client.AccountNumber)
        acc = self.stock_trade_client.AccountNumber[0]
        accFlag = self.stock_trade_client.GoodsList(acc, 1)  
        print(acc, accFlag[0])

        objReply = stock_request.CpCurReply(self.Stock_Order_client, "CpTd0311")
        objReply.Subscribe()

        self.Stock_Order_client.SetInputValue(0, "1")   
        self.Stock_Order_client.SetInputValue(1, acc )  
        self.Stock_Order_client.SetInputValue(2, accFlag[0])   
        self.Stock_Order_client.SetInputValue(3, code)  
        self.Stock_Order_client.SetInputValue(4, number)  
        self.Stock_Order_client.SetInputValue(5, price)   
        self.Stock_Order_client.SetInputValue(7, "0")   
        self.Stock_Order_client.SetInputValue(8, "12")  
        
        self.Stock_Order_client.Request()
        stock_request.MessagePump(10000)

        sleep(1)
        
        rqStatus = self.Stock_Order_client.GetDibStatus()
        rqRet = self.Stock_Order_client.GetDibMsg1()
        print("\nstatus : ", rqStatus, rqRet)
        if rqStatus == -1:
            print(f'fail : {code}, number : {number}\n')
        else:
            print('sell : ' + code)
            self.add_log(f'{datetime.now()}-sell {code} : {number}\n')
        
        return rqStatus

    def get_sell_price(self, code):
        objReply = stock_request.CpCurReply(self.stock_mst_client, "StockMst")
        objReply.Subscribe()
        self.stock_mst_client.SetInputValue(0, code)  
        self.stock_mst_client.Request() 
        stock_request.MessagePump(10000)
        sleep(1)
        return self.stock_mst_client.GetHeaderValue(16)
    
    def get_buy_price(self, code):
        objReply = stock_request.CpCurReply(self.stock_mst_client, "StockMst")
        objReply.Subscribe()
        self.stock_mst_client.SetInputValue(0, code)  
        self.stock_mst_client.Request() 
        stock_request.MessagePump(10000)
        sleep(1)
        return self.stock_mst_client.GetHeaderValue(17)

    def add_log(self, st):
        try:
            f = open("log.txt",'a')
            f.write(st)
            f.close()
        except FileNotFoundError:
            f = open("log.txt",'w')
            f.write(st)
            f.close()
