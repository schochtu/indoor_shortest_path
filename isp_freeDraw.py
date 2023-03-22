import math
import pylint
import numpy as np

import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib.widgets import Slider, Button, RadioButtons


###############


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
    grid.g[start.x][start.y].fScore = heuristic(
        start.x, start.y, goal.x, goal.y)

    while not (len(openSet) == 0):
        min_f = min(x.fScore for x in openSet)
        current = next((x for x in openSet if x.fScore == min_f), None)
        # print(current.get_node())

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
                n[0].fScore = n[0].gScore + \
                    heuristic(goal.x, goal.y, n[0].x, n[0].y)
                if n[0] not in openSet:
                    openSet.append(n[0])

    return "This path cannot be traversed. Wow, much sad, so shame, very nope. "

###############

# def clamp(n, smallest, largest):
#    return max(smallest, min(n, largest))


def hor_search(start, goal, grid, hor_dir, dist):
    horSet = []
    while True:
        x1 = start.x + hor_dir
        if not (grid.in_bounds(x1, start.y)):
            return horSet  # Off grid - done

        if (grid.is_wall(grid.g[x1][start.y])):
            return horSet  # Is wall - done

        if ((x1 == goal.x) and (start.y == goal.y)):
            grid.g[x1][start.y].gScore = dist + 1
            horSet.append(grid.g[x1][start.y])
            return horSet

        # otherwise node must be open space
        dist = dist + 1
        x2 = x1 + hor_dir

        if (grid.is_wall(grid.g[x1][start.y-1])) and not (grid.is_wall(grid.g[x2][start.y-1])):
            grid.g[x1][start.y].gScore = dist
            grid.g[x1][start.y].fScore = grid.g[x1][start.y].gScore + \
                heuristic(goal.x, goal.y,
                          grid.g[x1][start.y].x, grid.g[x1][start.y].y)
            grid.g[x2][start.y-1].cameFrom(grid.g[x1][start.y])
            horSet.append(grid.g[x1][start.y])
            horSet.append(grid.g[x2][start.y-1])

        if (grid.is_wall(grid.g[x1][start.y+1])) and not (grid.is_wall(grid.g[x2][start.y+1])):
            grid.g[x1][start.y].gScore = dist
            grid.g[x1][start.y].fScore = grid.g[x1][start.y].gScore + \
                heuristic(goal.x, goal.y,
                          grid.g[x1][start.y].x, grid.g[x1][start.y].y)
            grid.g[x2][start.y+1].cameFrom(grid.g[x1][start.y])
            horSet.append(grid.g[x1][start.y])
            horSet.append(grid.g[x2][start.y+1])

        if len(horSet) > 0:
            horSet.append(horSet.append(grid.g[x1][start.y]))

        return horSet
#
#    if len(nodes) > 0:
#      nodes.append(self.add_node(x1, y0, (hor_dir, 0), dist))
#
#    return nodes # Process next tile. x0 = x1

# def search_hor(self, pos, hor_dir, dist):
#  """ Search in horizontal direction, return the newly added open nodes
#  @param pos: Start position of the horizontal scan.
#  @param hor_dir: Horizontal direction (+1 or -1).
#  @param dist: Distance traveled so far.
#  @return: New jump point nodes (which need a parent). """
#
#  x0, y0 = pos
#
#  while True:
#    x1 = x0 + hor_dir
#    if not self.on_map(x1, y0):
#      return []
#
#    # Off-map, done.
#    g = grid[x1][y0]
#    if g == OBSTACLE: return []
#
#    # Done.
#    if (x1, y0) == self.dest:
#      return [self.add_node(x1, y0, None, dist + HORVERT_COST)]
#
#    # Open space at (x1, y0).
#    dist = dist + HORVERT_COST
#    x2 = x1 + hor_dir
#    nodes = []
#
#    if self.obstacle(x1, y0 - 1) and not self.obstacle(x2, y0 - 1):
#      nodes.append(self.add_node(x1, y0, (hor_dir, -1), dist))
#
#    if self.obstacle(x1, y0 + 1) and not self.obstacle(x2, y0 + 1):
#      nodes.append(self.add_node(x1, y0, (hor_dir, 1), dist))
#
#    if len(nodes) > 0:
#      nodes.append(self.add_node(x1, y0, (hor_dir, 0), dist))
#
#    return nodes # Process next tile. x0 = x1

##############################


def jump_point_search(start, goal, grid, heuristic):
    openSet = []
    openSet.append(start)

    grid.g[start.x][start.y].gScore = 0
    grid.g[start.x][start.y].fScore = heuristic(
        start.x, start.y, goal.x, goal.y)

    return start

###############

# functions for GUI


