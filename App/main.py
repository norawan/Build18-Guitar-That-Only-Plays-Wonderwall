import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # remove self-advertisement

from constants import *
from procedures import *
from wonderwall import *

import time
import serial
from serial.tools.list_ports import comports

RPIPORT = None
for port in comports():
    strPort = str(port)
    if "RaspberryPi Pico" in strPort:
        RPIPORT = strPort.split(" ")[0] # Get the first part before the - Raspberry Pi Pico
if RPIPORT != None:
    ser = serial.Serial(RPIPORT, BAUDRATE, timeout=MAX_LATENCY)
    
pygame.init()
screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), 
                                DESIRED_EFFECTS)

pygame.display.set_caption('Guitar That Only Plays Wonderwall')
iconImage = pygame.image.load("App/images/Wonderwall.png")
pygame.display.set_icon(iconImage)

running = True

# Wonderwall state
playing = False
scheduledPiece, totalMeasures, lyrics = getWonderwallDict()
startTime = 0
timePlayed = 0
startMeasure = 0
currentMeasure = 0
changedMeasure = False
justStarted = True
currentOffset = 0
chordsToPlay = {}
offsetList = []
measureDuration_ns = (NUM_NS_IN_ONE_MINUTE / (TEMPO)) * NUM_BEATS_IN_MEASURE
if DEBUG: print("Measure duration (ns): {}".format(measureDuration_ns))
if DEBUG: print("Total measures: {}".format(totalMeasures))

# application objects
orbPos = [0, 0]
objects = createObjects(screen, orbPos, lyrics, int(currentMeasure))
colors = createColors()
radii = createRadii(screen, objects)
showing = createShowParams(objects)
userHasOrb = False

###############################################################################
# Helper Functions
###############################################################################

def togglePlayPause():
    showing[PLAY_BUTTON_IDX] = not showing[PLAY_BUTTON_IDX]
    showing[PAUSE_BAR1_IDX] = not showing[PAUSE_BAR1_IDX]
    showing[PAUSE_BAR2_IDX] = not showing[PAUSE_BAR2_IDX]

def getMeasureFromTime():
    currentTime = time.time_ns()
    elapsedTime = timePlayed + (currentTime - startTime)
    measureNumber = elapsedTime // measureDuration_ns
    return measureNumber

def getCurrentOffset():
    currentTime = time.time_ns()
    elapsedTime = timePlayed + (currentTime - startTime)
    offset = (elapsedTime / measureDuration_ns) % 1
    return offset

# Plays input chord by sending command over serial port
def playChord(chord: str):
    if RPIPORT != None and not userHasOrb:
        # Only send chord to RPI if connected and user not adjusting
        print(chord)
        message = chord + "\n"
        ser.write(message.encode())
        
