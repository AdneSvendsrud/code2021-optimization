from math import floor
from floor import Floor
from random import randint, random, shuffle
import copy

'''
RULES:
No two rooms can exist in the same place (no overlapping rooms)

•Walls can overlap (one wall can be the right wall of one room, and the left wall of another. A wall
of a room can also be the wall of the floor itself)

•A room can have any arbitrary rotation

•If a room has windows, then they must be attached to a wall of the floor plan itself, i.e. they must
point outwards. A window cannot go inwards to the building.

•Rooms of the same type should be adjacent to each other

•workRoom should be adjacent to the boundary edges

•There should be circulation area connecting each room

'''

class Algorithm:

    testobject = {
        "planboundary": [
            {"x": 0, "y": 0}, 
            {"x": 50, "y": 0}, 
            {"x": 0, "y": 60}, 
            {"x": 50, "y": 60}],
        "rooms": [
            {"width": 10, 
            "height": 10, 
            "type": "workRoom"},
            {"width": 5, 
            "height": 5, 
            "type": "workRoom"},
            {"width": 10, 
            "height": 20, 
            "type": "meeting"},
            {"width": 15, 
            "height": 5, 
            "type": "workRoom"}]
    }
    testobject_3m_5r = {
        "planboundary": [
            {"x": 0, "y": 0}, 
            {"x": 50, "y": 0}, 
            {"x": 0, "y": 60}, 
            {"x": 50, "y": 60}],
        "rooms": [
            {"width": 10, 
            "height": 10, 
            "type": "workRoom"},
            {"width": 5, 
            "height": 5, 
            "type": "workRoom"},
            {"width": 5, 
            "height": 5, 
            "type": "workRoom"},
            {"width": 10, 
            "height": 20, 
            "type": "meeting"},
            {"width": 10, 
            "height": 10, 
            "type": "meeting"},
            {"width": 10, 
            "height": 10, 
            "type": "meeting"},
            {"width": 15, 
            "height": 5, 
            "type": "workRoom"}]
    }
    
    testobject2 = {
        "planboundary": [
            {"x": 0, "y": 0}, 
            {"x": 10, "y": 0}, 
            {"x": 0, "y": 15}, 
            {"x": 10, "y": 15}],
        "rooms": [
            {"width": 2, 
            "height": 2, 
            "type": "workRoom"},
            {"width": 3, 
            "height": 2, 
            "type": "workRoom"}]
    }

    def __init__(self, floor_width, floor_height, N=30, test_obj=None):
        self.floors = []
        self.width = floor_width
        self.heigth = floor_height
        if test_obj != None:
            self.testobject = test_obj
        else:
            self.testobject = self.testobject
        if(not self.createFloors(N=N)):
            raise Exception('Floor is wrong')
        self.population_N = N
    '''
    Naive approach
    '''
    def naive(self):
        '''
        # take middle
        x = self.floors.midx
        y = self.floors.midy

        # take every place and try if it is free
        for i in range():
            print("take every place and try if it is free")
            # I'm guessing a double for loop to iterate over the 2d array?


        # check if it is in grid
        if x + self.heigth > self.heigth:
            print("out of the grid")
            return
            
        if y + self.width > self.width:
            print("out of the grid")
            return

        # check if there is free space
        if self.floor.layout[x][y] != 0:
            print("change params x and y")

        # call place_rooms function
        self.floor.place_rooms(x, y)
        '''

        # place room on 0,0
        #  - check if is not out of grid: otherwise FALSE
        #  - fill the places
        # find new free top left corner
        # place another room
        #  - check if is not out of grid
        #     - if yes, go down
        #     
        #  - fill the places
        # check surrounding
        #  - 
        
        pass


    '''
    Genetetic algo
    '''
    def run(self, iter_cnt=100):
        for f in self.floors:
            print("Placing floor...")
            self.cross_mutation_rooms(f, idx=list(range(len(f.rooms))))
            f.store_init_state()
        print("Placing floor is done...")

        for iter_i in range(iter_cnt):

            print("="* 100)
            print("#" + "   Iteration  ", iter_i+1, flush=True)

            for fl in self.floors[1:]:
                
                rms = copy.deepcopy(fl.workpl_ids) 
                shuffle(rms)
                
                mts = copy.deepcopy(fl.meet_ids)
                shuffle(mts)
                
                # 6% rate of cross mutation 
                if random() < 0.02:
                    print("Cross fit mutation")
                    if random() < 0.5:
                        self.cross_mutation_rooms(fl, [rms[0]])
                    elif len(mts) > 0:
                        self.cross_mutation_rooms(fl, [mts[0]])

                # mutate all rooms
                for r_i in rms:
                    r = fl.rooms[r_i]
                    self.mutate_room(fl, r, randint(0,3), r_i) # DEBUG
                for m_i in mts:
                    r = fl.rooms[m_i]
                    self.mutate_room(fl, r, randint(0,3), m_i) # DEBUG

                # store state of layout to memory
                fl.store_state()

            # store state for the first floor too
            self.floors[0].store_state()

            # calculate fitness for all floors
            sorted_floors = sorted(self.floors, key=lambda x: x.fitness()[0], reverse=True)
            # print("FITNESSes : ", [x.fitness()[0] for x in self.floors])
            self.floors = sorted_floors

            # Control whether there is any optimal solution
            correctness = [x.fitness()[1] for x in self.floors]
            if sum(correctness) > 0:
                index = correctness.index(True)
                print("Correctness", correctness)
                self.print_layout(self.floors[index])
                return self.floors[index], True
            # self.print_layout(self.floors[0])
        # Maybe return something
        return self.floors[0], False

    def cross_mutation_rooms(self, floor, idx):
        idx_to_relax = []
        for i, r in enumerate(floor.rooms):
            if i not in idx:
                continue
            x_prev, y_prev = floor.rooms[i].x, floor.rooms[i].y
            if x_prev != -1 or y_prev != -1:
                # Dealocate object place before
                floor.restore_object(floor.rooms[i], x_prev, y_prev, i) 
            x, y = randint(0, floor.width-r.width-1), randint(0, floor.height-r.height-1)
            overlap = floor.place_relax(i, x, y)
            if overlap > 0:
                idx_to_relax.append((i,x,y,overlap))
                floor.restore_object(floor.rooms[i], x, y, i) 
            else:
                r.set_coords(x, y)
            
        # print('INDEXES FOR RELAXATION' , idx_to_relax)
        

        self.relax_room(floor, idx_to_relax)
        # self.mutate_room(floor, floor.rooms[1], 2, 1) # DEBUG 

    def relax_room(self, floor, idx_to_relax):
        # relax overlaping objects, [(room_i,x,y,overlap)]

        # print('TO RELAX', idx_to_relax)
        for i, x, y, s in idx_to_relax:
            relax = False
            prev_s = s
            cnt = 0
            while not relax:
                # self.print_layout(floor)
                # print(x, y)
                floor.restore_object(floor.rooms[i], x, y, i)
                # moves = [(x-1, y),(x, y-1), (x, y+1), (x+1, y),
                #          (x-1, y+1),(x-1, y-1), (x+1, y-1), (x+1, y+1)]

                # 8 direction move support
                # moves = [(max(x-1,0), y),(x, max(y-1,0)), 
                #         (x, min(y+1, floor.height)),
                #         (min(x+1, floor.width), y),
                #         (max(x-1,0), min(y+1, floor.height)),
                #         (max(x-1,0), max(y-1,0)), 
                #         (min(x+1,floor.width),max(y-1,0)), 
                #         (min(x+1,floor.width), min(y+1, floor.height))]

                moves = [(max(x-1,0), y),(x, max(y-1,0)),
                        (x, min(y+1, floor.height)),
                        (min(x+1, floor.width), y)]  
                shuffle(moves)
                scores = []
                # print("MOVES ", moves)
                for x_n, y_n in moves:
                    scores.append(floor.place_relax(i, x_n, y_n))
                    floor.restore_object(floor.rooms[i], x_n, y_n, i)
                
                cnt+=1
                
                min_idx = scores.index(min(scores))
                # simulating anneling
                if random() < 0.01:
                    self.cross_mutation_rooms(floor, [i])
                    return 
                relax = (scores[min_idx] == 0) 
                x, y = moves[min_idx]
                # print(min_idx, relax, x, y)
                # if cnt == 3:
                #     exit(0)
            # Finally place room
            floor.place_relax(i, x, y)
            floor.rooms[i].set_coords(x, y)
            # exit(0)

    def mutate_room(self, fl, room, direction, roomId):
        # simply make move to some direction
        x, y = room.x, room.y
        fl.restore_object(room, x, y, roomId)

        # 8 direction move
        # moves = [(max(x-1,0), y),(x, max(y-1,0)), (x, min(y+1, fl.height)),
        #          (min(x+1, fl.width), y),
        #         (max(x-1,0), min(y+1, fl.height)),
        #         (max(x-1,0), max(y-1,0)), (min(x+1,fl.width), max(y-1,0)), 
        #         (min(x+1,fl.width), min(y+1, fl.height))]


        moves = [(max(x-1,0), y),(x, max(y-1,0)), (x, min(y+1, fl.height)),
                 (min(x+1, fl.width), y)]            
                

        x_n, y_n = moves[direction]
        # print("MOVING TO {} {} from {} {}", x_n, y_n, x, y)         

        score = fl.place_relax(roomId, x_n, y_n)
        if score > 0:
            # fl.restore_object(room, x_n, y_n, roomId)
            self.relax_room(fl, [(roomId, x_n, y_n, score)])
        else:
            room.set_coords(x_n, y_n)

    def createFloors(self, N):
        self.population_N = N
        for i in range(N):
            print("Index of added floor is :  ", i)
            try:
                self.floors.append(Floor(self.testobject["planboundary"][3]["x"], self.testobject["planboundary"][3]["y"], self.testobject))
            except Exception as error:
                print(error)
                return False
        return True
    
    def createTestObject():
        # WARNING: NOT GUARANTEED TO WORK!!!!
        rand_x = randint(10, 1000)
        rand_y = randint(10, 1000)
        return {
        "planboundary": [
            {"x": 0, "y": 0}, 
            {"x": rand_x, "y": 0}, 
            {"x": 0, "y": rand_y}, 
            {"x": rand_x, "y": rand_y}],
        "rooms": [
            {"width": randint(5, 20), "height": randint(5, 20)} for _ in range(randint(1, 15))
            ]
    }

    def print_layout(self, fl):
        print("Layout .... ")
        for i in range(fl.width):
            for j in range(fl.height):
                if fl.layout[i][j] == -1:
                    print("- ", end="")    
                else:
                    print('%-2i' % fl.layout[i][j], end="")
            print()
