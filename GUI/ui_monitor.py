from PySide2.QtWidgets import QWidget, QPushButton, QLabel
from PySide2.QtGui import QPainter, QColor, QPainterPath, QTransform, QPen, QFont
from PySide2.QtCore import QTimer, Qt, QObject

from Management.map_management import MapManagement
from Management.robot_management import RobotManagement


class LayerMap(QWidget):
    _instance = None
    size_x = 1920  # kich thuoc x widget
    size_y = 975  # kich thuoc y widget
    zone_x = 1860  # kich thuoc x vung hien thi map
    zone_y = 915  # kich thuoc y vung hien thi map
    start_x = 30  # vi tri x bat dau hien thi map
    start_y = 30  # vi tri y bat dau hien thi map
    node_diameter = 10
    res = 0
    list_robot = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if hasattr(self, '_initialized'):
            return
        super().__init__(parent)
        self._initialized = True

        self.resize(self.size_x, self.size_y)
        self.move(0, 0)

        max_x = 0
        max_y = 0
        for node in MapManagement().map_coordinate.values():
            if max_x < node[0]:
                max_x = node[0]
            if max_y < node[1]:
                max_y = node[1]
        self.res = max(((max_x + 3000) / self.zone_x), ((max_y + 3000) / self.zone_y))
        WidRobot.res = self.res
        WidRobot.robot_diameter = (960 / self.res)

        for node in MapManagement().map_coordinate.values():
            self.create_node(node)
        for robot in RobotManagement().list_robot.values():
            self.list_robot[robot.robot_id] = WidRobot(self, robot.robot_id, robot.coordinate[0], robot.coordinate[1])

    def create_node(self, coordinate):
        x = self.start_x + (coordinate[0]+1500)//self.res - self.node_diameter//2
        y = self.size_y - ((self.start_y + (coordinate[1]+1500)//self.res) + self.node_diameter//2)
        point = QPushButton(self)
        point.setGeometry(x, y, self.node_diameter, self.node_diameter)
        point.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #a0a0a0;
                        border-radius: {self.node_diameter//2}px;
                    }}
                    QPushButton:hover {{
                        background-color: #ff0000;
                    }}
                """)


class WidRobot(QWidget):
    robot_diameter = None
    map_size_x = LayerMap.size_x
    map_size_y = LayerMap.size_y
    map_start_x = LayerMap.start_x
    map_start_y = LayerMap.start_y
    res = 0

    def __init__(self, parent=None, robot_id=None, coordinate_x=0, coordinate_y=0):
        super().__init__(parent)
        self.robot_id = robot_id
        self.resize(self.robot_diameter, self.robot_diameter)
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

        self.timer_update_robot = QTimer(self)
        self.timer_update_robot.timeout.connect(self.update_state)
        self.timer_update_robot.start(30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Chống răng cưa
        # Tạo màu và vẽ hình tròn
        painter.setBrush(QColor(100, 100, 100))  # Màu nền của hình tròn
        painter.setPen(Qt.NoPen)  # Không viền cho hình tròn

        # Vẽ hình tròn tại giữa widget
        radius = min(self.width(), self.height()) // 2  # Tính bán kính
        center_x = self.width() // 2
        center_y = self.height() // 2

        painter.drawEllipse(center_x - radius, center_y - radius, 2 * radius, 2 * radius)

    def update_state(self):
        robot_coordinate = RobotManagement().list_robot[self.robot_id].coordinate
        self.coordinate_x = robot_coordinate[0]
        self.coordinate_y = robot_coordinate[1]

        x = self.map_start_x + (self.coordinate_x + 1500) // self.res - self.robot_diameter // 2
        y = self.map_size_y - ((self.map_start_y + (self.coordinate_y + 1500) // self.res) + self.robot_diameter // 2)
        self.move(x, y)
        self.update()
        self.show()


