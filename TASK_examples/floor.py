from typing import overload
from room import Room

OVERLAP_CONST = 66666

class Floor:
    def __init__(self, width, height, rooms):
        #  0,0 is top left
        #  0, max is top right
        #  max, 0 is bottom left
        #  max, max is bottom right
        self.width = width
        self.height = height
        self.resolution = width * height
        self.layout= [[[-1]*height]*width,  # grid of 100x100, everything is 0 for now
                     [[-1]*height]*width]   # prev and modified version
        self.rooms = [Room(room) for room in rooms]
        
        summarize = 0
        
        for room in self.rooms:
            summarize += room.area

            if (room.width > self.width and room.height > self.width) or (room.height > self.width and room.width > self.width):
                raise RuntimeError('Can\'t fit the room sizes')
            if room.width > self.width or room.height > self.height:
                room.width, room.height = room.height, room.width
        
        if summarize > width*height:
            raise RuntimeError('The area is too large to fit the floor')

        self.midx = height // 2
        self.midy = width // 2

    def place_room(self, roomId, x, y):
        room = self.rooms[roomId]
        if not self.sanity_check(room, x, y):
            return # Out of borders
        for i in range(room.width):
            for j in range(room.height):
                if self.layout[1][x+i][y+j] != -1:
                    self.layout[1][x+i][y+j] = roomId
                else:
                    self.restore_object(room, x, y, roomId)
                    return False
        return True

    def restore_object(self, room, x, y, roomId):
        if not self.sanity_check(room, x, y):
            return # Out of borders, object was not placed
        for i in range(room.width):
            for j in range(room.height):
                if self.layout[1][x+i][y+j] == roomId:
                    self.layout[1][x+i][y+j] = -1

    def place_relax(self, roomId, x, y):
        # It wont place the room unless it overlap
        room = self.rooms[roomId]
        overlap = 0
        if not self.sanity_check(room, x, y):
            return OVERLAP_CONST # Out of borders, object was not placed
        for i in range(room.width):
            for j in range(room.height):
                if self.layout[1][x+i][y+j] != -1:
                    self.layout[1][x+i][y+j] = roomId
                else:
                    overlap += 1
        # Point for a try should be kept as it drastically change the overlap?
        # if overlap > 0:
        #     self.restore_object(room, x, y, roomId)
        return overlap

    def sanity_check(self, room, x, y):
        if x + room.width > self.width:
            return False
        if y + room.height > self.height:
            return False
        return True

    def restore_layout(self):
        self.layout = [self.layout[0], [[-1]*self.height]*self.width]

    def placing_done(self):
        self.layout = [self.layout[1], [[-1]*self.height]*self.width]

    def get_score():
        print("You win! :)")
    
