import sys, os
sys.path.append(os.path.abspath('stock_main'))
sys.path.append(os.path.abspath('security'))
from stock_main import stock_main

if __name__ == "__main__":
    stocks = stock_main.stock()
    # stocks.cybos_connect_module.login()
    stocks.load_data()
    stocks.save_data()
    # stocks.run()
    # test = cybos_connect()