import threading
import sys

from GUI.main_GUI_sim import MainWindow
from GUI.ui_gui_sim import *


def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # SystemManagement().start_system()
    threading.Thread(target=start_gui).start()
