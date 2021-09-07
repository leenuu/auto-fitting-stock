import numpy
from datetime import datetime

class analysis_stock:
    def analysis_data(self, code, stock_data):
        price_list = list()
        date_list = list()
        data = stock_data[code]
        for date in data:
            date_list.append(date)            
        date_list.sort()
        for date in date_list:
            # print(date)
            price = data[date]['price']
            price_list.append(price)

        first_price = price_list[0]
        yesterday_p = price_list[9]
        last_price = price_list[10]

        # print(stock_data[code])

        today = int(datetime.today().strftime("%Y%m%d"))

        high_line = stock_data[code][today]['high']
        mid_line = stock_data[code][today]['mid']
        low_line = stock_data[code][today]['low']

        max_price = max(price_list)
        min_price = min(price_list)
        max_index = numpy.where(numpy.array(price_list) == max_price)[0]
        min_index = numpy.where(numpy.array(price_list) == min_price)[0]
        
        return {'high' : high_line, 'mid' : mid_line, 'low' : low_line, "first" : first_price, "last" : last_price, "max" : max_price, "min" : min_price, "max index" : max_index, "min_index" : min_index, "yesterday price" : yesterday_p, "price" : price_list}

    def judgment_B_S(self, data, status):
        yesterday_p = data['yesterday price']
        now = data['last']
        mid = data['mid']
        high = data['high']
        low = data['low']
        have_stock = status
        sell_on = False
        if datetime.now().hour >= 15:
            sell_on = True

        # index = self.index_count(data)

        if have_stock and sell_on:
            if yesterday_p < high and now > high:
                return 'sell'

            elif yesterday_p > mid and now < mid:
                return 'sell'

            elif low > now:
                return 'sell'

            else: 
                return 'stay'
                
        elif have_stock == False and sell_on == False:
            if yesterday_p < mid and now > mid:
                return 'buy'        
            else: 
                return 'stay'         

        # elif yesterday_p > mid and now < mid:
        #     return 'stay'

        # elif yesterday_p == mid:
        #     return 'stay'

        
    def index_count(self, data):
        if len(data['max index']) == 1:
            MAX_index = data['max index']
            MAX_index_count = 1
        
        elif len(data['max index']) > 1:
            MAX_index = data['max index']
            MAX_index_count =  len(data['max index'])    


        if len(data['min index']) == 1:
            MIN_index = data['min index']
            MIN_index_count = 1
        
        elif len(data['min index']) > 1:
            MIN_index = data['min index']
            MIN_index_count =  len(data['min index']) 

        return {'max index' : MAX_index, 'max index count' : MAX_index_count, 'min index' : MIN_index, 'min index count' : MIN_index_count}
