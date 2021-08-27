from os import path
from dynamic_import import dynamic_import
import os

if __name__ == "__main__":
    path = str(os.getcwd()) + "\\stock_main"
    dynamic = dynamic_import.dynamic_import(path)
    dynamic.run()