import os

class dynamic_import:

    def __init__(self, path):
        self.import_path = path
        self.import_name_list = os.listdir(self.import_path)
        self.import_list = dict()

    def reload(self):
        for import_file in self.import_name_list:
            if '.py' in import_file:
                if '__intit__': 
                    pass
                # exec(f"from mode import {mode_file[:len(mode_file)-3]}")
                # importlib.import_module(f'{mode_file[:len(mode_file)-3]}',[])
                mode_name = f'mode.{import_file[:len(import_file)-3]}'
                mod = __import__(f'{mode_name}', fromlist=[mode_name])
                self.import_list[import_file[:len(import_file)-3]] = mod
                print(f'{mode_name} reloaded!')

        print(self.import_list)
    
    def edit_file(self):
        pass

    def try_cmd(self, import_file, cmd):
        try:
            exec(f"self.import_list['{import_file}'].{cmd}")
        except KeyError:
            print("No command")

    def run(self):
        while True:
            cmd = str(input("Dynamic Import > "))

            if cmd == "cls" or cmd == "clear":
                os.system("cls")

            elif cmd == "edit file":
                pass
                
            elif cmd == "reload":
                self.reload()

            elif cmd == "start":
                pass

            elif cmd == "exit":
                break
