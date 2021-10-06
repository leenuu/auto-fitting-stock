from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import fabs
from stock.basic import *
from stock.gui import stock_th

class Ui_Stock_gui(object):
    def __init__(self):
        self.stock = stock_main.stock()
        self.thread = stock_th.stock_thread()
        self.thread.threadEvent.connect(self.get_data)
        self.login_thread = stock_th.stock_login_thread()
        self.test_th = stock_th.test()
        self.logined = False
        self.start_st = 0

    def setupUi(self, Stock_gui):

        Stock_gui.setObjectName("Stock_gui")
        Stock_gui.resize(367, 134)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\img/chart-line-g3a7c2e109_1280.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Stock_gui.setWindowIcon(icon)

        self.Start_btn = QtWidgets.QPushButton(Stock_gui)
        self.Start_btn.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.Start_btn.setObjectName("Start_btn")
        self.Start_btn.clicked.connect(self.start)
        self.Start_btn.setDisabled(True)

        self.Stop_btn = QtWidgets.QPushButton(Stock_gui)
        self.Stop_btn.setGeometry(QtCore.QRect(100, 10, 75, 23))
        self.Stop_btn.setObjectName("Stop_btn")
        self.Stop_btn.clicked.connect(self.stop)
        self.Stop_btn.setDisabled(True)

        self.Buy_setting_Gurop = QtWidgets.QGroupBox(Stock_gui)
        self.Buy_setting_Gurop.setGeometry(QtCore.QRect(10, 40, 171, 81))
        self.Buy_setting_Gurop.setObjectName("Buy_setting_Gurop")

        self.All_kospi = QtWidgets.QRadioButton(self.Buy_setting_Gurop)
        self.All_kospi.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.All_kospi.setObjectName("All_kospi")

        self.Auto_recommend_kospi = QtWidgets.QRadioButton(self.Buy_setting_Gurop)
        self.Auto_recommend_kospi.setGeometry(QtCore.QRect(10, 60, 121, 16))
        self.Auto_recommend_kospi.setObjectName("Auto_recommend_kospi")

        self.Kospi_200 = QtWidgets.QRadioButton(self.Buy_setting_Gurop)
        self.Kospi_200.setGeometry(QtCore.QRect(10, 40, 121, 16))
        self.Kospi_200.setObjectName("Kospi_200")
        self.Kospi_200.setChecked(True)

        self.Show_my_stock_btn = QtWidgets.QPushButton(Stock_gui)
        self.Show_my_stock_btn.setGeometry(QtCore.QRect(190, 10, 75, 23))
        self.Show_my_stock_btn.setObjectName("Show_my_stock_btn")
        self.Show_my_stock_btn.setDisabled(True)
        # self.Show_my_stock_btn.clicked.connect(self.test_start)

        self.Show_log_btn = QtWidgets.QPushButton(Stock_gui)
        self.Show_log_btn.setGeometry(QtCore.QRect(280, 10, 75, 23))
        self.Show_log_btn.setObjectName("Show_log_btn")
        # self.Show_log_btn.clicked.connect(self.test_stop)

        self.Key_Settings_Gurop = QtWidgets.QGroupBox(Stock_gui)
        self.Key_Settings_Gurop.setGeometry(QtCore.QRect(190, 40, 161, 80))
        self.Key_Settings_Gurop.setObjectName("Key_Settings_Gurop")

        self.Key_file_btn = QtWidgets.QPushButton(self.Key_Settings_Gurop)
        self.Key_file_btn.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.Key_file_btn.setObjectName("Key_file_btn")
        self.Key_file_btn.clicked.connect(self.set_login_data)

        self.Key_status_label = QtWidgets.QLabel(self.Key_Settings_Gurop)
        self.Key_status_label.setGeometry(QtCore.QRect(10, 50, 71, 21))
        self.Key_status_label.setText("")
        self.Key_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Key_status_label.setObjectName("Key_status_label")

        self.Use_login_check = QtWidgets.QCheckBox(self.Key_Settings_Gurop)
        self.Use_login_check.setGeometry(QtCore.QRect(100, 20, 61, 21))
        self.Use_login_check.setObjectName("Use_login_check")
        self.Use_login_check.setChecked(True)
        self.Use_login_check.clicked.connect(self.check_use_login)

        self.retranslateUi(Stock_gui)
        QtCore.QMetaObject.connectSlotsByName(Stock_gui)

    def retranslateUi(self, Stock_gui):
        self._translate = QtCore.QCoreApplication.translate
        Stock_gui.setWindowTitle(self._translate("Stock_gui", "Auto Stock"))
        self.Start_btn.setText(self._translate("Stock_gui", "Login"))
        self.Stop_btn.setText(self._translate("Stock_gui", "Stop"))
        self.Buy_setting_Gurop.setTitle(self._translate("Stock_gui", "Buy Setting"))
        self.All_kospi.setText(self._translate("Stock_gui", "All Kospi"))
        self.Auto_recommend_kospi.setText(self._translate("Stock_gui", "Auto Recommend"))
        self.Kospi_200.setText(self._translate("Stock_gui", "Kospi 200"))
        self.Show_my_stock_btn.setText(self._translate("Stock_gui", "My Stocks"))
        self.Show_log_btn.setText(self._translate("Stock_gui", "Logs"))
        self.Key_Settings_Gurop.setTitle(self._translate("Stock_gui", "Key Setting"))
        self.Key_file_btn.setText(self._translate("Stock_gui", "Key Files"))
        self.Use_login_check.setText(self._translate("Stock_gui", "Login"))

    def start(self):
        if self.start_st == 0: 
            
            if self.login_thread.isRun == False:
                self.login_thread.isRun = True
                self.login_thread.start()
            
            self.Start_btn.setText(self._translate("Stock_gui", "Start"))

            self.start_st = 1

        elif self.start_st == 1:
            if self.thread.isRun == False:
                self.Stop_btn.setDisabled(False)
                self.Show_my_stock_btn.setDisabled(False)
                self.Start_btn.setDisabled(True)
                self.Auto_recommend_kospi.setDisabled(True)
                self.All_kospi.setDisabled(True)
                self.Kospi_200.setDisabled(True)
                self.Use_login_check.setDisabled(True)
                
                if self.All_kospi.isChecked():
                    kind = 'all'
                elif self.Kospi_200.isChecked():
                    kind = 'kospi200'
                elif self.Auto_recommend_kospi.isChecked():
                    kind = 'auto'

                self.thread.stock.load_data(kind)
                self.thread.isRun = True
                self.thread.start()
    
    def stop(self):
        self.thread.isRun = False
        self.Stop_btn.setDisabled(True)
        self.Start_btn.setDisabled(False)
        self.Auto_recommend_kospi.setDisabled(False)
        self.All_kospi.setDisabled(False)
        self.Kospi_200.setDisabled(False)

    def get_data(self, data):
        self.stock.user_inform_data['my stock'] = data
        self.stock.save_data()

    def check_use_login(self):
        if self.Use_login_check.isChecked():
            self.start_st = 0
            self.Start_btn.setText(self._translate("Stock_gui", "Login"))
            self.Start_btn.setDisabled(True)
            self.Show_my_stock_btn.setDisabled(True)
            self.Key_file_btn.setDisabled(False)

        else:
            self.start_st = 1
            self.Start_btn.setText(self._translate("Stock_gui", "Start"))
            self.Start_btn.setDisabled(False)
            self.Show_my_stock_btn.setDisabled(False)
            self.Key_file_btn.setDisabled(True)

    def set_login_data(self):
        key_file = QtWidgets.QFileDialog.getOpenFileName(None, "Open Key")
        key_file_path = key_file[0]
        status = self.stock.set_up(key_file_path)
        
        if status == 'complete':
            self.login_thread.user_data = self.stock.user_inform_data['key'] 
            self.Key_status_label.setText(self._translate("Stock_gui", "Complete"))
            self.Use_login_check.setDisabled(True)
            self.Key_file_btn.setDisabled(True)
            self.Start_btn.setDisabled(False)

        elif status == 'fail':
            self.Key_status_label.setText(self._translate("Stock_gui", "Fail"))



