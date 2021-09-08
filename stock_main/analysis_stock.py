import numpy
from datetime import datetime, date, timedelta
from stock_buy_sell import stock_buy_sell

class analysis_stock:
    def __init__(self):
        self.stock_buy_sell_module = stock_buy_sell()

    def analysis_data(self, bb, stc):
        
        today = int(date.today().strftime("%Y%m%d"))
        yesterday = int((date.today() - timedelta(1)).strftime("%Y%m%d"))

        yesterday_p = bb[yesterday]['price']
        now_p = bb[today]['price']

        high_line = bb[today]['high']
        mid_line = bb[today]['mid']
        low_line = bb[today]['low']
        yesterday_high_line = bb[yesterday]['high']
        yesterday_mid_line = bb[yesterday]['mid']
        yesterday_low_line = bb[yesterday]['low']
        
        now_stc = stc[len(stc)-1]
        yesterday_stc = stc[len(stc)-2]
        return {'yesterday stc' : yesterday_stc, 'now stc' : now_stc, 'high' : high_line, 'mid' : mid_line, 'low' : low_line, 'yesterday high' : yesterday_high_line, 'yesterday mid' : yesterday_mid_line, 'yesterday low' : yesterday_low_line, "yesterday price" : yesterday_p, "now price" : now_p}

    def judgment_B_S(self, code, data, my_stock):
        now_p, yesterday_p, now_stc, yesterday_stc = data['now price'], data['yesterday price'], data['yesterday stc'], data['now stc']
        now_high, now_low, now_mid, yesterday_high, yesterday_low, yesterday_mid= data['high'], data['low'], data['mid'], data['yesterday high'], data['yesterday low'], data['yesterday mid']
        bought_stock = list(my_stock.keys())
        sell_time = 15
        now = datetime.now().hour
        number = 1

        if now >= sell_time and code in bought_stock:
            if yesterday_stc > 80 and now_stc < 80:
                if yesterday_high > yesterday_p and now_p > now_high and my_stock[code]['buy location'] == 'mid':
                    self.stock_buy_sell_module.sell(code, my_stock[code]['amount'])
                
                elif yesterday_mid > yesterday_p and now_p > now_mid and my_stock[code]['buy location'] == 'low':
                    self.stock_buy_sell_module.sell(code, my_stock[code]['amount'])
                
                else:
                    return ['stay']
            else:
                return ['stay']

        else:
            if yesterday_stc < 20 and now_stc > 20:
                if yesterday_mid > yesterday_p and now_p > now_mid:
                    self.stock_buy_sell_module.buy(code, number)
                
                elif yesterday_low > yesterday_p and now_p > now_low:
                    self.stock_buy_sell_module.buy(code, number)
                
                else:
                    return ['stay']
            else:
                return ['stay']