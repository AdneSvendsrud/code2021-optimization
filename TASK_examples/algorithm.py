from _typeshed import Self
from floor import Floor
from random import randint

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
            {"x": 100, "y": 0}, 
            {"x": 0, "y": 100}, 
            {"x": 100, "y": 100}],
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

    def __init__(self, floor_width, floor_height, test_obj=None):
        self.floors = []
        self.width = floor_width
        self.heigth = floor_height
        if test_obj != None:
            self.testobject = test_obj
        # self.testobject = self.createTestObject()
        if(not self.createFloors(N=20)):
            raise Exception('Floor is wrong')
    
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
    Geneteic algo
    '''
    def run(self, iter_cnt=100):
        for f in self.floors:
            self.cross_mutation_rooms(f, idx=list(range(len(f.rooms))))

        # TODO run evolution with fitness
        # fitness = floor.get_score()

    def cross_mutation_rooms(self, floor, idx):
        idx_to_relax = []
        for i, r in enumerate(floor.rooms):
            if i not in idx:
                continue
            x, y = randint(0, floor.width-r.width), randint(0, floor.height-r.height)
            overlap = floor.place_relax(i, x, y)
            if overlap > 0:
                idx_to_relax.append((i,x,y,overlap))
        
        # relax overlaping objects
        for i, x, y, s in idx_to_relax:
            relax = False
            prev_s = s
            while not relax:
                floor.restore_object(floor.rooms[i], x, y, i)
                moves = [(x-1, y),(x, y-1), (x, y+1), (x+1, y),
                         (x-1, y+1),(x-1, y-1), (x+1, y-1), (x+1, y+1)]
                scores = []
                for x_n, y_n in moves:
                    scores.append(floor.place_relax(i, x_n, y_n))
                min_idx = scores.index(min(scores))
                relax = (scores[min_idx] == 0) 
                x, y = moves[min_idx]

        floor.placing_done()    

    def mutate_room(self, fl, room, direction):
        # simply make move to some direction 
        pass
        # moves = [(x-1, y),(x, y-1), (x, y+1), (x+1, y),
        #         (x-1, y+1),(x-1, y-1), (x+1, y-1), (x+1, y+1)]
        # scores = []
        # for x_n, y_n in moves:
        #     scores.append(floor.place_relax(i, x_n, y_n))
        # min_idx = scores.index(min(scores))
        # relax = (scores[min_idx] == 0) 
        # x, y = moves[min_idx]

    def createFloors(self, N):
        for _ in range(N):
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
