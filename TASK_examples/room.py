
i = 1

class Room:
    def __init__(self, room_dict):
        global i
        self.id = i
        i += 1
        self.height = room_dict['height']
        self.width = room_dict['width']
        self.area = self.length * self.width
        if (room_dict['type'].lower() == "workroom"):
            self.type = "workplace"
        else:
            self.type = "meeting"
    
