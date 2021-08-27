import Connect
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from security.encryption_process import encryption_pro


class stock:
    def __init__(self, status):
        self.id = ''
        self.pwd = ''
        self.pwdcert = ''
        self.user_inform = dict()
        self.status = status
    
    def login(self):
        login_system = encryption_pro()
        self.user_inform = login_system.get_key_file()
        
        if self.user_inform == 0:
            print("Invalid Key")
            exit()

        print("Correct Key")
        self.connection = Connect.cybos_connect()
        self.connection.taskkill()
        self.connection.connect(self.user_inform["id"], self.user_inform["pwd"], self.user_inform["pwdcert"], self.status) #true online 
        self.connection.connect_test()

        # print("connect test complete")
    

test = stock(False)
test.login()
# test.connect_test()


