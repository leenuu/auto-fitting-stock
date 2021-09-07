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

    def judgment_B_S(self, data, my_stock, status):
        yesterday_p = data['yesterday price']
        now = data['last']
        mid = data['mid']
        high = data['high']
        low = data['low']
        sell_on = status
        bought_stock = list()
        for code in list(my_stock.keys()):
            bought_stock.append(code) 

        if now > high and my_stock[code]['buy location'] == 'mid':
            return ['sell']

        elif now > mid and my_stock[code]['buy location'] == 'low':
            return ['sell']

        elif low > now:
            return ['sell']
                
        if code not in bought_stock and sell_on == False:
            if yesterday_p < mid and now > mid:
                return ['buy','mid']       
            elif yesterday_p < low and now > low:
                return ['buy','low']   
            else: 
                return ['stay']         
        
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


# First_MAX_lists = data['First'] - data['max']
# First_MIN_lists = data['First'] - data['min']
# Last_MAX_lists = data['last'] - data['max']
# Last_MIN_lists = data['last'] - data['min']
