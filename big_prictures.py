import math
import pylint
import numpy as np

import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib.widgets import Slider, Button, RadioButtons

from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.transform import resize
from skimage.morphology import erosion, dilation
from skimage.morphology import disk
###############


def genImage():
    image = io.imread(file)
    gray_img = rgb2gray(image) #create gray scale image
    if(file == 'resources/floor_plan_c' or file == 'resources/floor_plan_d' or file == 'resources/floor_plan_d' or file == 'resources/floor_plan_f'):
        selem = disk(2)
    else:
        selem = disk(0)
    res_img = dilation(gray_img, selem)  #dilation for eliminating writing
    #res_img = resize(dilated, (50, 100)) #resize image so it can be used as grid
    #res_img = dilated
    thresh = threshold_otsu(res_img)
    return thresh, res_img

def genGrid():
    thresh, res_img = genImage()
    grid = Grid(res_img.shape[0], res_img.shape[1])
    for i in range(res_img.shape[0]):
        for j in range(res_img.shape[1]):
            if(res_img[i, j] < thresh):
                grid.g[i][j].val = 1
            else:
                grid.g[i][j].val = 0
    
    img1 = [[0]*len(grid.g[0])  for n in range(len(grid.g))]
    for x in range(len(grid.g)):
        for y in range (len(grid.g[0])):
            img1[x][y] = grid.g[x][y].val

    return grid


###############

class Node:
    def __init__(self, x, y, val, gScore, fScore, cameFrom):
        self.x = x
        self.y = y
        self.val = val
        # bisherige Länge vom Startknoten aus
        self.gScore = gScore
        # gScore + geschätzte Länge zum Zielknoten (Heuristik)
        self.fScore = fScore
        # parent node
        self.cameFrom = cameFrom

    def get_node(self):
        return (self.x, self.y, self.val, self.gScore, self.fScore, self.cameFrom)


class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.g = [[0]*width for n in range(height)]

        for x in range(len(self.g)):
            for y in range(len(self.g[0])):
                self.g[x][y] = Node(x, y, 0, math.inf, math.inf, 0)

    def in_bounds(self, x, y):
        return (0 <= x < self.height and 0 <= y < self.width)

    def is_wall(self, node):
        return (node.val == 1)

    def neighbours(self, node):
        result = []  # Nachbarn werden gegen den Uhrzeigersinn abgesucht. Angefangen Links vom abgefragten Node
        no = 0.0
        nw = 0.0
        so = 0.0
        sw = 0.0
        if (self.in_bounds(node.x, node.y-1)):
            if not self.is_wall(self.g[node.x][node.y-1]):
                result.append((self.g[node.x][node.y-1], 1))
            else:
                nw += 0.5
                sw += 0.5
        if (self.in_bounds(node.x+1, node.y)):
            if not self.is_wall(self.g[node.x+1][node.y]):
                result.append((self.g[node.x+1][node.y], 1))
            else:
                so += 0.5
                sw += 0.5
        if (self.in_bounds(node.x, node.y+1)):
            if not self.is_wall(self.g[node.x][node.y+1]):
                result.append((self.g[node.x][node.y+1], 1))
            else:
                so += 0.5
                no += 0.5
        if (self.in_bounds(node.x-1, node.y)):
            if not self.is_wall(self.g[node.x-1][node.y]):
                result.append((self.g[node.x-1][node.y], 1))
            else:
                nw += 0.5
                no += 0.5

        if (self.in_bounds(node.x-1, node.y-1)):
            if not self.is_wall(self.g[node.x-1][node.y-1]):
                if nw != 1.0:
                    result.append((self.g[node.x-1][node.y-1], math.sqrt(2)))
        if (self.in_bounds(node.x+1, node.y-1)):
            if not self.is_wall(self.g[node.x+1][node.y-1]):
                if sw != 1.0:
                    result.append((self.g[node.x+1][node.y-1], math.sqrt(2)))
        if (self.in_bounds(node.x+1, node.y+1)):
            if not self.is_wall(self.g[node.x+1][node.y+1]):
                if so != 1.0:
                    result.append((self.g[node.x+1][node.y+1], math.sqrt(2)))
        if (self.in_bounds(node.x-1, node.y+1)):
            if not self.is_wall(self.g[node.x-1][node.y+1]):
                if no != 1.0:
                    result.append((self.g[node.x-1][node.y+1], math.sqrt(2)))
        return result

