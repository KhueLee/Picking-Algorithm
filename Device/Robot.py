from Management.map_management import MapManagement


class Robot:
    def __init__(self, robot_id, node_id):
        self.robot_id = robot_id
        self.node_id = node_id
        self.task = None
        self.is_moving = False
        self.coordinate = MapManagement().map_coordinate[self.node_id]

        self.robot_task = RobotTask(self)
        self.robot_sub_task = RobotSubTask(self)


class RobotTask:
    def __init__(self, robot):
        self.robot = robot

    def move_rack(self, rack_id, rack_from, rack_to):
        pass

    def move_empty(self, move_from, move_to):
        pass

    def charging(self):
        pass


class RobotSubTask:
    def __init__(self, robot):
        self.robot = robot

    def move_no_load(self):
        pass

    def move_with_load(self):
        pass

    def rotate(self):
        pass

    def load(self):
        pass

    def unload(self):
        pass

    def charge(self):
        pass

    def discharge(self):
        pass

    def scan_rack(self):
        pass

