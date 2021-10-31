import copy
from typing import overload
from room import Room

from enum import Enum

OVERLAP_CONST = 66666

class FloorType(Enum):
    OPEN = -1

fl_id = 0
C = 99


class Floor:
    def __init__(self, width, height, rooms):
        #  0,0 is top left
        #  0, max is top right
        #  max, 0 is bottom left
        #  max, max is bottom right
        global fl_id
        self.id = fl_id
        fl_id += 1
        self.width = width
        self.height = height
        self.resolution = width * height
        self.layout= [[-1]*height for i in range(width)]  # grid of 100x100, everything is 0 for now
                     #[[-1]*height for i in range(width)]]   # prev and modified version
        
        self.rooms = [Room(room) for room in rooms['rooms']]
        
        self.workpl_ids = [i for i in range(len(self.rooms)) if self.rooms[i].type == "workplace"]
        self.meet_ids = [i for i in range(len(self.rooms)) if self.rooms[i].type == "meeting"]

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

        self.memory = [] # array of arrays of rooms FIFO last 10
        self.init_mem = []

    def store_init_state(self):
        self.init_mem.append(copy.deepcopy(self.rooms))

    def store_state(self):
        if len(self.memory) > 10:
            self.memory  = self.memory[1:]
        self.memory.append(copy.deepcopy(self.rooms))

    def get_memory(self):
        self.init_mem.extend(self.memory)
        return self.init_mem

    def place_room(self, roomId, x, y):
        room = self.rooms[roomId]
        if not self.sanity_check(room, x, y):
            return False# Out of borders
        for i in range(room.width):
            for j in range(room.height):
                if self.layout[x+i][y+j] == -1:
                    self.layout[x+i][y+j] = roomId
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
                if self.layout[x+i][y+j] == roomId:
                    self.layout[x+i][y+j] = -1
        # room.detach_coords()

    def place_relax(self, roomId, x, y):
        # It wont place the room unless it overlap
        room = self.rooms[roomId]
        overlap = 0
        if not self.sanity_check(room, x, y):
            return OVERLAP_CONST # Out of borders, object was not placed
        for i in range(room.width):
            for j in range(room.height):
                if self.layout[x+i][y+j] == -1:
                    self.layout[x+i][y+j] = roomId
                else:
                    overlap += 1
                    # print("overlaping ", x+i, y+j, room.width, room.height)
        # Point for a try should be kept as it drastically change the overlap?
        # if overlap > 0:
        #     self.restore_object(room, x, y, roomId)
        # print("Here we are..." ,x, y)
        # self.print_layout(self)
        #room.set_coords(x, y)
        return overlap

    def sanity_check(self, room, x, y):
        if x + room.width > self.width:
            return False
        if y + room.height > self.height:
            return False
        if x < 0 or y < 0:
            return False
        return True

    # def restore_layout(self):
    #     self.layout = [self.layout[0], [[-1]*self.height]*self.width]

    # def placing_done(self):
    #     self.layout = [self.layout[1], [[-1]*self.height]*self.width]

    def fitness(self):
        fit_score = 0
        correctness = True

        for i, r in enumerate(self.rooms):
            x, y, w, h = r.x, r.y, r.width, r.height
            if r.type == "workplace":
                walls = [x == 0, y == 0, x+w == self.width, y+h == self.height]
                fit_score += 5 * sum(walls)
                if sum(walls) == 0:
                    correctness = False
                flag, _ = self.access_to_ids(r, i, [-1]) # Access to colored open space
                if flag: 
                    fit_score += 3
                else:
                    correctness = False
                flag, neig_work = self.access_to_ids(r, i, self.workpl_ids) # Next to other workplaces
                if flag:
                    fit_score += neig_work
                else:
                    correctness = False
            else: # meeting rooms
                flag, _ = self.access_to_ids(r, i, [-1]) # Access to open space
                if flag: 
                    fit_score += 3
                else:
                    correctness = False
                flag, neig_work = self.access_to_ids(r, i, self.meet_ids) # Next to other workplaces
                if flag:
                    fit_score += neig_work * 2
                else:
                    correctness = False
        
        # computation demanding part only if previous are correct
        if correctness:
            # color accessible open space from door
            self.color_open_space(self.layout, self.width, self.height)

            # for every room check acces to open space
            for i, r in enumerate(self.rooms):
                flag, _ = self.access_to_ids(r, i, [99])
                if not flag:
                    correctness = False
                    break

            # decolor open
            for i in range(self.width):
                for j in range(self.height):
                    if self.layout[i][j] == 99:
                        self.layout[i][j] = -1

        return fit_score, correctness

    def access_to_ids(self, room, roomId, ids):
        # ids is list of number for which we search connection
        # returns (flag, count of access to different rooms/types)
        r = room
        flag = False
        access_cnt = 0
        accessed_floors = [roomId]
        # wrapper around object
        x, y, w, h = (max(0, r.x-1), max(0, r.y-1), 
                     min(r.x+r.width+2, self.width), 
                     min(r.y+r.height+2, self.height))
        for x_coord in range(x, w):
            for y_coord in range(y, h):
                field = self.layout[x_coord][y_coord] # ACTUAL SHOULD BE AT 0 index
                if field in ids and field not in accessed_floors:
                    if self.is_it_corner(x_coord, y_coord, x, y, r.width, r.height):
                        continue # It is corner touch do not count that
                    flag = True # Just one is enough :D
                    access_cnt += 1
                    accessed_floors.append(field)
        return flag, access_cnt

    def is_it_corner(self, x_c, y_c, x, y, w, h):
        if x_c == x-1 and y_c == y-1:
            return True # Left top corner
        if x_c == x-1 and y_c == y+h+1:
            return True # Right top corner
        if x_c == x+w+1 and y_c == y-1:
            return True # Left bottom corner
        if x_c == x+w+1 and y_c == y+h+1:
            return True # Right bottom corner
        return False

    def print_layout(self, fl):
        print("Layout floor .... ")
        for i in range(fl.width):
            for j in range(fl.height):
                print('%-2i' % fl.layout[i][j], end="")
            print()

    def color_open_space(self, ar, w, h):
        C = 99

        visited = [] # List for visited nodes.
        queue = []     #Initialize a queue

        def bfs(ar, node, w, h): #function for BFS
            visited.append(node)
            queue.append(node)

            while queue:          # Creating loop to visit each node
                x, y = queue.pop(0)
                if ar[x][y] == -1:
                    ar[x][y] = C

                for n in [(x-1,y), (x+1, y), (x, y-1), (x, y+1)]:
                    if n not in visited:
                        if n[0] < w and n[0] >= 0 and n[1] < h and n[1] >= 0:
                            if ar[n[0]][n[1]] == -1:
                                visited.append(n)
                                queue.append(n)
                    

        if ar[0][0] == -1:
            bfs(ar, (0,0), w, h)
            return
        if ar[0][h-1] == -1:
            bfs(ar, (0,h-1), w, h)
            return
        if ar[w-1][0] == -1:
            bfs(ar, (w-1,0), w, h)
            return
        if ar[w-1][h-1] == -1:
            bfs(ar, (w-1,h-1), w, h)
            return


