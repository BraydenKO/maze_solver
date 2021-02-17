import queue
from PIL import Image

image = Image.open("photos\path_finder_maze.png")
image = image.convert("RGB")

def imagemaze(maze,image):
    width, height = image.size
    pixel_values = list(image.getdata())

    for idx, pixel in enumerate(pixel_values):
        if pixel == (0,0,0): #Black Wall
            pixel_values[idx] = "#"
        elif pixel == (255,255,255): #White Walking Space
            pixel_values[idx] = "□"
        elif pixel == (255, 0, 0): #Red End Point
            pixel_values[idx] = "X"
        elif pixel == (0,0,255): #Blue Starting Point
            pixel_values[idx] = "O"
        else:
            print("Invalid pixel in image")
            print(f"Colored: {pixel}")
            print("Location: row = ", idx//width, " | col = ", idx%width)
            quit()

    for i in range(height):
        maze.append([])
        for j in range(width):
            maze[i].append(pixel_values[i*width+j])

    maze = addpadding(maze)
    return maze



#prints the maze in an easy to read format (includes padding)
def printmaze(maze):
    for row in maze:
        for col in row:
            print(col, end="  ")
        print("\n")

#Colors the solved path into the maze
#Uses findpos(maze,path) to find the position of each step in the path to color in
def addpath(maze, path):
    for i in range(1,len(path)):
        row = findpos(maze,path[0:i])[0]
        col = findpos(maze,path[0:i])[1]
        maze[row][col] = "■"
    return maze

def addpathtoimg(maze,path,image):
    pixels = image.load()

    for i in range(1,len(path)):
        row = findpos(maze,path[0:i])[0]
        col = findpos(maze,path[0:i])[1]
        pixels[col-1,row-1] = (0,255,0)


    

    image = image.resize((round(image.size[0]*15),round(image.size[1]*15)), Image.NONE)
    image.show()
        
#Adds padding to the maze in order to prevent the pathfinder from leaving the maze
def addpadding(maze):
    width = len(maze[0])
    maze.insert(0,["#"]*width)
    maze.insert(len(maze),["#"]*width)
    for row in maze:
        row.insert(0,"#")
        row.insert(width+1,"#")
    return maze

#Use this to hard-code in the maze (Walls are #, open spaces are □, start is O, and end is X)
def createmaze(maze):
    maze.append(["X","□","□","#","O"])
    maze.append(["□","#","□","□","□"])
    maze.append(["□","□","□","#","#"])
    maze.append(["□","#","□","□","#"])
    maze.append(["□","□","□","#","#"])
    maze = addpadding(maze)
    return maze

#Checks if the given path leads to the X, ending point.
#Uses findpos(maze,path) to check if the position's value is the end point
def stillsearching(maze,path):
    row = findpos(maze,path)[0]
    col = findpos(maze,path)[1]
    if maze[row][col] == "X":
        return False
    else:
        return True

#Checks if the given path is a possible path (it doesn't intersect walls)
def valid(maze,path):
    row = findpos(maze,path)[0]
    if row == False:
        return False
    else:
        return True

#Finds the end position of the given path.
def findpos(maze,path):
    row = 1
    col = maze[row].index("O")
    for direction in path:
        if direction == "U":
            row += -1
        elif direction == "R":
            col += 1
        elif direction == "D":
            row += 1
        elif direction == "L":
            col += -1

        #if any spot in the path intersects a wall, return False for both row and col
        if maze[row][col] == "#":
            return False, False

    return row, col 

maze=[]
nums = queue.Queue()
nums.put("")
path = ""
# maze = createmaze(maze)
maze = imagemaze(maze,image)
printmaze(maze)

count = 0

while stillsearching(maze,path):
    #If the path backtracks (which is never optimal)
    #Then discard this path and look at the next one
    #If no more paths are left (the maze is unsolvable)
    #Then end the loop
    if ("DU" in path) or ("LR" in path) or ("UD" in path) or ("RL" in path):
        path = nums.get()
        if nums.empty():
            break
        continue
    
    #For the given path, try out all of the next possible steps
    for i in ["U","R","D","L"]:
        put = path + i
        if valid(maze, put):
            nums.put(put)
    path = nums.get()


print(path)
maze = addpath(maze,path)
printmaze(maze)
addpathtoimg(maze,path,image)