###############


def heuristic(ax, ay, bx, by):
    return abs(ax-bx) + abs(ay - by)

###############


def reconstruct_path(start, current):
    full_path = []
    while current.cameFrom != 0:
        full_path.insert(0, current)
        current = current.cameFrom
    full_path.insert(0, start)
    return full_path


def interpret_path(path):
    result = []
    for n in path:
        result.append((n.x, n.y))
    return result

###############


def a_star_search(start, goal, grid, heuristic):
    openSet = []
    openSet.append(start)

    grid.g[start.x][start.y].gScore = 0
    grid.g[start.x][start.y].fScore = heuristic(start.x, start.y, goal.x, goal.y)

    while not (len(openSet) == 0):
        min_f = min(x.fScore for x in openSet)
        current = next((x for x in openSet if x.fScore == min_f), None)
        #print(current.get_node())

        if ((current.x == goal.x) and (current.y == goal.y)):
            node_path = reconstruct_path(start, current)
            coord_path = interpret_path(node_path)
            return node_path, coord_path

        openSet.remove(current)
        # print(current.get_node())
        neigh = grid.neighbours(current)

        for n in neigh:
            tentative_gScore = current.gScore + n[1]
            if tentative_gScore < n[0].gScore:
                n[0].cameFrom = current
                n[0].gScore = tentative_gScore
                n[0].fScore = n[0].gScore + heuristic(goal.x, goal.y, n[0].x, n[0].y)
                if n[0] not in openSet:
                    openSet.append(n[0])

    return "This path cannot be traversed. Wow, much sad, so shame, very nope. "

##############################

def vert_search(start, goal, grid, vert_dir, dist, openSet):
    x0 = start.x
    leng = len(openSet)
    
    while True:
        x1 = x0 + vert_dir
        if not (grid.in_bounds(x1, start.y)):
            return [] #Off grid - done

        if (grid.is_wall(grid.g[x1][start.y])):
            return [] #Is wall - done

        if ((x1 == goal.x) and (start.y == goal.y)):
            grid.g[x1][start.y].cameFrom = grid.g[x0][start.y]
            grid.g[x1][start.y].gScore = dist + 1
            grid.g[x1][start.y].fScore = grid.g[x1][start.y].gScore + heuristic(goal.x, goal.y, grid.g[x1][start.y].x, grid.g[x1][start.y].y)
            return openSet.append(goal)

        #otherwise node must be open space
        
        dist = dist + 1
        x2 = x1 + vert_dir
        #vertSet = []
        
        if (grid.is_wall(grid.g[x1][start.y-1])) and not (grid.is_wall(grid.g[x2][start.y-1])):
            grid.g[x1][start.y].gScore = dist
            grid.g[x1][start.y].fScore = grid.g[x1][start.y].gScore + heuristic(goal.x, goal.y, grid.g[x1][start.y].x, grid.g[x1][start.y].y)
            grid.g[x2][start.y-1].cameFrom = grid.g[x1][start.y]
            openSet.append(grid.g[x2][start.y-1])

        if (grid.is_wall(grid.g[x1][start.y+1])) and not (grid.is_wall(grid.g[x2][start.y+1])):
            grid.g[x1][start.y].gScore = dist
            grid.g[x1][start.y].fScore = grid.g[x1][start.y].gScore + heuristic(goal.x, goal.y, grid.g[x1][start.y].x, grid.g[x1][start.y].y)
            grid.g[x2][start.y+1].cameFrom = grid.g[x1][start.y]
            openSet.append(grid.g[x2][start.y+1])

        if len(openSet) > leng:
            openSet.append(openSet.append(grid.g[x1][start.y]))
            return openSet

        grid.g[x1][start.y].gScore = dist
        grid.g[x1][start.y].fScore = grid.g[x1][start.y].gScore + heuristic(goal.x, goal.y, grid.g[x1][start.y].x, grid.g[x1][start.y].y)
        grid.g[x1][start.y].cameFrom = grid.g[x0][start.y]
        x0 = x1

