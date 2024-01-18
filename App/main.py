import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # remove self-advertisement

from constants import *
from procedures import *
from wonderwall import *

from threading import Thread
import time
import serial
from serial.tools.list_ports import comports

ports = []

for port in comports():
    strPort=str(port)
    try:
        s = serial.Serial(strPort)
        s.close()
        ports.append(strPort)
    except (OSError, serial.SerialException):
        pass

for port in ports:
    print(port)

if len(ports) > 0:
    ser = serial.Serial(ports[0], BAUDRATE, timeout=MAX_LATENCY)

class ThreadReturn(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
    
pygame.init()
screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT), 
                                DESIRED_EFFECTS)

pygame.display.set_caption('Guitar That Only Plays Wonderwall')
iconImage = pygame.image.load("App/images/Wonderwall.png")
pygame.display.set_icon(iconImage)

running = True

# application objects
objects = createObjects(screen)
colors = createColors()
showing = createShowParams(objects)

# Wonderwall state
wonderwallThread = ThreadReturn(None)
playing = False

scheduledPiece, totalMeasures = getWonderwallDict()
startTime = time.time_ns()
startMeasure = 1
currentMeasure = 1
justStarted = True
currentOffset = 0
chordsToPlay = {}
offsetList = []
measureDuration_ns = (NUM_NS_IN_ONE_MINUTE / (TEMPO)) * NUM_BEATS_IN_MEASURE
print(measureDuration_ns)

###############################################################################
# Helper Functions
###############################################################################

def togglePlayPause():
    showing[PLAY_BUTTON_IDX] = not showing[PLAY_BUTTON_IDX]
    showing[PAUSE_BAR1_IDX] = not showing[PAUSE_BAR1_IDX]
    showing[PAUSE_BAR2_IDX] = not showing[PAUSE_BAR2_IDX]

def getMeasureFromTime():
    currentTime = time.time_ns()
    elapsedTime = currentTime - startTime
    measureNumber = elapsedTime // measureDuration_ns + (startMeasure)
    return measureNumber

def getCurrentOffset():
    currentTime = time.time_ns()
    elapsedTime = currentTime - startTime
    offset = (elapsedTime / measureDuration_ns) - currentMeasure + startMeasure
    return offset

# Plays input chord by sending command over serial port
def playChord(chord):
    
    # ser.write("Em")
    print(chord)
        
###############################################################################
# Main Loop
###############################################################################
while running:
    mouseX, mouseY = pygame.mouse.get_pos()

    # Set cursor when selecting pressable button
    if (showing[PLAY_BUTTON_IDX] and mouseInTriangle(objects[PLAY_BUTTON_IDX], mouseX, mouseY)) or \
        (not showing[PLAY_BUTTON_IDX]) and mouseInPauseButton(objects[PAUSE_BAR1_IDX], objects[PAUSE_BAR2_IDX], mouseX, mouseY) or \
        (mouseInBackButton(objects[BACK_TRIANGLE_IDX], objects[BACK_BAR_IDX], mouseX, mouseY)):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
            objects = createObjects(screen)

        elif event.type == MOUSEBUTTONDOWN:
            if showing[PLAY_BUTTON_IDX] and mouseInTriangle(objects[PLAY_BUTTON_IDX], mouseX, mouseY):
                # Pressed Play
                togglePlayPause()
                playing = not playing
                startTime = time.time_ns()
            elif (not showing[PLAY_BUTTON_IDX]) and mouseInPauseButton(objects[PAUSE_BAR1_IDX], objects[PAUSE_BAR2_IDX], mouseX, mouseY):
                # Pressed Pause
                togglePlayPause()
                playing = not playing
            elif (mouseInBackButton(objects[BACK_TRIANGLE_IDX], objects[BACK_BAR_IDX], mouseX, mouseY)):
                # Pressed Back
                playing = False
                showing[PLAY_BUTTON_IDX] = True
                showing[PAUSE_BAR1_IDX] = False
                showing[PAUSE_BAR2_IDX] = False

                # Reset music variables
                currentMeasure = 1
                justStarted = True

    # Play Wonderwall
    if (playing and currentMeasure <= totalMeasures):
        newMeasure = getMeasureFromTime()
        if (justStarted or newMeasure > currentMeasure):
            if (DEBUG): print("Measure: {}".format(newMeasure))
            justStarted = False
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

    screen.fill(BLACK)
    drawObjects(screen, objects, colors, showing)
    pygame.display.update()

pygame.quit()