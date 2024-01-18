import pygame
from constants import *

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

def mouseInBackButton(triangleCoordinates : tuple, bar : pygame.Rect, mouseX, mouseY):
    return mouseInButton(bar, mouseX, mouseY) or mouseInTriangle(triangleCoordinates, mouseX, mouseY)

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
    
def createObjects(appScreen : pygame.Surface):
    objects = []

    x_center = appScreen.get_width() // 2
    y_center = appScreen.get_height() // 2
    centerPoint = pygame.Rect(x_center, y_center, 0, 0)

    guitarWidth = (GUITAR_IMG_WIDTH * GUITAR_IMG_SCALE_FACTOR) * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    guitarHeight = (GUITAR_IMG_HEIGHT * GUITAR_IMG_SCALE_FACTOR) * appScreen.get_height() // FIGMA_SCREEN_HEIGHT

    titleWidth = TITLE_WIDTH * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    titleHeight = TITLE_HEIGHT * appScreen.get_height() // FIGMA_SCREEN_HEIGHT
    titleLeft = (x_center - (titleWidth // 2))
    titleTop = y_center - (guitarHeight // 2) - (TITLE_VERTICAL_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)

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

    # Play button
    playBase = PLAY_SIZE * appScreen.get_height() // FIGMA_SCREEN_HEIGHT
    playHeight = playBase
    playX = x_center
    playY = y_center + (guitarHeight // 2) + (PLAY_BUTTON_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)
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
    backX = x_center - BACK_BUTTON_OFFSET * appScreen.get_width() // FIGMA_SCREEN_WIDTH
    backY = y_center + (guitarHeight // 2) + (PLAY_BUTTON_OFFSET * appScreen.get_height() // FIGMA_SCREEN_HEIGHT)
    backCoordinates = makeTriangle((backX, backY), backBase, backHeight, "left")
    backBarWidth = (PLAY_SIZE * appScreen.get_width() // FIGMA_SCREEN_WIDTH) // 3
    backBarHeight = backHeight 
    backBarLeft = backX - (backHeight // 2)
    backBarTop = backY - (backBarHeight // 2)
    backBarRect = pygame.Rect(backBarLeft, backBarTop, backBarWidth, backBarHeight)

    # Append objects to list
    objects.append((titleText, titleTextRect))  # Title
    objects.append((guitarSurface, guitarRect)) # Image
    objects.append(playCoordinates)             # Play button
    objects.append(pauseLeftBarRect)            # Left Pause Bar
    objects.append(pauseRightBarRect)           # Right Pause Bar
    objects.append(backCoordinates)             # Back triangle
    objects.append(backBarRect)                 # Back bar

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

    return colors

def drawObjects(screen : pygame.Surface, objects : list, colors : list[pygame.Color], showing : list[bool]):
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
        # elif type(item) == tuple and len(item) == 2 and \
        #     type(item[0]) == type(item[1]) == int: # circle
        #     pygame.draw.circle(screen, colors[counter], item, radii[counter])
        else:
            print(f"Drawing Error. Type found: {type(item)}")
    return

def createShowParams(L):
    showing = [True] * len(L)
    showing[PAUSE_BAR1_IDX] = False
    showing[PAUSE_BAR2_IDX] = False
    return showing