from pywinauto import application
import win32com.client, time, os
from stock.security import encryption_process

class cybos_connect:
    def login(self):
        status = False
        login_system = encryption_process.encryption_pro()
        user_inform = login_system.get_key_file()
        
        if user_inform == 0:
            print("Invalid Key")
            exit()

        print("Correct Key")
        self.taskkill()
        self.connect(user_inform["id"], user_inform["pwd"], user_inform["pwdcert"], status) #true online 
        self.connect_test()

        return user_inform

    def taskkill(self):
        os.system('taskkill /IM ncStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T') 
        os.system('taskkill /IM DibServer* /F /T') 
        os.system('wmic process where "name like \'%ncStarter%\'" call terminate') 
        os.system('wmic process where "name like \'%CpStart%\'" call terminate') 
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')
        time.sleep(5) 

        print("Task Kill Complete")

    def connect(self, id, pwd, pwdcert, status):
        app = application.Application()
        if status == True:
            app.start(f'C:\DAISHIN\STARTER\\ncStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwdcert} /autostart')
        elif status == False:
            app.start(f'C:\DAISHIN\STARTER\\ncStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert: /autostart')            
        input("When starting task is complete, Press Enter key......")
    
    def connect_test(self):
        print("start PLUS Connect test")
        CpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        Connect = CpCybos.IsConnect
        if (Connect == 0):
            print("PLUS Connect Failed")
            exit()
        else:
            print("PLUS Connect Complete")
