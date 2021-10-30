from typing import overload
from room import Room

from enum import Enum

OVERLAP_CONST = 66666

class FloorType(Enum):
    OPEN = -1


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
        
        self.workpl_ids = [i for i in range(len(self.rooms)) if self.rooms[i] == "workplaces"]
        self.meet_ids = [i for i in range(len(self.rooms)) if self.rooms[i] == "meeting"]

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
            return False# Out of borders
        for i in range(room.width):
            for j in range(room.height):
                if self.layout[1][x+i][y+j] != -1:
                    self.layout[1][x+i][y+j] = roomId
                else:
                    self.restore_object(room, x, y, roomId)
                    return False
        room.set_coords(x, y)
        return True

    def restore_object(self, room, x, y, roomId):
        if not self.sanity_check(room, x, y):
            return # Out of borders, object was not placed
        for i in range(room.width):
            for j in range(room.height):
                if self.layout[1][x+i][y+j] == roomId:
                    self.layout[1][x+i][y+j] = -1
        room.detach_coords()

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
        room.set_coords(x, y)
        return overlap

    def sanity_check(self, room, x, y):
        if x + room.width > self.width:
            return False
        if y + room.height > self.height:
            return False
        if x < 0 or y < 0:
            return False
        return True

    def restore_layout(self):
        self.layout = [self.layout[0], [[-1]*self.height]*self.width]

    def placing_done(self):
        self.layout = [self.layout[1], [[-1]*self.height]*self.width]

    def fitness(self):
        fit_score = 0
        for i, r in enumerate(self.rooms):
            x, y, w, h = r.x, r.y, r.width, r.height
            if r.type == "workplace":
                walls = [x == 0, y == 0, x+w == self.width, y+h == self.height]
                fit_score += 5 * sum(walls)
                flag, score = self.access_to_ids(r, i, [-1]) # Access to open space
                if flag: 
                    fit_score += 3
                flag, neig_work = self.access_to_ids(r, i, self.workpl_ids) # Next to other workplaces
                if flag:
                    fit_score += score
            else: # meeting rooms
                flag, score = self.access_to_ids(r, i, [-1]) # Access to open space
                if flag: 
                    fit_score += 3
                flag, neig_work = self.access_to_ids(r, i, self.meet_ids) # Next to other workplaces
                if flag:
                    fit_score += neig_work * 2
        return fit_score

    def access_to_ids(self, room, roomId, ids):
        # ids is list of number for which we search connection
        # returns (flag, count of access to different rooms/types)
        r = room
        flag = False
        access_cnt = 0
        accessed_floors = []
        # wrapper around object
        x, y, w, h = (max(0, r.x-1), max(0, r.y-1), 
                     min(r.x+r.width+2, self.width), 
                     min(r.y+r.height+2, self.height))
        for x_coord in range(x, w):
            for y_coord in range(y, h):
                field = self.layout[0][x_coord][y_coord] # ACTUAL SHOULD BE AT 0 index
                if field in ids and field not in accessed_floors:
                    flag = True # Just one is enough :D
                    access_cnt += 1
                    accessed_floors.append(field)
        return flag, access_cnt

        for i, r in enumerate(self.rooms()):
            if i == roomId:
                continue


