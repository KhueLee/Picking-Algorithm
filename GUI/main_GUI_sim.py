import sys
from GUI.ui_gui_sim import *
from GUI.ui_monitor import *
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        ################################################################################################################
        # Init cửa sổ
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.showFullScreen()  # Hiển thị cửa sổ full màn hình
        self.setWindowFlags(self.windowFlags() or Qt.FramelessWindowHint)  # Tắt thanh control box
        LayerMap(self.ui.wid_monitor).show()
        # self.ui.lb_map_name.setText(SystemManagement().state["map_name"])
        self.timer_update_state = QTimer(self)
        self.timer_update_state.timeout.connect(self.update_state)
        self.timer_update_state .start(1000)

    def update_state(self):
        # self.ui.lb_runtime.setText(str(datetime.timedelta(seconds=SystemManagement().state["runtime"])))
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

