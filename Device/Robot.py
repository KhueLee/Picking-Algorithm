import threading

from Management.map_management import MapManagement
import math
from datetime import datetime
import time
import random


class Robot:
    robot_moving_config = None

    def __init__(self, robot_id, node_id):
        self.robot_id = robot_id
        self.current_node_id = node_id
        self.task = None
        self.is_moving = False
        self.freq_update = self.robot_moving_config["freq"]
        coordinate = MapManagement().map_coordinate[self.current_node_id]
        self.v = 0
        self.a = 0
        self.t_a = 0
        self.d_a = 0
        self.coordinate_current = [coordinate[0], coordinate[1]]
        self.coordinate_start = [coordinate[0], coordinate[1]]
        self.coordinate_target = [coordinate[0], coordinate[1]]
        self.time_start_move = datetime.now()
        self.robot_sub_task = RobotSubTask(self)
        self.robot_task = RobotTask(self)

    def move_sim(self, node_target, is_load):
        self.is_moving = True
        coordinate_target = MapManagement().map_coordinate[node_target]
        self.coordinate_target = [coordinate_target[0], coordinate_target[1]]
        if is_load:
            self.v = self.robot_moving_config["load"]["velocity"]
            self.a = self.robot_moving_config["load"]["acc"]
        else:
            self.v = self.robot_moving_config["noload"]["velocity"]
            self.a = self.robot_moving_config["noload"]["acc"]
        self.t_a = self.v/self.a
        self.d_a = self.v * self.t_a / 2

        if self.coordinate_target[0] == self.coordinate_current[0]:
            self.coordinate_start[1] = self.coordinate_current[1]
            distance = (self.coordinate_target[1] - self.coordinate_start[1])
            sign = math.copysign(1, distance)
            distance = abs(distance)

            if distance > (self.d_a * 2):
                t_keep = (distance - self.d_a * 2) / self.v
                self.time_start_move = datetime.now()
                self.calculate_move_y_trapezium_profile(t_keep, sign)
            else:
                t_acc = math.sqrt(distance / self.a)
                self.time_start_move = datetime.now()
                self.calculate_move_y_triangle_profile(t_acc, sign)

        elif self.coordinate_target[1] == self.coordinate_current[1]:
            self.coordinate_start[0] = self.coordinate_current[0]
            distance = (self.coordinate_target[0] - self.coordinate_start[0])
            sign = math.copysign(1, distance)
            distance = abs(distance)
            if distance > (self.d_a * 2):
                t_keep = (distance - self.d_a * 2) / self.v
                self.time_start_move = datetime.now()
                self.calculate_move_x_trapezium_profile(t_keep, sign)
            else:
                t_acc = math.sqrt(distance/self.a)
                self.time_start_move = datetime.now()
                self.calculate_move_x_triangle_profile(t_acc, sign)
        else:
            return False

    def calculate_move_x_trapezium_profile(self, t_keep, sign):
        while self.is_moving:
            time.sleep(1 / self.freq_update)
            t = (datetime.now() - self.time_start_move).total_seconds()
            if t < self.t_a:
                self.coordinate_current[0] = self.coordinate_start[0] + sign * (self.a * t * t) / 2
            elif t < (self.t_a + t_keep):
                self.coordinate_current[0] = self.coordinate_start[0] + sign * (self.d_a + self.v * (t - self.t_a))
            elif t < (self.t_a * 2 + t_keep):
                self.coordinate_current[0] = self.coordinate_start[0] + sign * (self.d_a + self.v * t_keep + self.v * (t - self.t_a - t_keep) - self.a * (t - self.t_a - t_keep) * (t - self.t_a - t_keep) / 2)
            else:
                self.coordinate_current[0] = self.coordinate_target[0]
                break
        self.is_moving = False
        self.end_moving()

    def calculate_move_x_triangle_profile(self, t_acc, sign):
        while self.is_moving:
            time.sleep(1 / self.freq_update)
            t = (datetime.now() - self.time_start_move).total_seconds()

            if t < t_acc:
                self.coordinate_current[0] = self.coordinate_start[0] + sign * (self.a * t * t) / 2
            elif t < (t_acc * 2):
                self.coordinate_current[0] = self.coordinate_start[0] + sign * self.a * t_acc * t_acc / 2 + sign * ((t_acc * self.a) * (t - t_acc) - self.a * (t - t_acc) * (t - t_acc) / 2)
            else:
                self.coordinate_current[0] = self.coordinate_target[0]
                break
        self.is_moving = False
        self.end_moving()

    def calculate_move_y_trapezium_profile(self, t_keep, sign):
        while self.is_moving:
            time.sleep(1 / self.freq_update)
            t = (datetime.now() - self.time_start_move).total_seconds()

            if t < self.t_a:
                self.coordinate_current[1] = self.coordinate_start[1] + sign * (self.a * t * t) / 2
            elif t < (self.t_a + t_keep):
                self.coordinate_current[1] = self.coordinate_start[1] + sign * (self.d_a + self.v * (t - self.t_a))
            elif t < (self.t_a * 2 + t_keep):
                self.coordinate_current[1] = self.coordinate_start[1] + sign * (self.d_a + self.v * t_keep + self.v * (t - self.t_a - t_keep) - self.a * (t - self.t_a - t_keep) * (t - self.t_a - t_keep) / 2)
            else:
                self.coordinate_current[1] = self.coordinate_target[1]
                break
        self.is_moving = False
        self.end_moving()

    def calculate_move_y_triangle_profile(self, t_acc, sign):
        while self.is_moving:
            time.sleep(1 / self.freq_update)
            t = (datetime.now() - self.time_start_move).total_seconds()

            if t < t_acc:
                self.coordinate_current[1] = self.coordinate_start[1] + sign * (self.a * t * t) / 2
            elif t < (t_acc * 2):
                self.coordinate_current[1] = self.coordinate_start[1] + sign * self.a * t_acc * t_acc / 2 + sign * ((t_acc * self.a) * (t - t_acc) - self.a * (t - t_acc) * (t - t_acc) / 2)
            else:
                self.coordinate_current[1] = self.coordinate_target[1]
                break
        self.is_moving = False
        self.end_moving()

    def end_moving(self):
        self.coordinate_current[0] = int(self.coordinate_current[0])
        self.coordinate_current[1] = int(self.coordinate_current[1])
        if self.coordinate_current == self.coordinate_target:
            self.current_node_id = MapManagement().map_id[(self.coordinate_current[0], self.coordinate_current[1])]
            # self.is_completed = True
            self.is_moving = False


