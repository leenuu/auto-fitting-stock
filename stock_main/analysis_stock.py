import numpy
from datetime import datetime
from stock_buy_sell import stock_buy_sell

class analysis_stock:
    def __init__(self):
        self.stock_buy_sell_module = stock_buy_sell()

    def analysis_data(self, code, stock_data):
        price_list = list()
        date_list = list()
        data = stock_data[code]
        for date in data:
            date_list.append(date)            
        date_list.sort()
        for date in date_list:
            price = data[date]['price']
            price_list.append(price)

        first_price = price_list[0]
        yesterday_p = price_list[9]
        last_price = price_list[10]

        today = int(datetime.today().strftime("%Y%m%d"))

        high_line = stock_data[code][today]['high']
        mid_line = stock_data[code][today]['mid']
        low_line = stock_data[code][today]['low']

        max_price = max(price_list)
        min_price = min(price_list)
        max_index = numpy.where(numpy.array(price_list) == max_price)[0]
        min_index = numpy.where(numpy.array(price_list) == min_price)[0]
        
        return {'high' : high_line, 'mid' : mid_line, 'low' : low_line, "first" : first_price, "last" : last_price, "max" : max_price, "min" : min_price, "max index" : max_index, "min_index" : min_index, "yesterday price" : yesterday_p, "price" : price_list}

    def judgment_B_S(self, data, my_stock):
        yesterday_p = data['yesterday price']
        now = data['last']
        mid = data['mid']
        high = data['high']
        low = data['low']
        bought_stock = list()
       