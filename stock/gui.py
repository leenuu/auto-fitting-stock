from PyQt5 import QtCore, QtGui, QtWidgets
from stock.basic import *

class Ui_Stock_gui(object):
    def setupUi(self, Stock_gui):

        Stock_gui.setObjectName("Stock_gui")
        Stock_gui.resize(367, 134)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\img/chart-line-g3a7c2e109_1280.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Stock_gui.setWindowIcon(icon)

        self.Start_btn = QtWidgets.QPushButton(Stock_gui)
        self.Start_btn.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.Start_btn.setObjectName("Start_btn")

        self.Stop_btn = QtWidgets.QPushButton(Stock_gui)
        self.Stop_btn.setGeometry(QtCore.QRect(100, 10, 75, 23))
        self.Stop_btn.setObjectName("Stop_btn")

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

        self.Show_my_stock_btn = QtWidgets.QPushButton(Stock_gui)
        self.Show_my_stock_btn.setGeometry(QtCore.QRect(190, 10, 75, 23))
        self.Show_my_stock_btn.setObjectName("Show_my_stock_btn")

        self.Show_log_btn = QtWidgets.QPushButton(Stock_gui)
        self.Show_log_btn.setGeometry(QtCore.QRect(280, 10, 75, 23))
        self.Show_log_btn.setObjectName("Show_log_btn")

        self.Key_Settings_Gurop = QtWidgets.QGroupBox(Stock_gui)
        self.Key_Settings_Gurop.setGeometry(QtCore.QRect(190, 40, 161, 80))
        self.Key_Settings_Gurop.setObjectName("Key_Settings_Gurop")

        self.Key_file_btn = QtWidgets.QPushButton(self.Key_Settings_Gurop)
        self.Key_file_btn.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.Key_file_btn.setObjectName("Key_file_btn")

        self.Key_status_label = QtWidgets.QLabel(self.Key_Settings_Gurop)
        self.Key_status_label.setGeometry(QtCore.QRect(10, 50, 71, 21))
        self.Key_status_label.setText("")
        self.Key_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Key_status_label.setObjectName("Key_status_label")

        self.Use_login_check = QtWidgets.QCheckBox(self.Key_Settings_Gurop)
        self.Use_login_check.setGeometry(QtCore.QRect(100, 20, 61, 21))
        self.Use_login_check.setObjectName("Use_login_check")

        self.retranslateUi(Stock_gui)
        QtCore.QMetaObject.connectSlotsByName(Stock_gui)

    def retranslateUi(self, Stock_gui):
        _translate = QtCore.QCoreApplication.translate
        Stock_gui.setWindowTitle(_translate("Stock_gui", "Auto Stock"))
        self.Start_btn.setText(_translate("Stock_gui", "Start"))
        self.Stop_btn.setText(_translate("Stock_gui", "Stop"))
        self.Buy_setting_Gurop.setTitle(_translate("Stock_gui", "Buy Setting"))
        self.All_kospi.setText(_translate("Stock_gui", "All Kospi"))
        self.Auto_recommend_kospi.setText(_translate("Stock_gui", "Auto Recommend"))
        self.Kospi_200.setText(_translate("Stock_gui", "Kospi 200"))
        self.Show_my_stock_btn.setText(_translate("Stock_gui", "My Stocks"))
        self.Show_log_btn.setText(_translate("Stock_gui", "Logs"))
        self.Key_Settings_Gurop.setTitle(_translate("Stock_gui", "Key Setting"))
        self.Key_file_btn.setText(_translate("Stock_gui", "key_files"))
        self.Use_login_check.setText(_translate("Stock_gui", "Login"))



