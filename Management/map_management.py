import threading
import zipfile
import json
import heapq
from datetime import datetime


# Class for map management
class MapManagement:
    _instance = None
    map_data = None

    list_shelf = []     # array id of node which have shelf
    list_station = []   # array id of node which have station

    map_id = {}     # map with key is coordinate, value is id
    map_coordinate = {}     # map with key is id, value is coordinate
    map_node = {}   # map with key is coordinate, value is node
    map_reg = {}  # map with key is id, value is list robot register
    map_lock = {}  # map with key is id, value is lock thread
    map_edge = {}   # map with key is id, value is array node edge

    # single ton class robot management
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    # (need test)
    # function for load map to server with input is map data
    def import_map_to_system(self, map_data):
        self.map_data = map_data
        nodes = map_data["nodes"]

        for node in nodes:
            id_node = node["id"]
            x = int(node["coordinate"]["x"])
            y = int(node["coordinate"]["y"])

            self.map_coordinate[id_node] = (x, y)
            self.map_id[(x, y)] = id_node
            self.map_node[id_node] = node
            self.map_reg[id_node] = {}
            self.map_lock[id_node] = threading.Lock()
            self.map_edge[id_node] = []

            for edge in node['edges']:
                self.map_edge[id_node].append(edge["destination"])

            if node["type"] == 1 or node["type"] == 3:  # 1 for Rack area and 3 for Load area
                self.list_shelf.append(id_node)

    # (need test)
    # function for load map from zip map, import map to database and import map to server
    def load_map_from_zip(self, map_path):
        map_data = None
        with zipfile.ZipFile(map_path, 'r') as zip_ref:
            with zip_ref.open('topo.json') as f:
                map_data = json.load(f)

        extracted_data = {
            'name': map_data.get('map', {}).get('name'),
            'width': map_data.get('map', {}).get('width'),
            'height': map_data.get('map', {}).get('height'),
            'nodes': []
        }

        for node in map_data.get('nodes', []):
            extracted_node = {
                'id': node.get('id'),
                'edges': node.get('edges'),
                'type': node.get('type'),
                'coordinate': node.get('coordinate')
            }
            extracted_data['nodes'].append(extracted_node)

            # Load map to system
            self.import_map_to_system(extracted_data)

        return extracted_data

    # (need DEV)
    # function for path planning using A*
    def astar(self, node_start, node_end, is_lift_rack):
        # function calculate heuristic for A*
        def heuristic(node_a, node_b):
            return (abs(self.map_coordinate[node_a][0] - self.map_coordinate[node_b][0]) +
                    abs(self.map_coordinate[node_a][1] - self.map_coordinate[node_b][1]))

        open_list = []
        close_list = []
        heapq.heappush(open_list, (0, node_start))
        came_from = {}
        g_score = {node_start: 0}
        f_score = {node_start: heuristic(node_start, node_end)}

        turn_penalty = 10

        while open_list:
            current = heapq.heappop(open_list)[1]
            if current == node_end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(node_start)
                path.reverse()

                path_coordinate = []
                for node_id in reversed(path):
                    path_coordinate.append(node_id)
                path_coordinate.reverse()
                return path
            close_list.append(current)

            map_edge = {}
            for edge in self.map_edge[current]:
                map_edge[edge] = heuristic(edge, node_end)

            map_sorted = dict(sorted(map_edge.items(), key=lambda item: item[1], reverse=True))
            print(map_sorted)

            for edge in map_sorted.keys():

                if edge in close_list:
                    continue

                if edge not in self.list_shelf:
                    tentative_g_score = g_score[current] + heuristic(current, edge)
                    # Check turn
                    if current in came_from:
                        previous_node = came_from[current]
                        if ((self.map_coordinate[current][0] - self.map_coordinate[previous_node][0],
                            self.map_coordinate[current][1] - self.map_coordinate[previous_node][1]) !=
                                (self.map_coordinate[edge][0] - self.map_coordinate[current][0],
                                 self.map_coordinate[edge][1] - self.map_coordinate[current][1])):
                            tentative_g_score += turn_penalty

                    if edge not in g_score or tentative_g_score < g_score[edge]:
                        came_from[edge] = current
                        g_score[edge] = tentative_g_score
                        f_score[edge] = tentative_g_score + heuristic(edge, node_end)
                        heapq.heappush(open_list, (f_score[edge], edge))
        return None

    # (need DEV)
    # function for calculate segment task
    def get_segment_task(self, path_id):
        path_coord = self.convert_to_coordinate(path_id)
        segments = []
        current_index = 1

        while current_index <= len(path_coord) - 1:
            control_index = current_index

            for index in range(current_index + 1, len(path_coord)):
                if self.is_turn_point(path_coord[current_index], path_coord[index]):
                    control_index = index - 1
                    break

            if control_index == current_index:
                control_index = len(path_coord) - 1

            segment = {
                "path_id": [],
                "path_coord": [],
                "is_last": control_index == len(path_coord) - 1
            }
            for path_index in range(current_index, control_index + 1):
                # print(f"Path plan: {path_coord[path_index]}")
                segment["path_coord"].append(path_coord[path_index])
                segment["path_id"].append(path_id[path_index])
            segments.append(segment)
            current_index = control_index + 1

        return segments

    def is_turn_point(self, start, end):
        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])

        return dx != 0 and dy != 0

    def convert_to_coordinate(self, path_plan_id):
        coordinates = []
        for path in path_plan_id:
            coordinates.append(MapManagement.map_coordinate[path])
        return coordinates


MapManagement().load_map_from_zip("Winmart_1909.zip")
print(datetime.now())
print(MapManagement().astar("10000008", "10001484", False))
print(datetime.now())

