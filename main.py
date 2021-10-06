import sys, os
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
sys.path.append(os.path.abspath('stock'))
from PyQt5 import QtWidgets
from stock.gui import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Stock_gui = QtWidgets.QWidget()
    ui = gui.Ui_Stock_gui()
    ui.setupUi(Stock_gui)
    Stock_gui.show()
    sys.exit(app.exec_())