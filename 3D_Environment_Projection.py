"""



mouse movement -> START LINE 382 TO FIX POINTS RENDERING BEHIND YOU

fix points rendering so that lines partial render

mouse movement is broken
"""
# ___________________________________________________________________________________

import pygame as py
import numpy as np
import math

global nodes, nodesOriginal, sensativity

py.init()

# Caption
py.display.set_caption('Sick 3D Simulation')

# set up screen dimensions and origin
screen_Width = 1470
screen_Height = 892
size = (screen_Width, screen_Height)
screen = py.display.set_mode(size)

sensativity = 40  # out of 100 aim for

# Camera
camera_Position = [0, 0, -2000]
camera_Rotation = [0, 0, 0]
near_clipz = -500


# ____________________________________________________________________________________________________
# COORD CREATING FUNCTIONS
def makePrism(topRight, w, h, l):
    prismPoints = [
        topRight,
        [topRight[0] - w, topRight[1], topRight[2]],
        [topRight[0] - w, topRight[1] - h, topRight[2]],
        [topRight[0], topRight[1] - h, topRight[2]],
        [topRight[0], topRight[1], topRight[2] - l],
        [topRight[0] - w, topRight[1], topRight[2] - l],
        [topRight[0] - w, topRight[1] - h, topRight[2] - l],
        [topRight[0], topRight[1] - h, topRight[2] - l],
    ]
    return prismPoints


def makePolyPrism(base, h, direction):
    topBase = []
    for i in base:
        topBase.append(i)
    if direction == 'y':
        for i in range(len(base)):
            topBase.append([base[i][0], base[i][1] + h, base[i][2]])
    elif direction == 'z':
        for i in range(len(base)):
            topBase.append([base[i][0], base[i][1], base[i][2] + h])
    elif direction == 'x':
        for i in range(len(base)):
            topBase.append([base[i][0], base[i][1], base[i][2] + h])

    return (topBase)


# ____________________________________________________________________________________________________


# deadzone


# NODES AND SHAPES______________________________________________________________________________________
nodes = [
    [[50, 50, -150],  # 1
     [-50, 50, -150],
     [-50, -50, -150],
     [50, -50, -150],
     [50, 50, -250],
     [-50, 50, -250],
     [-50, -50, -250],
     [50, -50, -250]],

    [
        [1000, -200, 1000],  # 2
        [-1000, -200, 1000],
        [-1000, -200, -1000],
        [1000, -200, -1000],
        [1000, -300, 1000],
        [-1000, -300, 1000],
        [-1000, -300, -1000],
        [1000, -300, -1000]
    ],


    makePrism([800, -100, 800], 1600, 200, 1600),  # 3


    makePolyPrism(
        [[-300, -100, 300], [-450, -100, 0], [-300, -100, -300], [0, -100, -450], [300, -100, -300], [450, -100, 0],
         [300, -100, 300], [0, -100, 450]], 30, 'y'),  # 4


    [[0, 0, 0]],#the origin for the whole thing, so

    makePrism((1500,800,1500),200,1100,200),
    makePrism((1400,850,1400),100,50,100)
    # ****************************************** ORIGIN X, ORIGINY ORIGIN Z  ************************************
    # 5

]
nodesOriginal = nodes


colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'light_gray': (192, 192, 192),
    'dark_gray': (64, 64, 64),
    'sky': (124, 220, 249),
    'nitronGrey': (25, 25, 30)
}


# ________________________________________________________________________________________________________________


# ____________________________________________________________________________________________________

# Translate Coords to fit new centered origin
def trCoords(screenCoords):
    return (screenCoords[0] + (screen_Width / 2), screenCoords[1] + (screen_Height / 2))


# magnitude function
def mag(Coords):
    return math.sqrt(Coords[0] ** 2 + Coords[1] ** 2 + Coords[2] ** 2)


