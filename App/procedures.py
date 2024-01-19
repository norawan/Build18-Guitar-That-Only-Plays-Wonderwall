import pygame
from constants import *

ORB_START_X = None
MS_WIDTH = None

def makeImage(file_path):
    # Load the image
    image = pygame.image.load(file_path)

    # Convert
    if (".png" in file_path):
        image.convert_alpha()
    else:
        image.convert()

    # return a tuple with the surface and its rect
    return image

def mouseInButton(button : pygame.Rect, mouseX, mouseY):
    return mouseX >= button.left and mouseX <= button.right \
        and mouseY >= button.top and mouseY <= button.bottom

def mouseInPauseButton(pauseLeft : pygame.Rect, pauseRight : pygame.Rect, mouseX, mouseY):
    fullButton = pauseLeft.union(pauseRight)
    return mouseInButton(fullButton, mouseX, mouseY)

def mouseInSeekButton(triangleCoordinates : tuple, bar : pygame.Rect, mouseX, mouseY):
    return mouseInButton(bar, mouseX, mouseY) or mouseInTriangle(triangleCoordinates, mouseX, mouseY)

def mouseInCircle(circlePos, radius, mouseX, mouseY):
    (circleX, circleY) = circlePos
    distSq = ((circleX - mouseX) ** 2) + ((circleY - mouseY) ** 2)
    return (distSq <= (radius ** 2))

