import threading
import sys
import json

from GUI.main_GUI_sim import MainWindow
from GUI.ui_gui_sim import *
from Management.system_management import SystemManagement


def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


def read_config(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    config_path = "ConfigSystem/config.json"
    data_config = read_config(config_path)
    SystemManagement().start_system(data_config)
    threading.Thread(target=start_gui).start()