# Rotation Functions
def rotateX(Coords, angle, axis=[0, 0, 0]):
    translatedCoords = [points - axis for points, axis in zip(Coords, axis)]
    Ax = [
        [1, 0, 0],
        [0, math.cos(angle), -1 * math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ]

    # newCoords = [[],[],[]]
    # newCoords[0] = Coords[0] * Ax[0][0] + Coords[1] * Ax[0][1] + Coords[2] * Ax[0][2]
    # newCoords[1] = Coords[0] * Ax[1][0] + Coords[1] * Ax[1][1] + Coords[2] * Ax[1][2]
    # newCoords[2] = Coords[0] * Ax[2][0] + Coords[1] * Ax[2][1] + Coords[2] * Ax[2][2]
    newCoords = np.dot(Ax, translatedCoords)
    newCoords1 = [new + axis for new, axis in zip(newCoords, axis)]
    return (newCoords1)


def rotateY(Coords, angle, axis=[0, 0, 0]):
    translatedCoords = [points - axis for points, axis in zip(Coords, axis)]
    Ay = [
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-1 * math.sin(angle), 0, math.cos(angle)]
    ]

    # newCoords = [[],[],[]]
    # newCoords[0] = Coords[0]*Ay[0][0] + Coords[1]*Ay[0][1] + Coords[2]*Ay[0][2]
    # newCoords[1] = Coords[0]*Ay[1][0] + Coords[1]*Ay[1][1] + Coords[2]*Ay[1][2]
    # newCoords[2] = Coords[0]*Ay[2][0] + Coords[1]*Ay[2][1] + Coords[2]*Ay[2][2]
    newCoords = np.dot(Ay, translatedCoords)
    newCoords1 = [new + axis for new, axis in zip(newCoords, axis)]
    return (newCoords1)