# triHelper derived from https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle
def triHelper(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

# help for mouseInTriangle from https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle
def mouseInTriangle(coordinates : tuple, mouseX, mouseY):
    point = (mouseX, mouseY)
    (p1, p2, p3) = coordinates

    d1 = triHelper(point, p1, p2)
    d2 = triHelper(point, p2, p3)
    d3 = triHelper(point, p3, p1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def makeTriangle(centerCoordinate : tuple, base, height, direction):
    x_center, y_center = centerCoordinate
    half_base = base // 2
    half_height = height // 2
    if direction == "up":
        x1 = x_center
        y1 = y_center - half_height
        x2 = x_center - half_base
        y2 = y_center + half_height
        x3 = x_center + half_base
        y3 = y_center + half_height
    elif direction == "down":
        x1 = x_center
        y1 = y_center + half_height
        x2 = x_center - half_base
        y2 = y_center - half_height
        x3 = x_center + half_base
        y3 = y_center - half_height
    elif direction == "left":
        x1 = x_center - half_base
        y1 = y_center
        x2 = x_center + half_base
        y2 = y_center - half_height
        x3 = x_center + half_base
        y3 = y_center + half_height
    else:
        x1 = x_center + half_base
        y1 = y_center
        x2 = x_center - half_base
        y2 = y_center - half_height
        x3 = x_center - half_base
        y3 = y_center + half_height
    return ((x1, y1), (x2, y2), (x3, y3))

def updateCurrentMeasure(userHasOrb, oldMeasure, oldOffset, oldTimePlayed, numMeasures, measureDuration_ns, mouseX):
    if not userHasOrb:
        return oldMeasure, oldOffset, oldTimePlayed, False
    elif mouseX < (ORB_START_X): # past left bound of slider
        return 0, 0, 0, True
    elif mouseX > (ORB_START_X + MS_WIDTH): # past right bound of slider
        return numMeasures, 0, numMeasures * measureDuration_ns, True
    else: # jumping to specific location on slider
        startDist = ORB_START_X
        jumpFactor = (mouseX - startDist) / MS_WIDTH
        roundedMeasure = round(jumpFactor * numMeasures)
        if DEBUG : print("Changing measure to {}".format(roundedMeasure))
        return roundedMeasure, 0, roundedMeasure * measureDuration_ns, True

def orbOnScreen(screen : pygame.Surface, orbPos):
    posX = orbPos[0] * screen.get_width() // FIGMA_SCREEN_WIDTH
    posY = orbPos[1] * screen.get_height() // FIGMA_SCREEN_HEIGHT
    return (posX, posY)

# assumes orb will be moved to curMeasure
def updateMeasureOrb(offset, curMeasure, numMeasures, oldOrbPos):
    (_, oldOrbY) = oldOrbPos

    if numMeasures == 0: # no song
        return (ORB_START_X, oldOrbY)
    else:
        if (offset == None):
            offset = 0
        movement = MS_WIDTH * ((curMeasure + offset) / numMeasures)
        newX = int(ORB_START_X + movement)
        return (newX, oldOrbY)
    
def createObjects(appScreen : pygame.Surface,  orbPos: list):
    objects = []

    x_center = appScreen.get_width() // 2
    y_center = appScreen.get_height() // 2
    centerPoint = pygame.Rect(x_center, y_center, 0, 0)

    guitarWidth = (GUITAR_IMG_WIDTH * GUITAR_IMG_SCALE_FACTOR) * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    guitarHeight = (GUITAR_IMG_HEIGHT * GUITAR_IMG_SCALE_FACTOR) * appScreen.get_height() // FIGMA_SCREEN_HEIGHT

    titleWidth = TITLE_WIDTH * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    titleHeight = TITLE_HEIGHT * appScreen.get_height() // FIGMA_SCREEN_HEIGHT
    titleLeft = (x_center - (titleWidth // 2))
    titleTop = y_center - (guitarHeight // 2) - (TITLE_Y_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)

    # Title Text
    fontSize = TITLE_FONT_SIZE * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    titleFont = pygame.font.SysFont("Comic Sans", fontSize, bold=False)
    titleText = titleFont.render("Anyway, here's Wonderwall.", True, WHITE, BLACK)
    titleRect = pygame.Rect(titleLeft, titleTop, titleWidth, titleHeight)
    titleTextRect = titleText.get_rect()
    titleTextRect.center = titleRect.center

    # Image
    guitarSurface = makeImage("App/images/ScumbagGuitarPlayer.png")
    guitarSurface = pygame.transform.scale(guitarSurface, (guitarWidth, guitarHeight))
    guitarRect = guitarSurface.get_rect()
    guitarRect.center = centerPoint.center
    guitarRect.centery -= (GUITAR_IMG_Y_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)

    # Play button
    playBase = PLAY_SIZE * appScreen.get_height() // FIGMA_SCREEN_HEIGHT
    playHeight = playBase
    playX = x_center
    playY = y_center + (guitarHeight // 2) + (PLAY_BUTTON_Y_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)
    playCoordinates = makeTriangle((playX, playY), playBase, playHeight, "right")

    # Pause button
    pauseWidth = (PLAY_SIZE * appScreen.get_width() // FIGMA_SCREEN_WIDTH) // 3
    pauseHeight = playHeight
    pauseBar1Left = playX - pauseWidth - (pauseWidth // 2)
    pauseBar1tTop = playY - (pauseHeight // 2)
    pauseBar2Left =  playX + pauseWidth  - (pauseWidth // 2)
    pauseBar2Top = pauseBar1tTop
    pauseLeftBarRect = pygame.Rect(pauseBar1Left, pauseBar1tTop, pauseWidth, pauseHeight)
    pauseRightBarRect = pygame.Rect(pauseBar2Left, pauseBar2Top, pauseWidth, pauseHeight)

    # Backtrack button
    backBase = PLAY_SIZE * appScreen.get_height() // FIGMA_SCREEN_HEIGHT
    backHeight = playBase
    backX = x_center - BACK_BUTTON_X_OFFSET * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    backY = y_center + (guitarHeight // 2) + (PLAY_BUTTON_Y_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)
    backCoordinates = makeTriangle((backX, backY), backBase, backHeight, "left")
    backBarWidth = (PLAY_SIZE * appScreen.get_width() // FIGMA_SCREEN_WIDTH) // 3
    backBarHeight = backHeight 
    backBarLeft = backX - (backHeight // 2)
    backBarTop = backY - (backBarHeight // 2)
    backBarRect = pygame.Rect(backBarLeft, backBarTop, backBarWidth, backBarHeight)

    # Forward button
    forwardBase = PLAY_SIZE * appScreen.get_height() // FIGMA_SCREEN_HEIGHT
    forwardHeight = playBase
    forwardX = x_center + FORWARD_BUTTON_X_OFFSET * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    forwardY = y_center + (guitarHeight // 2) + (PLAY_BUTTON_Y_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)
    forwardCoordinates = makeTriangle((forwardX, forwardY), forwardBase, forwardHeight, "right")
    forwardBarWidth = (PLAY_SIZE * appScreen.get_width() // FIGMA_SCREEN_WIDTH) // 3
    forwardBarHeight = forwardHeight 
    forwardBarLeft = forwardX + (forwardHeight // 2)
    forwardBarTop = forwardY - (forwardBarHeight // 2)
    forwardBarRect = pygame.Rect(forwardBarLeft, forwardBarTop, forwardBarWidth, forwardBarHeight)

    # Measure slider
    msWidth = MEASURE_SLIDER_WIDTH * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    msThick = MEASURE_SLIDER_THICKNESS * appScreen.get_height() // FIGMA_SCREEN_HEIGHT
    msLeft = x_center - (msWidth // 2)
    msTop = y_center + (guitarHeight // 2) + (MEASURE_SLIDER_Y_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)
    measureSliderLine = pygame.Rect(msLeft, msTop, msWidth, msThick)
    global MS_WIDTH
    MS_WIDTH = msWidth

    # Measure orb
    measureOrbX, measureOrbY = msLeft, (msTop + msThick // 2)
    orbPos[0] =  int(measureOrbX)
    orbPos[1] = int(measureOrbY)
    global ORB_START_X 
    ORB_START_X = orbPos[0]

    # Only Wonderwall Textbox 
    textBoxWidth = TEXT_BOX_WIDTH * appScreen.get_width() // FIGMA_SCREEN_WIDTH 
    textBoxHeight = TEXT_BOX_HEIGHT * appScreen.get_height() // FIGMA_SCREEN_HEIGHT
    textBoxLeft = forwardX
    textBoxTop = forwardY - (textBoxHeight // 2)
    textBoxRect = pygame.Rect(textBoxLeft, textBoxTop, textBoxWidth, textBoxHeight)
    
    fontSize = TITLE_FONT_SIZE * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    titleFont = pygame.font.SysFont("Comic Sans", fontSize, bold=False)
    textBoxText = titleFont.render("No other songs. Only Wonderwall.", True, WHITE, RED)
    textBoxTextRect = textBoxText.get_rect()
    textBoxTextRect.center = textBoxRect.center

    # Append objects to list
    objects.append((titleText, titleTextRect))  # Title
    objects.append((guitarSurface, guitarRect)) # Image
    objects.append(playCoordinates)             # Play button
    objects.append(pauseLeftBarRect)            # Left Pause Bar
    objects.append(pauseRightBarRect)           # Right Pause Bar
    objects.append(backCoordinates)             # Back triangle
    objects.append(backBarRect)                 # Back bar
    objects.append(forwardCoordinates)          # Forward triangle
    objects.append(forwardBarRect)              # Forward bar
    objects.append(measureSliderLine)           # Measure slider
    objects.append((orbPos[0], orbPos[1]))      # Orb
    objects.append((textBoxText, textBoxTextRect)) # Only Wonderwall Textbox

    return objects

def createColors():
    colors = []

    colors.append(WHITE)    # Title
    colors.append(None)     # Image
    colors.append(WHITE)    # Play button
    colors.append(WHITE)    # Left Pause Bar
    colors.append(WHITE)    # Right Pause Bar
    colors.append(WHITE)    # Back triangle
    colors.append(WHITE)    # Back bar
    colors.append(WHITE)    # Forward triangle
    colors.append(WHITE)    # Forward bar
    colors.append(WHITE)    # Measure slider
    colors.append(WHITE)    # Orb
    colors.append(RED)      # Only Wonderwall Textbox

    return colors

def createRadii(appScreen : pygame.Surface, L):

    if appScreen.get_height() > appScreen.get_width():
        orbRadius = appScreen.get_height() * ORB_RADIUS // FIGMA_SCREEN_HEIGHT
    else:
        orbRadius = appScreen.get_width() * ORB_RADIUS // FIGMA_SCREEN_WIDTH
    
    radii = [None] * len(L)
    radii[ORB_IDX] = orbRadius
    return radii

def drawObjects(screen : pygame.Surface, objects : list, colors : list[pygame.Color], radii : list[int], showing : list[bool]):
    counter = -1
    for item in objects:
        counter += 1
        if not showing[counter]: continue

        if type(item) == pygame.Rect:
            pygame.draw.rect(screen, colors[counter], item)
        elif type(item) == tuple and len(item) == 2 and \
            type(item[0]) == pygame.Surface and type(item[1]) == pygame.Rect: # textRect
            screen.blit(item[0], item[1])
        elif type(item) == tuple and len(item) == 3 and \
            type(item[0]) == type(item[1]) == type(item[2]) == tuple: # triangle
            pygame.draw.polygon(screen, colors[counter], item)
        elif type(item) == tuple and len(item) == 4 and \
            type(item[0]) == type(item[1]) == type(item[2]) == type(item[3]) == int: # line
            end_pos = item[0] + item[2]
            pygame.draw.line(screen, colors[counter], (item[0], item[1]), (end_pos, item[1]), item[3])
        elif type(item) == tuple and len(item) == 2 and \
            type(item[0]) == type(item[1]) == int: # circle
            pygame.draw.circle(screen, colors[counter], item, radii[counter])
        else:
            print(f"Drawing Error. Type found: {type(item)}")
    return

def createShowParams(L):
    showing = [True] * len(L)
    showing[PAUSE_BAR1_IDX] = False
    showing[PAUSE_BAR2_IDX] = False
    showing[TEXT_BOX_IDX] = False
    return showing