##############################

def hor_search(start, goal, grid, hor_dir, dist, openSet):
    y0 = start.y
    leng = len(openSet)
    
    while True:
        y1 = y0 + hor_dir
        if not (grid.in_bounds(start.x, y1)):
            return [] #Off grid - done

        if (grid.is_wall(grid.g[start.x][y1])):
            return [] #Is wall - done

        if ((y1 == goal.y) and (start.x == goal.x)):
            grid.g[start.x][y1].cameFrom = grid.g[start.x][y0]
            grid.g[start.x][y1].gScore = dist + 1
            grid.g[start.x][y1].fScore = grid.g[start.x][y1].gScore + heuristic(goal.x, goal.y, grid.g[start.x][y1].x, grid.g[start.x][y1].y)
            return openSet.append(goal)

        #otherwise node must be open space
        dist = dist + 1
        y2 = y1 + hor_dir
        #horSet = []
        
        if (grid.is_wall(grid.g[start.x-1][y1])) and not (grid.is_wall(grid.g[start.x-1][y2])):
            grid.g[start.x][y1].gScore = dist
            grid.g[start.x][y1].fScore = grid.g[start.x][y1].gScore + heuristic(goal.x, goal.y, grid.g[start.x][y1].x, grid.g[start.x][y1].y)
            grid.g[start.x-1][y2].cameFrom = grid.g[start.x][y1]
            openSet.append(grid.g[start.x-1][y2])

        if (grid.is_wall(grid.g[start.x+1][y1])) and not (grid.is_wall(grid.g[start.x+1][y2])):
            grid.g[start.x][y1].gScore = dist
            grid.g[start.x][y1].fScore = grid.g[start.x][y1].gScore + heuristic(goal.x, goal.y, grid.g[start.x][y1].x, grid.g[start.x][y1].y)
            grid.g[start.x+1][y2].cameFrom = grid.g[start.x][y1]
            openSet.append(grid.g[start.x+1][y2])

        if len(openSet) > leng:
            openSet.append(openSet.append(grid.g[start.x][y1]))
            return openSet

        grid.g[start.x][y1].gScore = dist
        grid.g[start.x][y1].fScore = grid.g[start.x][y1].gScore + heuristic(goal.x, goal.y, grid.g[start.x][y1].x, grid.g[start.x][y1].y)
        grid.g[start.x][y1].cameFrom = grid.g[start.x][y0]
        y0 = y1

###############

def diag_search(start, goal, grid, hor_dir, vert_dir, dist, openSet):
    current = start
    leng = len(openSet)

    while True:
        x1 = current.x + vert_dir
        y1 = current.y + hor_dir

        if not (grid.in_bounds(start.x, y1)):
            return [] #Off grid - done

        if (grid.is_wall(grid.g[start.x][y1])):
            return [] #Is wall - done
        
        if ((y1 == goal.y) and (x1 == goal.x)):
            grid.g[x1][y1].cameFrom = grid.g[current.x][current.y]
            grid.g[x1][y1].gScore = dist + 1
            grid.g[x1][y1].fScore = grid.g[x1][y1].gScore
            return openSet.append(goal)

        #otherwise node must be open space
        dist = dist + np.sqrt(2)
        x2 = x1 + vert_dir
        y2 = y1 + hor_dir

        if (grid.is_wall(grid.g[x1][current.y])) and not (grid.is_wall(grid.g[x2][current.y])):
            grid.g[x1][y1].gScore = dist
            grid.g[x1][y1].fScore = grid.g[x1][y1].gScore + heuristic(goal.x, goal.y, grid.g[x1][y1].x, grid.g[x1][y1].y)
            # ??? grid.g[x1][y2].cameFrom = grid.g[start.x][y1]
            openSet.append(grid.g[x1][y1])
            hor_done = False
            vert_done = False

        if (grid.is_wall(grid.g[current.x][y1])) and not (grid.is_wall(grid.g[current.x][y2])):
            grid.g[x1][y1].gScore = dist
            grid.g[x1][y1].fScore = grid.g[x1][y1].gScore + heuristic(goal.x, goal.y, grid.g[x1][y1].x, grid.g[x1][y1].y)
            # ??? grid.g[x1][y2].cameFrom = grid.g[start.x][y1]
            openSet.append(grid.g[x1][y1])
            hor_done = False
            vert_done = False