def rotateZ(Coords, angle, axis=[0, 0, 0]):
    translatedCoords = [points - axis for points, axis in zip(Coords, axis)]
    Az = [
        [math.cos(angle), -1 * math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]

    # newCoords = [[],[],[]]
    # newCoords[0] = Coords[0]*Az[0][0] + Coords[1]*Az[0][1] + Coords[2]*Az[0][2]
    # newCoords[1] = Coords[0]*Az[1][0] + Coords[1]*Az[1][1] + Coords[2]*Az[1][2]
    # newCoords[2] = Coords[0]*Az[2][0] + Coords[1]*Az[2][1] + Coords[2]*Az[2][2]
    newCoords = np.dot(Az, translatedCoords)
    newCoords1 = [new + axis for new, axis in zip(newCoords, axis)]
    return (newCoords1)


def rotateShapeX(shapeNodes, angle):
    newShapeNodes = []
    for i in range(len(shapeNodes)):
        newShapeNodes.append(rotateX(shapeNodes[i], angle))

    return newShapeNodes


def rotateShapeY(shapeNodes, angle):
    newShapeNodes = []
    for i in range(len(shapeNodes)):
        newShapeNodes.append(rotateY(shapeNodes[i], angle))

    return newShapeNodes


def rotateShapeZ(shapeNodes, angle):
    newShapeNodes = []
    for i in range(len(shapeNodes)):
        newShapeNodes.append(rotateZ(shapeNodes[i], angle))

    return newShapeNodes


# Perspective Function:

# fov = 90
# aspect_ratio = screen_Width / screen_Height

# far_clip = 1000


Pz = 1


def Project(Coords):
    # R3 to R3
    Coords1 = [1 * (Coords[0] - camera_Position[0]), 1 * (Coords[1] - camera_Position[1]),
               1 * (Coords[2] - camera_Position[2])]
    for i in range(len(Coords1)):
        if (camera_Position[2] - Coords[2]) != 0:
            Coords1[i] *= ((camera_Position[2] - near_clipz) / (camera_Position[2] - Coords[2]))

    return Coords1


# Lines function
def drawLine3D(node1, node2, color, thickness):

    #MOUSE: DOING THIS SO THAT CAMERA ROTATION WILL HAPPEN TO YOUR CAMERA POINTS OBJECTIVE OF THE ANGLE YOU ARE LOOKING

    var = rotateX(node1, camera_Rotation[0], camera_Position)
    var1 = rotateY(var, camera_Rotation[1], camera_Position)
    projectedCoords1 = Project(var1)[0:2]

    var = rotateX(node2, camera_Rotation[0], camera_Position)
    var2 = rotateY(var, camera_Rotation[1], camera_Position)
    projectedCoords2 = Project(var2)[0:2]
    if (node1[2] > camera_Position[2]) & (node2[2] > camera_Position[2]):
        py.draw.line(screen, color, trCoords(projectedCoords1), trCoords(projectedCoords2), thickness)


# Drawing 3D Shapes:
def drawPolyPrism(nodeSet):
    for i in range(len(nodeSet)):
        # projectedCoords = Project(nodeSet[i])[0:2]
        if i < len(nodeSet) / 2 - 1:
            drawLine3D(nodeSet[i], nodeSet[i + 1], colors["white"], 2)

            # 4 lines not part of 2 squares
            drawLine3D(nodeSet[i], nodeSet[i + math.floor(len(nodeSet) / 2)], colors["white"], 2)
        elif (i == len(nodeSet) / 2 - 1):
            drawLine3D(nodeSet[i], nodeSet[0], colors["white"], 2)

            # 4 lines not part of 2 squares
            drawLine3D(nodeSet[i], nodeSet[i + math.floor(len(nodeSet) / 2)], colors["white"], 2)
        elif i < (len(nodeSet) - 1):  # & i > 3):
            drawLine3D(nodeSet[i], nodeSet[i + 1], colors["white"], 2)
        elif i == (len(nodeSet) - 1):
            drawLine3D(nodeSet[i], nodeSet[math.floor(len(nodeSet) / 2)], colors["white"], 2)


def drawPrism(nodeSet):
    for i in range(len(nodeSet)):

        # projectedCoords = Project(nodeSet[i])[0:2]
        if i < 3:
            drawLine3D(nodeSet[i], nodeSet[i + 1], colors["white"], 2)

            # 4 lines not part of 2 squares
            drawLine3D(nodeSet[i], nodeSet[i + 4], colors["white"], 2)
        elif (i == 3):
            drawLine3D(nodeSet[i], nodeSet[0], colors["white"], 2)

            # 4 lines not part of 2 squares
            drawLine3D(nodeSet[i], nodeSet[i + 4], colors["white"], 2)
        elif i < (len(nodeSet) - 1):  # & i > 3):
            drawLine3D(nodeSet[i], nodeSet[i + 1], colors["white"], 2)
        elif i == (len(nodeSet) - 1):
            drawLine3D(nodeSet[i], nodeSet[4], colors["white"], 2)


# TEXT


def writeText2D(words, Coords, color, size=15):
    x, y = Coords[0], Coords[1]
    font = py.font.Font('freesansbold.ttf', size)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render(words, True, color)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (trCoords([x, y]))
    screen.blit(text, textRect)


# ____________________________________________________________________________________________________


# Main Loop
#default set mouse to playable state:
py.event.set_grab(True)
py.mouse.set_visible(False)

#put mouse in middle
py.mouse.set_pos(0,0)
while True:
    # clear screen
    screen.fill(colors["nitronGrey"])

    # Words
    # writeText2D('wsg gang', (0,0), colors['green'])
    writeText2D(('Camera X: ' + str(camera_Position[0])), ((-screen_Width / 2 + 80), (-screen_Height / 2 + 25)),
                colors['green'], 15)
    writeText2D(('Camera Y: ' + str(camera_Position[1])), ((-screen_Width / 2 + 80), (-screen_Height / 2 + 45)),
                colors['green'], 15)
    writeText2D(('Camera Z: ' + str(camera_Position[2])), ((-screen_Width / 2 + 80), (-screen_Height / 2 + 65)),
                colors['green'], 15)
    writeText2D(('Sensativity: ' + str(sensativity)), ((-screen_Width / 2 + 80), (-screen_Height / 2 + 90)),
                colors['green'], 15)

    # nodes[3] = rotateShapeY(nodes[3],.01)

    # camera clip - this worked somehow
    near_clipz = camera_Position[2] - 500

    # MOUSE MOVEMENT
    #mouse_x, mouse_y = py.mouse.get_rel()

    # Update camera rotation based on mouse movement
    #camera_Rotation[0] += mouse_y * -0.0001 * sensativity
    #scamera_Rotation[1] += mouse_x * 0.0001 * sensativity

    # DRAWSHAPES:
    drawPrism(nodes[0])
    drawPrism(nodes[1])
    drawPrism(nodes[2])
    drawPrism(nodes[5])
    drawPrism(nodes[6])
    drawPolyPrism(nodes[3])

    # DRAWING NODES __ __  __ __  __ __  __ __  __ __  __ __  __ __##@#@#!@#!@#!@#(!@&^$(!&@#%$(!&@

    for t in range(len(nodes)):
        for i in range(len(nodes[t])):
            # MOUSE ROTATION

            #var = rotateX(nodes[t][i], camera_Rotation[0], camera_Position)
            #change = rotateY(var, camera_Rotation[1], camera_Position),

            #nodes[t][i] = rotateX(nodes[t][i], camera_Rotation[0], camera_Position)
            #nodes[t][i] = rotateY(nodes[t][i], camera_Rotation[1], camera_Position)

            # the problem here is that it is working, but doesn't work like minecraft/real world view mechanics.
            # ie when you are looking straight and turn right, you rotate around y, but when you ar elooking up and rotate, you rotate aorund that
            # same axis, but in this it would change to z axis because of how we set up rotation transformation

            # Perspective project
            #def cameraAdjust() ** START HERE
            var = rotateX(nodes[t][i], camera_Rotation[0], camera_Position)
            var1 = rotateY(var, camera_Rotation[1], camera_Position)

            projectedCoords = Project(var1)[0:2]
            if var1[2] > camera_Position[2]:
                #mouse in affect:

                # DRAWING NODES
                py.draw.circle(screen, colors['cyan'], trCoords(projectedCoords), 2)

                py.draw.circle(screen, colors['red'], trCoords(Project(nodes[4][0])[0:2]), 3)

    # _ __  __ __  __ __  __ __  __ __  __ __  __  __ __  __ __##@#@#!@#!@#!@#(!@&^$(!&@#%$(!&@

    # AUTOMATIC MOVEMENT

    # KEYBOARD INPUT
    keys = py.key.get_pressed()

    #player movement

    if keys[py.K_s]:
        # rotate clockwise x-axis
        for t in range(len(nodes)):
            for i in range(len(nodes[t])):
                nodes[t][i] = rotateX(nodes[t][i], .001, nodes[4][0])

    if keys[py.K_w]:
        # rotate clockwise x-axis
        for t in range(len(nodes)):
            for i in range(len(nodes[t])):
                nodes[t][i] = rotateX(nodes[t][i], -.001,nodes[4][0])

    if keys[py.K_a]:
        # rotate clockwise x-axis
        for t in range(len(nodes)):
            for i in range(len(nodes[t])):
                nodes[t][i] = rotateY(nodes[t][i], .001,nodes[4][0])

    if keys[py.K_d]:
        # rotate clockwise x-axis
        for t in range(len(nodes)):
            for i in range(len(nodes[t])):
                nodes[t][i] = rotateY(nodes[t][i], -.001,nodes[4][0])

    if keys[py.K_e]:
        # rotate clockwise x-axis
        for t in range(len(nodes)):
            for i in range(len(nodes[t])):
                nodes[t][i] = rotateZ(nodes[t][i], .001,nodes[4][0])

    if keys[py.K_q]:
        # rotate clockwise x-axis
        for t in range(len(nodes)):
            for i in range(len(nodes[t])):
                nodes[t][i] = rotateZ(nodes[t][i], -.001,nodes[4][0])

    if keys[py.K_p]:
        # rotate clockwise x-axis
        near_clipz += 2
        print(near_clipz)

    if keys[py.K_o]:
        # rotate clockwise x-axis
        near_clipz -= 2
        print(near_clipz)

    if keys[py.K_LEFT]:
        # rotate clockwise x-axis
        camera_Position[0] += 2

    if keys[py.K_RIGHT]:
        # rotate clockwise x-axis
        camera_Position[0] -= 2

    if keys[py.K_DOWN]:
        # rotate clockwise x-axis
        camera_Position[2] -= 2

    if keys[py.K_UP]:
        # rotate clockwise x-axis
        camera_Position[2] += 2

    if keys[py.K_SPACE]:
        # rotate clockwise x-axis
        camera_Position[1] += 2

    if keys[py.K_LSHIFT]:
        # rotate clockwise x-axis
        camera_Position[1] -= 2

        # esc mouse cursor
    if keys[py.K_ESCAPE]:
        # release cursor
        py.event.set_grab(False)
        py.mouse.set_visible(True)

    #this function is meant to reset everything, it doesn't work.
    if keys[py.K_k]:
        for t in range(len(nodes)):
            for i in range(len(nodes)):
                if t < len(nodesOriginal) & i < len(nodesOriginal[t]):
                    nodes[t][i] = nodesOriginal[t][i]
        print(nodes, nodesOriginal)




    for ev in py.event.get():
        #change cursor to control screen when clicked
        if ev.type == py.MOUSEBUTTONDOWN:
            # release cursor
            py.event.set_grab(True)
            py.mouse.set_visible(False)

        #og tutorial thing:
        if ev.type == py.MOUSEBUTTONUP:
            pos = py.mouse.get_pos()
            py.draw.circle(
                screen, colors['white'], pos, 20, 3
            )

    # UPDATE DISPLAY
    py.display.update()

    if py.event.get(py.QUIT):
        exit()
