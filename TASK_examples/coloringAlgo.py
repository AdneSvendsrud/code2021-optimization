



ar = [ [2,2,2,2,2,-1,-1,-1,-1,-1],
        [2,2,2,2,2,-1,-1,-1,-1,-1],
        [2,2,2,2,2,-1,-1,-1,-1,-1],
        [3,3,3,3,3,-1,-1,-1,-1,-1],
        [3,3,3,3,3,-1,4,4,-1,-1],
        [3,3,3,3,3,-1,4,4,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]


neg_ar = [ [2,2,2,2,2,-1,-1,-1,-1,-1],
        [2,2,2,2,2,-1,-1,-1,-1,-1],
        [2,2,2,2,2,-1,-1,-1,-1,-1],
        [3,3,3,3,3,-1,-1,-1,-1,-1],
        [3,3,3,3,3,-1,4,4,-1,-1],
        [3,3,3,3,3,-1,4,4,-1,-1],
        [-1,-1,5,5,-1,-1,-1,-1,-1,-1],
        [6,6,5,5,-1,-1,-1,-1,-1,-1],
        [6,6,5,5,-1,-1,-1,-1,-1,-1]]

# w h mene jedna
def color_open_space(ar, w, h):
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

def print_layout(ar, x, y):
        print("Layout .... ")
        for i in range(x):
            for j in range(y):
                if ar[i][j] == -1:
                    print("- ", end="")    
                elif ar[i][j] == 99:
                    print("# ", end="")
                else:
                    print('%-2i' % ar[i][j], end="")
            print()

color_open_space(neg_ar, len(ar), len(ar[0]))
print_layout(neg_ar, len(ar), len(ar[0]))