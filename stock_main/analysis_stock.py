from datetime import datetime, date, timedelta
import stock_buy_sell

class analysis_stock:
    def __init__(self):
        self.stock_buy_sell_module = stock_buy_sell.stock_buy_sell()

    def analysis_data(self, bb, stc):
        
        today = int(date.today().strftime("%Y%m%d"))
        if datetime.today().weekday() == 0:
            yesterday = int((date.today() - timedelta(3)).strftime("%Y%m%d"))
        else:
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

    def judgment_B_S(self, code, data, my_stock, sell_on, buy_on):
        now_p, yesterday_p, now_stc, yesterday_stc = data['now price'], data['yesterday price'], data['now stc'], data['yesterday stc']
        now_high, now_low, now_mid, yesterday_high, yesterday_low, yesterday_mid= data['high'], data['low'], data['mid'], data['yesterday high'], data['yesterday low'], data['yesterday mid']
        bought_stock = list(my_stock.keys())
        # print(bought_stock)
        
        number = 1
        if sell_on and code in bought_stock:
            if yesterday_high > yesterday_p and now_p > now_high and my_stock[code]['buy location'] == 'mid':
                status = self.stock_buy_sell_module.sell(code, my_stock[code]['amount'])
                if status == 0:
                    return ['success']
                else:
                    return ['fail']

            elif yesterday_mid > yesterday_p and now_p > now_mid and my_stock[code]['buy location'] == 'low':
                status = self.stock_buy_sell_module.sell(code, my_stock[code]['amount'])
                if status == 0:
                    return ['sell success']
                else:
                    return ['fail']
            
            elif yesterday_low < yesterday_p and now_low > now_p:
                status = self.stock_buy_sell_module.sell(code, my_stock[code]['amount'])
                if status == 0: 
                    return ['sell success']
                else:
                    return ['fail']
                    
            else:
                return ['stay']

        elif buy_on and code not in bought_stock:
            if yesterday_stc < 20 and now_stc > 20:
                if yesterday_mid > yesterday_p and now_p > now_mid:
                    status = self.stock_buy_sell_module.buy(code, number, 'mid')
                    if status == 0:
                        print(yesterday_stc, now_stc)
                        return ['buy success', number, 'mid']
                    else:
                        return ['fail']
                        
                elif yesterday_low > yesterday_p and now_p > now_low:
                    status = self.stock_buy_sell_module.buy(code, number, 'low')
                    if status == 0:
                        print(yesterday_stc, now_stc)
                        return ['buy success', number, 'low']
                    else:
                        return ['fail']
                   
                else:
                    return ['stay']

            else:
                return ['stay']

        else:
            return ['stay']