###############

def jump_point_search(start, goal, grid, heuristic):
    openSet = []
    openSet.append(start)

    grid.g[start.x][start.y].gScore = 0
    grid.g[start.x][start.y].fScore = heuristic(start.x, start.y, goal.x, goal.y)
     
    while not (len(openSet) == 0):
        min_f = min(x.fScore for x in openSet)
        current = next((x for x in openSet if x.fScore == min_f), None)

        if ((current.x == goal.x) and (current.y == goal.y)):
            print('Found goal!')
            node_path = reconstruct_path(start, current)
            coord_path = interpret_path(node_path)
            return node_path, coord_path

        openSet.remove(current)
        temp = []
        temp = hor_search(current, goal, grid, -1, 0, openSet)
        if (temp):
            for n in temp:
                openSet.append(n)
        temp = hor_search(current, goal, grid, +1, 0, openSet)
        if (temp):
            for n in temp:
                openSet.append(n)
        temp = vert_search(current, goal, grid, -1, 0, openSet)
        if (temp):
            for n in temp:
                openSet.append(n)
        temp = vert_search(current, goal, grid, +1, 0, openSet)
        if (temp):
            for n in temp:
                openSet.append(n)
        print('OpenSet in loop')
        print(openSet)

    return "This path cannot be traversed. Wow, much sad, so shame, very nope. "

###############

# functions for GUI
def Onclick(event):

    global ix, iy
    ix, iy = event.xdata, event.ydata

    i = math.floor(event.ydata)
    j = math.floor(event.xdata)
   
    ax.scatter(int(event.xdata) + 0.5, int(event.ydata) + 0.5, s=50, marker="s")
    fig.canvas.draw()

    global coords
    coords.append((int(i)))
    coords.append((int(j)))

    if len(coords) == 4:
        fig.canvas.mpl_disconnect(cid)

    return coords

def calc_astar(event):
    print('penis')
    result = a_star_search(grid.g[coords[0]][coords[1]], grid.g[coords[2]][coords[3]], grid, heuristic)
    path = result[1]

    ax.clear()

    for i in range(1, len(path)-1):
        grid.g[path[i][0]][path[i][1]].val = 4

    img = [[0]*len(grid.g[0]) for n in range(len(grid.g))]
    for x in range(len(grid.g)):
        for y in range(len(grid.g[0])):
            img[x][y] = grid.g[x][y].val
    
    cmap = colors.ListedColormap(['white', 'black', 'blue', 'green', 'grey'])
    #fig, ax = plt.subplots()
    im = ax.pcolor(img[::1], cmap=cmap, edgecolors='k', linewidths=0)

    ax.scatter(coords[1] + 0.5, coords[0] + 0.5, s=50, marker="s")
    ax.scatter(coords[3] + 0.5, coords[2] + 0.5, s=50, marker="s")
    xcoords = [x[0] for x in path]
    ycoords = [x[1] for x in path]
    #print(xcoords)
    ax.scatter(ycoords, xcoords, s=5, marker="o")
    #ax.quiver(path[::], path[::], 1, 1, scale_units='inches', scale=5, headwidth=1, headlength=1, color='r', pivot='middle')

    ax.xaxis.set(ticks=np.arange(0.5, len(wlabels)), ticklabels=wlabels)
    ax.yaxis.set(ticks=np.arange(0.5, len(hlabels)), ticklabels=hlabels)
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    fig.canvas.draw()

    for i in range(1, len(path)-1):
        grid.g[path[i][0]][path[i][1]].val = 0

