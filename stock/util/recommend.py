import win32com.client

class stock_recommend:
    def __init__(self):
        self.codes = []
        self.stock_code_client = win32com.client.Dispatch("CpUtil.CpCodeMgr")

    def check_all_stocks_code(self):
        kospi = self.stock_code_client.GetStockListByMarket(1)
        kosdaq = self.stock_code_client.GetStockListByMarket(2)
        kospi_codes, kosdaq_codes = list(), list()
        kospi_name, kosdaq_name = dict(), dict()
        for code in kospi:
            name = self.stock_code_client.CodeToName(code)
            kospi_name.update({code : name})
            kospi_codes.append(code)

        return {'kospi codes' : kospi_codes, 'kospi name' : kospi_name} 

    def check_kospi200(self, codes):
        kospi200 = list()
        for code in codes:
            if self.stock_code_client.GetStockKospi200Kind(code) > 0:
                kospi200.append(code)
        return kospi200

