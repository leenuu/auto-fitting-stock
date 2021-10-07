from stock.basic.stock_main import stock
from PyQt5 import QtCore
from stock.util import Connect
from stock.basic import stock_main
import time
# import debugpy
import copy

class stock_thread(QtCore.QThread):

    threadEvent = QtCore.pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.stock = stock_main.stock()
        self.codes = list()
        self.user_stock = dict()
        self.isRun = False
        self.kind = ''
        self.error_dict = {"error" : -1}
        
    def run(self):
      if self.isRun:
        # debugpy.debug_this_thread()
        if type(self.stock.stock_code) != list:
            print('error')
            exit()

        full_stock = False
        times = 'buy'
        
        print('check time', end='')

        while True:
            stock_number = 1
                
            if full_stock:
                times = 'sell'

            print('\nstart')
            for code in self.stock.stock_code:
                stock_len = len(self.stock.stock_code)
                print(f'\r{stock_number}/{stock_len}  ', end='')
                if self.isRun == False:
                    break
                
                if times == 'buy' and len(self.stock.stock_code) == 50:
                    full_stock = True
                    print('full stock')
                    break

                if full_stock == False:
                    times = self.stock.get_times()

                if times == 'sell':
                    stock_len = len(self.stock.user_inform_data['my stock'])
                
                try:
                    status = self.stock.judgment(code, times)

                except Exception as error_msg:
                    if str(error_msg) == "list.remove(x): x not in list":
                        time.sleep(5)
                        status = self.stock.judgment(code, times)
                    else:
                        self.isRun == False
                        print(f"error : {error_msg}")
                        self.threadEvent.emit(self.error_dict)
                        time.sleep(1)

                if status == None:
                    self.codes.remove(code)
                    pass
                
                elif status[0] == 'buy success':
                    self.stock.user_inform_data['my stock'][code] = {'amount': status[1], 'buy location' : status[2]}
                    self.stock.stock_code.remove(code)
                    self.threadEvent.emit(self.stock.user_inform_data['my stock'])
                        
                elif status[0] == 'sell success':
                    del self.user_stock[code]
                    self.stock.stock_code.remove(code)
                    self.threadEvent.emit(self.stock.user_inform_data['my stock'])
                

                stock_number += 1

                # print(f'\r{stock_number}/{len(self.stock.stock_code)}       ', end='')
                
                # time.sleep(0.251)
                # print(f'\r                                                          ', end='')

            self.threadEvent.emit(self.stock.user_inform_data['my stock'])

            if self.isRun == False:
                print('\nstop')
                break
            
            print('\nend')

        # self.isRun = False

    def save(self):
        pass

class stock_login_thread(QtCore.QThread):

    # threadEvent = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.cybos_connect_module = Connect.cybos_connect()
        self.user_data = dict()
        self.isRun = False
        
    def run(self):
      if self.isRun:
        # data = list()
        # self.threadEvent.emit(data)
        self.cybos_connect_module.login(self.user_data)
        self.isRun = False

class test(QtCore.QThread):

    # threadEvent = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.isRun = False

    def run(self):
        i = 0
        print('start')
        if self.isRun:
            while True:
                print(i)
                time.sleep(1)
                i += 1
                if i == 10 or self.isRun == False:
                    break
        print('stop')
        self.isRun = False

