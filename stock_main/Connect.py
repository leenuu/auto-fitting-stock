from pywinauto import application
import win32com.client
import time
import os

class cybos_connect:
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
        time.sleep(30)
    
    def connect_test(self):
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        if (bConnect == 0):
            print("PLUS Connect Failed")
            exit()
        else:
            print("PLUS Connect Complete")