###############################################################################
# Main Loop
###############################################################################
while running:
    mouseX, mouseY = pygame.mouse.get_pos()

    # Set cursor when selecting pressable button
    if (showing[PLAY_BUTTON_IDX] and mouseInTriangle(objects[PLAY_BUTTON_IDX], mouseX, mouseY)) or \
        (not showing[PLAY_BUTTON_IDX]) and mouseInPauseButton(objects[PAUSE_BAR1_IDX], objects[PAUSE_BAR2_IDX], mouseX, mouseY) or \
        (mouseInSeekButton(objects[BACK_TRIANGLE_IDX], objects[BACK_BAR_IDX], mouseX, mouseY)) or \
        mouseInCircle(objects[ORB_IDX], radii[ORB_IDX], mouseX, mouseY):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Show/Hide Only Wonderwall Textbox
    if (mouseInSeekButton(objects[FORWARD_TRIANGLE_IDX], objects[FORWARD_BAR_IDX], mouseX, mouseY)):
        showing[TEXT_BOX_IDX] = True
    else:
        showing[TEXT_BOX_IDX] = False

    currentMeasure, currentOffset, timePlayed, changedMeasure = updateCurrentMeasure(userHasOrb, currentMeasure, currentOffset, timePlayed, totalMeasures, measureDuration_ns, mouseX) # update current measure with mouse
    # mMatch orb position to current measure
    orbPosTuple = updateMeasureOrb(currentOffset, currentMeasure, totalMeasures, orbPos) 
    # Update slider graphics
    orbPos[0], orbPos[1] = orbPosTuple
    objects[ORB_IDX] = orbPosTuple
    # Update lyrics textbox
    lyricTuple = updateLyric(objects[LYRICS_IDX], lyrics, int(currentMeasure))
    objects[LYRICS_IDX] = lyricTuple

    # Handle user events
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                playing = not playing

        elif event.type == KEYUP:
            pass

        elif event.type == VIDEORESIZE:
            width, height = event.size
            if width < MIN_WIDTH:
                width = MIN_WIDTH
            if height < MIN_HEIGHT:
                height = MIN_HEIGHT
            screen = pygame.display.set_mode((width, height), DESIRED_EFFECTS)
            objects = createObjects(screen, orbPos, lyrics, int(currentMeasure))
            radii = createRadii(screen, objects)

        elif event.type == MOUSEBUTTONDOWN:
            if showing[PLAY_BUTTON_IDX] and mouseInTriangle(objects[PLAY_BUTTON_IDX], mouseX, mouseY):
                # Pressed Play
                if DEBUG: print("Playing")
                togglePlayPause()
                playing = not playing
                startTime = time.time_ns()
                
            elif (not showing[PLAY_BUTTON_IDX]) and mouseInPauseButton(objects[PAUSE_BAR1_IDX], objects[PAUSE_BAR2_IDX], mouseX, mouseY):
                # Pressed Pause
                if DEBUG: print("Pausing")
                # Update time played
                timePlayed = timePlayed + time.time_ns() - startTime
                togglePlayPause()
                playing = not playing

            elif (mouseInSeekButton(objects[BACK_TRIANGLE_IDX], objects[BACK_BAR_IDX], mouseX, mouseY)):
                # Pressed Back
                playing = False
                showing[PLAY_BUTTON_IDX] = True
                showing[PAUSE_BAR1_IDX] = False
                showing[PAUSE_BAR2_IDX] = False

                # Reset music variables
                currentMeasure = 0
                currentOffset = 0
                justStarted = True
                timePlayed = 0

                # Update orb position
                orbPosTuple = updateMeasureOrb(currentOffset, currentMeasure, totalMeasures, orbPos) # match orb position to current measure
                orbPos[0], orbPos[1] = orbPosTuple
                objects[ORB_IDX] = orbPosTuple  # update slider graphics
                drawObjects(screen, objects, colors, radii, showing)

            elif mouseInCircle(objects[ORB_IDX], radii[ORB_IDX], mouseX, mouseY): # clicking in slider
                userHasOrb = True

        elif event.type == MOUSEBUTTONUP:
            if (userHasOrb):
                userHasOrb = False
                startTime = time.time_ns()
                chordsToPlay = scheduledPiece.get(currentMeasure, "none")
                if (chordsToPlay != "none"):
                    offsetList = list(chordsToPlay.keys())
                    offsetList.sort()

    # Play Wonderwall
    if (playing and currentMeasure < totalMeasures):
        newMeasure = getMeasureFromTime()
        if (justStarted or changedMeasure or newMeasure > currentMeasure):
            if (DEBUG): print("Measure: {}".format(newMeasure))
            justStarted = False
            changedMeasure = False
            currentMeasure = newMeasure
            chordsToPlay = scheduledPiece.get(currentMeasure, "none")
            if (chordsToPlay != "none"):
                offsetList = list(chordsToPlay.keys())
                offsetList.sort()
        newOffset = getCurrentOffset()

        if (len(offsetList) > 0 and newOffset > offsetList[0]):
            if (DEBUG): print(offsetList[0])

            if (chordsToPlay != "none"):
                chordAtOffset = chordsToPlay.get(offsetList[0], "none")
            if (chordAtOffset != "none"):
                playChord(chordAtOffset)
            offsetList = offsetList[1:]
        
        currentOffset = newOffset

    screen.fill(BLACK)
    drawObjects(screen, objects, colors, radii, showing)
    pygame.display.update()

pygame.quit()