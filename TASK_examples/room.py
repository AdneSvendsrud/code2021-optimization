
class Room:
    def __init__(self, room_dict):
        self.height = room_dict['height']
        self.width = room_dict['width']
        self.area = self.length * self.width
        if (room_dict['type'].lower() == "workroom"):
            self.type = "workplace"
        else:
            self.type = "meeting"
        self.x = -1
        self.y = -1

    def set_coords(self, x, y):
        self.x, self.y = x, y

    def detach_coords(self):
        self.x, self.y = -1, -1
