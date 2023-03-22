#import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
#from matplotlib import colors
#import math
#import pylint
#
#from skimage import io
#from skimage.color import rgb2gray
#from skimage.filters import threshold_otsu
#from skimage.transform import resize
#from skimage.morphology import erosion, dilation
#from skimage.morphology import disk
#
#class Node:
#    def __init__(self, x, y, val, gScore, fScore, cameFrom):
#        self.x = x
#        self.y = y
#        self.val = val
#        self.gScore = gScore
#        self.fScore = fScore
#        self.cameFrom = cameFrom
#
#    def get_node(self):
#        return (self.x, self.y, self.val, self.gScore, self.fScore, self.cameFrom)
#
#
#class Grid:
#    def __init__(self, width, height):
#        self.width = width
#        self.height = height
#        self.g = [[0]*height for n in range(width)]
#
#        for x in range(len(self.g)):
#            for y in range(len(self.g[0])):
#                self.g[x][y] = Node(x, y, 0, math.inf, math.inf, 0)
#
#    def in_bounds(self, x, y):
#        return (0 <= x < self.width and 0 <= y < self.height)
#
#    def is_wall(self, node):
#        return (node.val == 1)
#
#    def neighbours(self, node):
#        result = []  # Nachbarn werden gegen den Uhrzeigersinn abgesucht. Angefangen Links vom abgefragten Node
#        if (self.in_bounds(node.x, node.y-1)):
#            if not self.is_wall(self.g[node.x][node.y-1]):
#                result.append(self.g[node.x][node.y-1])
#        if (self.in_bounds(node.x+1, node.y)):
#            if not self.is_wall(self.g[node.x+1][node.y]):
#                result.append(self.g[node.x+1][node.y])
#        if (self.in_bounds(node.x, node.y+1)):
#            if not self.is_wall(self.g[node.x][node.y+1]):
#                result.append(self.g[node.x][node.y+1])
#        if (self.in_bounds(node.x-1, node.y)):
#            if not self.is_wall(self.g[node.x-1][node.y]):
#                result.append(self.g[node.x-1][node.y])
#        return result
#
#################
#
#def genImage(file):
#    image = io.imread(file)
#    gray_img = rgb2gray(image) #create gray scale image
#    selem = disk(0)
#    dilated = dilation(gray_img, selem)  #dilation for eliminating writing
#    res_img = resize(dilated, (50, 100)) #resize image so it can be used as grid
#    thresh = threshold_otsu(res_img)
#    return thresh, res_img
#
#def genGrid(file):
#    thresh, res_img = genImage(file)
#    grid = Grid(res_img.shape[0], res_img.shape[1])
#    for i in range(res_img.shape[0]):
#        for j in range(res_img.shape[1]):
#            if(res_img[i, j] < thresh):
#                grid.g[i][j].val = 1
#            else:
#                grid.g[i][j].val = 0
#    
#    img1 = [[0]*len(grid.g[0])  for n in range(len(grid.g))]
#    for x in range(len(grid.g)):
#        for y in range (len(grid.g[0])):
#            img1[x][y] = grid.g[x][y].val
#
#    return grid
#
##img = io.imread('resources\\floor_plan_c.png')
##img_gray = rgb2gray(img)
##selem = disk(1)
##dilated = dilation(img_gray, selem)
##res_img = resize(dilated, (50, 100))
##
##thresh = threshold_otsu(res_img)
#
#grid = genGrid('resources\\floor_plan_c.png')
#
##grid = Grid(res_img.shape[0], res_img.shape[1])
##
##for i in range(res_img.shape[0]):
##    for j in range(res_img.shape[1]):
##        if(res_img[i, j] < thresh):
##            grid.g[i][j].val = 1
##            a = a +1
##        else:
##            grid.g[i][j].val = 0
##            b= b +1
##
##
#img1 = [[0]*len(grid.g[0])  for n in range(len(grid.g))]
#for x in range(len(grid.g)):
#    for y in range (len(grid.g[0])):
#        img1[x][y] = grid.g[x][y].val
#
#
#cmap = colors.ListedColormap(['white','black','blue','green'])
#plt.figure()
#plt.pcolor(img1[::-1],cmap=cmap,edgecolors='k', linewidths=1)
##plt.pcolor(grid.g[::-1].val,cmap=cmap,edgecolors='k', linewidths=3)
#wm = plt.get_current_fig_manager()
#wm.window.state('zoomed')
#plt.show()
#
######################## TEST STUFF #######################
##img = io.imread('resources\\floor_plan_c.png')
##img_gray = rgb2gray(img)
##selem = disk(1)
##eroded = dilation(img_gray, selem)
##res_img = resize(eroded, (50, 100))
##
##
##
###print(res_img.shape[0])
##
##io.imshow(res_img)
##io.show()
##
##
##thresh = threshold_otsu(res_img)
##binary = res_img > thresh 
##io.imshow(binary)
###plt.show()            #plt.show or io.show ... both works
##io.show()
#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

t = np.arange(0.0, 2.0, 0.01)
s0 = np.sin(2*np.pi*t)
s1 = np.sin(4*np.pi*t)
s2 = np.sin(8*np.pi*t)

fig, ax = plt.subplots()
l, = ax.plot(t, s0, lw=2, color='red')
plt.subplots_adjust(left=0.3)

axcolor = 'lightgoldenrodyellow'
rax = plt.axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('2 Hz', '4 Hz', '8 Hz'))


def hzfunc(label):
    hzdict = {'2 Hz': s0, '4 Hz': s1, '8 Hz': s2}
    ydata = hzdict[label]
    l.set_ydata(ydata)
    plt.draw()
radio.on_clicked(hzfunc)

rax = plt.axes([0.05, 0.4, 0.15, 0.15], facecolor=axcolor)
radio2 = RadioButtons(rax, ('red', 'blue', 'green'))


def colorfunc(label):
    l.set_color(label)
    plt.draw()
radio2.on_clicked(colorfunc)

rax = plt.axes([0.05, 0.1, 0.15, 0.15], facecolor=axcolor)
radio3 = RadioButtons(rax, ('-', '--', '-.', 'steps', ':'))


def stylefunc(label):
    l.set_linestyle(label)
    plt.draw()
radio3.on_clicked(stylefunc)

plt.show()