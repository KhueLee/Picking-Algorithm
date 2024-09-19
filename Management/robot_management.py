from Device.Robot import Robot
from Management.map_management import MapManagement


class RobotManagement:
    _instance = None
    list_robot = {}

    # single ton class robot management
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def init_robot(self, number_of_robot):
        for i in range(number_of_robot):
            robot_id = f"Robot_{i}"
            node_id = MapManagement().map_data["nodes"][i]["id"]
            self.list_robot[robot_id] = Robot(robot_id, node_id)

