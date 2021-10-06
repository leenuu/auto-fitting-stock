import win32com.client, numpy, json
import pandas as pd
from stock.util import stock_request

class stock_data:
    def __init__(self):
        self.chart_data_client = win32com.client.Dispatch("CpSysDib.StockChart")
        self.stock_mst_client = win32com.client.Dispatch('DsCbo1.StockMst')
        self.user_inform_client = win32com.client.Dispatch("CpTrade.CpTd6033")
        self.stock_code_client = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        self.stock_trade_client =  win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.CpSeries_client = win32com.client.Dispatch("CpIndexes.CpSeries")
        self.stock_index_client = win32com.client.Dispatch("CpIndexes.CpIndex")

    def get_stock_data(self, code, day):
        objReply = stock_request.CpCurReply(self.chart_data_client, "StockChart")
        objReply.Subscribe()

        self.chart_data_client.SetInputValue(0, code)   
        self.chart_data_client.SetInputValue(1, ord('2')) 
        self.chart_data_client.SetInputValue(4, day)
        self.chart_data_client.SetInputValue(5, [0,2,3,4,5, 8]) 
        self.chart_data_client.SetInputValue(6, ord('D')) 
        self.chart_data_client.SetInputValue(9, ord('1')) 
        self.chart_data_client.Request() 
        stock_request.MessagePump(10000)

        count = self.chart_data_client.GetHeaderValue(3)
        columns = ['open', 'high', 'low', 'close']
        index = []
        rows = []
        for i in range(count): 
            index.append(self.chart_data_client.GetDataValue(0, i)) 
            rows.append([self.chart_data_client.GetDataValue(1, i), self.chart_data_client.GetDataValue(2, i), self.chart_data_client.GetDataValue(3, i), self.chart_data_client.GetDataValue(4, i)]) 

        stock_data = pd.DataFrame(rows, columns=columns, index=index)

        return stock_data

    def get_bollinger_bands(self, code):
        stock_data = self.get_stock_data(code, 30)
        data = stock_data['close']
        high_line, low_line, mid_line, width, price = float(), float(), float(), float(), float()
        temp_data = dict()
        i = 0
        
        while True:
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
                return code

        return temp_data

    def my_sotck_inform(self):
        user_stock_inform = dict()
        initCheck = self.stock_trade_client.TradeInit(0)
        if (initCheck != 0):
            print("reset fail")
            exit()
        
        acc = self.stock_trade_client.AccountNumber[0]
        accFlag = self.stock_trade_client.GoodsList(acc, 1)
        
        objReply = stock_request.CpCurReply(self.user_inform_client, "CpTd6033")
        objReply.Subscribe()

        self.user_inform_client.SetInputValue(0, acc)
        self.user_inform_client.SetInputValue(1, accFlag[0])
        self.user_inform_client.SetInputValue(2, 50)

        self.user_inform_client.Request() 
        stock_request.MessagePump(10000)
 
        cnt = self.user_inform_client.GetHeaderValue(7)
        # print(cnt)
        for i in range(cnt):
            code = self.user_inform_client.GetDataValue(12, i)  # 종목코드
            name = self.user_inform_client.GetDataValue(0, i)  # 종목명
            cashFlag = self.user_inform_client.GetDataValue(1, i)  # 신용구분
            date = self.user_inform_client.GetDataValue(2, i)  # 대출일
            amount = self.user_inform_client.GetDataValue(7, i) # 체결잔고수량
            buyPrice = self.user_inform_client.GetDataValue(17, i) # 체결장부단가
            evalValue = self.user_inform_client.GetDataValue(9, i) # 평가금액(천원미만은 절사 됨)
            evalPerc = self.user_inform_client.GetDataValue(11, i) # 평가손익

            user_stock_inform[code] = {'amount': amount, 'buy location' : ''}
            # print(code, name, amount)
        return user_stock_inform

    def get_Stochastic_Slow(self, code):
        chart_value = dict()

        self.set_data_Stochastic_Slow(code, 21, self.CpSeries_client)
        self.stock_index_client.series = self.CpSeries_client
        self.stock_index_client.put_IndexKind("Stochastic Slow")  
        self.stock_index_client.put_IndexDefault("Stochastic Slow")  

        self.stock_index_client.Term1 = 5
        self.stock_index_client.Term2 = 3
        self.stock_index_client.Signal = 3
        self.stock_index_client.Calculate()

        cntofIndex = self.stock_index_client.ItemCount
        indexName = ["SLOW K", "SLOW D"]
        for index in range(cntofIndex):
            name = indexName[index]
            chart_value[name] = []
            cnt = self.stock_index_client.GetCount(index)
            for j in range(cnt) :
                value = self.stock_index_client.GetResult(index,j)
                chart_value[name].append(value)
        
        return chart_value

    def set_data_Stochastic_Slow(self, code, cnt, CpSeries_client):

        objReply = stock_request.CpCurReply(self.chart_data_client, "StockChart")
        objReply.Subscribe()

        self.chart_data_client.SetInputValue(0, code)
        self.chart_data_client.SetInputValue(1, ord('2'))
        self.chart_data_client.SetInputValue(4, cnt) 
        self.chart_data_client.SetInputValue(5, [0, 2, 3, 4, 5, 8])  
        self.chart_data_client.SetInputValue(6, ord('D'))  
        self.chart_data_client.SetInputValue(9, ord('1')) 
        
        self.chart_data_client.Request() 
        stock_request.MessagePump(10000)
        
        len = self.chart_data_client.GetHeaderValue(3)

        for i in range(len):
            day = self.chart_data_client.GetDataValue(0, len - i - 1)
            open = self.chart_data_client.GetDataValue(1, len - i - 1)
            high = self.chart_data_client.GetDataValue(2, len - i - 1)
            low = self.chart_data_client.GetDataValue(3, len - i - 1)
            close = self.chart_data_client.GetDataValue(4, len - i - 1)
            vol = self.chart_data_client.GetDataValue(5, len - i - 1)
            CpSeries_client.Add(close, open, high, low, vol)

    def save_user_stock_data(self, data):
        with open('user_data.json', 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, sort_keys=True, indent=4, ensure_ascii=False)
        
    def load_user_stock_data(self):
        with open('user_data.json', 'r') as json_file:
            user_stock_data = json.load(json_file)
        return user_stock_data





 