from cryptography.fernet import Fernet
from tkinter import filedialog

class encryption_pro:
    def __init__(self):
        self.data = b''
        self.login_str = b'404_not_found'
        self.login_key_str = b''
    
    def get_key_file(self):
        try:
            path = input("Filfe path: ")
            with open(path, 'r') as key_file:
                key_data = key_file.read().split('\n')
                login_fernet = Fernet(key_data[0].encode('euc-kr'))
                key = key_data[1].encode('euc-kr')
                id = key_data[2].encode('euc-kr')
                pwd = key_data[3].encode('euc-kr')
                pwdcert = key_data[4].encode('euc-kr')
            
            if self.login_str == login_fernet.decrypt(key):
                id = login_fernet.decrypt(id).decode('euc-kr')
                pwd = login_fernet.decrypt(pwd).decode('euc-kr')
                pwdcert = login_fernet.decrypt(pwdcert).decode('euc-kr')
                data = {"id": id, "pwd": pwd, "pwdcert": pwdcert}
                return data

            else:
                return 0

        except Exception as e:
            print(e) 
