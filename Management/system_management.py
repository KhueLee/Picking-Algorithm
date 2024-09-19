from datetime import datetime
import time
import threading

from Management.map_management import MapManagement
from Management.robot_management import RobotManagement


class SystemManagement:
    is_start = True
    _instance = None
    state = {}
    data_config = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def start_system(self, data_config):
        self.data_config = data_config
        map_name = self.data_config["map_name"]
        self.state["map_name"] = map_name

        MapManagement().load_map_from_zip(f"ConfigSystem/Map/{map_name}.zip")
        RobotManagement().init_robot(data_config["number_of_robot"], data_config["robot_param"])

        self.state["start_time"] = datetime.now()
        self.state["runtime"] = 0
        threading.Thread(target=self.update_system_state_1s).start()

    def update_system_state_1s(self):
        while self.is_start:
            self.state["runtime"] = round((datetime.now() - self.state["start_time"]).total_seconds())
            self.state["no_thread"] = threading.active_count()
            time.sleep(1)