def calc_jpoint(event):
    print("calc_jpoint")
    result = jump_point_search(grid.g[coords[0]][coords[1]], grid.g[coords[2]][coords[3]], grid, heuristic)
    print("----- result -----")
    print(result)
    path = result[1]

    ax.clear()

    for i in range(1, len(path)-1):
        grid.g[path[i][0]][path[i][1]].val = 4

    img = [[0]*len(grid.g[0]) for n in range(len(grid.g))]
    for x in range(len(grid.g)):
        for y in range(len(grid.g[0])):
            img[x][y] = grid.g[x][y].val
    
    cmap = colors.ListedColormap(['white', 'black', 'blue', 'green', 'grey'])
    #fig, ax = plt.subplots()
    im = ax.pcolor(img[::1], cmap=cmap, edgecolors='k', linewidths=0)

    ax.scatter(coords[1] + 0.5, coords[0] + 0.5, s=50, marker="s")
    ax.scatter(coords[3] + 0.5, coords[2] + 0.5, s=50, marker="s")
    #xcoords = [x[0] for x in path]
    #ycoords = [x[1] for x in path]
    #print(xcoords)
    #ax.scatter(ycoords, xcoords, s=10, marker="o")
    #ax.quiver(path[::], path[::], 1, 1, scale_units='inches', scale=5, headwidth=1, headlength=1, color='r', pivot='middle')

    ax.xaxis.set(ticks=np.arange(0.5, len(wlabels)), ticklabels=wlabels)
    ax.yaxis.set(ticks=np.arange(0.5, len(hlabels)), ticklabels=hlabels)
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    fig.canvas.draw()

    for i in range(1, len(path)-1):
        grid.g[path[i][0]][path[i][1]].val = 0

def reset(event):
    #for x in range(len(coords)):
    coords.clear()
    init()
    did = fig.canvas.mpl_connect('button_press_event', Onclick)
    #print(len(coords))
    #if len(coords) == 4:
        #fig.canvas.mpl_disconnect(did)


def init():    
    grid = genGrid()
    img = [[0]*len(grid.g[0]) for n in range(len(grid.g))]
    for x in range(len(grid.g)):
        for y in range(len(grid.g[0])):
            img[x][y] = grid.g[x][y].val

    #h = grid.height
    #w = grid.width
    #hlabels = range(0, h)
    #wlabels = range(0, w)
    #print(len(grid.g))

    cmap = colors.ListedColormap(['white', 'black'])
    im = ax.pcolor(img[::1], cmap=cmap, edgecolors='k', linewidths=0)


    return grid
###############

file = 'resources/floor_plan_i.png'
#file = 'resources/cat.png'
#file = 'resources/maze_d.png'
fig, ax = plt.subplots()

#result = a_star_search(grid.g[2][1], grid.g[7][7], grid, heuristic)
#print(result)

#path = result[1]
#
#for i in range(1, len(path)-1):
#    grid.g[path[i][0]][path[i][1]].val = 4
#


# variables for GUI
coords = []
#path = []

cid = fig.canvas.mpl_connect('button_press_event', Onclick)
# Button for reset the whole thing 
resetx = plt.axes([0.8, 0.025, 0.12, 0.04])
reset_button = Button(resetx, 'Reset', hovercolor='0.975')
reset_button.on_clicked(reset)

# Button for calculation of jump star algorithm
jumppointx = plt.axes([0.62, 0.025, 0.12, 0.04])
jumppoint_button = Button(jumppointx, 'Jump Star', hovercolor='0.975')
jumppoint_button.on_clicked(calc_jpoint)

# Button for calculation of a star algorithm
astarx = plt.axes([0.42, 0.025, 0.12, 0.04])
astar_button = Button(astarx, 'A Star', hovercolor='0.975')
astar_button.on_clicked(calc_astar)

grid = init()
h = grid.height
w = grid.width
hlabels = range(0, h)
wlabels = range(0, w)

ax.xaxis.set(ticks=np.arange(0.5, len(wlabels)), ticklabels=wlabels)
ax.yaxis.set(ticks=np.arange(0.5, len(hlabels)), ticklabels=hlabels)
ax.xaxis.tick_top()
ax.invert_yaxis()

######### for good people ##########
wm = plt.get_current_fig_manager()
wm.window.state('zoomed')

######### For the cool Linux users ########
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()  # press alt + F4 (or alt + tab)


plt.show()