class RobotTask:
    def __init__(self, robot):
        self.robot = robot
        threading.Thread(target=self.move_empty, args=("1",)).start()

    def move_rack(self, rack_id, rack_from_node, rack_to_node):
        self.robot.robot_sub_task.move_no_load(rack_from_node)
        self.robot.robot_sub_task.load()
        self.robot.robot_sub_task.move_with_load(rack_to_node)
        self.robot.robot_sub_task.unload()

    def move_empty(self, to_node):
        # time.sleep(1)
        # while True:
        node_target = random.choice(list(MapManagement().map_coordinate.keys()))
        self.robot.robot_sub_task.move_no_load(node_target)

    def charging(self):
        pass


class RobotSubTask:
    def __init__(self, robot):
        self.robot = robot

    def move_no_load(self, to_node_id):
        print(self.robot.robot_id, "move from", self.robot.current_node_id, to_node_id)
        path_plan = MapManagement().astar(self.robot.current_node_id, to_node_id, False)
        print(self.robot.robot_id, path_plan)
        safe_point = 0
        while self.robot.current_node_id != path_plan[-1] and path_plan is not None:
            coordinate_next = MapManagement().map_coordinate[path_plan[safe_point+1]]
            if coordinate_next[0] == self.robot.coordinate_current[0] or coordinate_next[1] == self.robot.coordinate_current[1]:
                safe_point += 1
            else:
                self.robot.move_sim(path_plan[safe_point], False)

            if safe_point+1 == len(path_plan):
                self.robot.move_sim(path_plan[-1], False)

    def move_with_load(self, to_node_id):
        path_plan = MapManagement().astar(self.robot.current_node_id, to_node_id, True)
        safe_point = 0
        while self.robot.current_node_id != path_plan[-1] and path_plan is not None:
            coordinate_next = MapManagement().map_coordinate[path_plan[safe_point + 1]]
            if coordinate_next[0] == self.robot.coordinate_current[0] or coordinate_next[1] == \
                    self.robot.coordinate_current[1]:
                safe_point += 1
            else:
                self.robot.move_sim(path_plan[safe_point], False)

            if safe_point + 1 == len(path_plan):
                self.robot.move_sim(path_plan[-1], False)

    def rotate(self):
        pass

    def load(self):
        time.sleep(2)

    def unload(self):
        time.sleep(2)

    def charge(self):
        pass

    def discharge(self):
        pass

    def scan_rack(self):
        time.sleep(2)

