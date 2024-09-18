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

    def add_robot(self):
        pass