def Onclick(event):

    global ix, iy
    ix, iy = event.xdata, event.ydata

    i = math.floor(event.ydata)
    j = math.floor(event.xdata)
    ax.scatter(int(event.xdata) + 0.5, int(event.ydata) +
               0.5, s=50, marker="s", color='black')
    fig.canvas.draw()

    global grid_coords
    grid_coords.append((int(i)))
    grid_coords.append((int(j)))

    return grid_coords


def startEndClick(event):

    global ix, iy
    ix, iy = event.xdata, event.ydata

    i = math.floor(event.ydata)
    j = math.floor(event.xdata)

    ax.scatter(int(event.xdata) + 0.5, int(event.ydata) +
               0.5, s=50, marker="s", color='blue')
    fig.canvas.draw()

    global coords
    coords.append((int(i)))
    coords.append((int(j)))

    return coords


def calc_astar(event):
    result = a_star_search(
        grid.g[coords[0]][coords[1]], grid.g[coords[2]][coords[3]], grid, heuristic)
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
    im = ax.pcolor(img[::1], cmap=cmap, edgecolors='k', linewidths=1)

    ax.scatter(coords[1] + 0.5, coords[0] + 0.5, s=50, marker="s")
    ax.scatter(coords[3] + 0.5, coords[2] + 0.5, s=50, marker="s")

    ax.xaxis.set(ticks=np.arange(0.5, len(wlabels)), ticklabels=wlabels)
    ax.yaxis.set(ticks=np.arange(0.5, len(hlabels)), ticklabels=hlabels)
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    fig.canvas.draw()

    for i in range(1, len(path)-1):
        grid.g[path[i][0]][path[i][1]].val = 0


def reset(event):
    # for x in range(len(coords)):
    coords.clear()
    init()
    fig.canvas.mpl_connect('button_press_event', Onclick)
    # print(len(coords))
    # if len(coords) == 4:
    # fig.canvas.mpl_disconnect(did)


def init():
    grid = Grid(50, 100)
    img = [[0]*len(grid.g[0]) for n in range(len(grid.g))]
    for x in range(len(grid.g)):
        for y in range(len(grid.g[0])):
            img[x][y] = grid.g[x][y].val

    cmap = colors.ListedColormap(['white', 'black'])
    im = ax.pcolor(img[::1], cmap=cmap, edgecolors='k', linewidths=1)

    return grid


def setGrid(event):

    fig.canvas.mpl_disconnect(cid)

    for i in range(0, len(grid_coords), 2):
        grid.g[grid_coords[i]][grid_coords[i + 1]].val = 1

    img = [[0]*len(grid.g[0]) for n in range(len(grid.g))]
    for x in range(len(grid.g)):
        for y in range(len(grid.g[0])):
            img[x][y] = grid.g[x][y].val

    cmap = colors.ListedColormap(['white', 'black'])
    im = ax.pcolor(img[::1], cmap=cmap, edgecolors='k', linewidths=1)

    fig.canvas.mpl_connect('button_press_event', startEndClick)
###############


file = 'resources\\floor_plan_b.png'

fig, ax = plt.subplots()

#result = a_star_search(grid.g[2][1], grid.g[7][7], grid, heuristic)
# print(result)

#path = result[1]
#
# for i in range(1, len(path)-1):
#    grid.g[path[i][0]][path[i][1]].val = 4
#


# variables for GUI
grid_coords = []
coords = []
#path = []

cid = fig.canvas.mpl_connect('button_press_event', Onclick)
# Button for reset the whole thing
resetx = plt.axes([0.8, 0.025, 0.12, 0.04])
reset_button = Button(resetx, 'Reset', hovercolor='0.975')
reset_button.on_clicked(reset)

# Button for calculation of jump star algorithm
jumpstarx = plt.axes([0.62, 0.025, 0.12, 0.04])
jumpstar_button = Button(jumpstarx, 'Jump Star', hovercolor='0.975')
# path_button.on_clicked(PathImg)

# Button for calculation of a star algorithm
astarx = plt.axes([0.42, 0.025, 0.12, 0.04])
astar_button = Button(astarx, 'A Star', hovercolor='0.975')
astar_button.on_clicked(calc_astar)

# Button for setting drawn grid
setx = plt.axes([0.20, 0.025, 0.12, 0.04])
set_button = Button(setx, 'Set', hovercolor='0.975')
set_button.on_clicked(setGrid)

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

######### for linux suckers ########
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()  # press alt + F4 (or alt + tab)


plt.show()

########## TO DO  THOMAS ############################
#
# 1. image stuff in eine function packen                DONE
# 2. grid erstellung in eine function packen            DONE
# 3. integration der image sachen in hauptprogrammm     DONE
# 4. random Start und Endpunkt
# 5. path als pfeile plotten
#
#
