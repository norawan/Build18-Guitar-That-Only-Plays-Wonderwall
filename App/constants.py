from pygame.locals import *

# constants
GREEN=(0x14, 0xAE, 0x5C)
RED=(0xF2, 0x48, 0x22)
BACKGROUND=(0x1E, 0x1E, 0x1E)
SKY_BLUE=(0x0D, 0x99, 0xFF)
WHITE_GRAY=(0xE6, 0xE6, 0xE6)
WHITE=(255, 255, 255)
GOLD=(0xFF, 0xE8, 0xA3)
BLACK=(0, 0, 0)
CYAN=(0x33, 0xFF, 0xFF)
GRAY=(0xB3, 0xB3, 0xB3)
DARK_GRAY=(0x75, 0x75, 0x75)
PINK=(0xFF, 0xC7, 0xC2)

MIN_WIDTH=778
MIN_HEIGHT=560
FIGMA_SCREEN_WIDTH=1512
FIGMA_SCREEN_HEIGHT=870
DESIRED_EFFECTS=HWSURFACE|DOUBLEBUF|RESIZABLE

TITLE_WIDTH=100
TITLE_HEIGHT=50
TITLE_Y_OFFSET=150
TITLE_FONT_SIZE=40

GUITAR_IMG_WIDTH=794
GUITAR_IMG_HEIGHT=536
GUITAR_IMG_SCALE_FACTOR=0.75
GUITAR_IMG_Y_OFFSET=50

LARGE_FONT_FACTOR=40

PLAY_SIZE=60
PLAY_BUTTON_Y_OFFSET=50
BACK_BUTTON_X_OFFSET=200
FORWARD_BUTTON_X_OFFSET=200

MEASURE_SLIDER_Y_OFFSET=125
MEASURE_SLIDER_WIDTH=600
MEASURE_SLIDER_THICKNESS=6

ORBX=389
ORBY=860
ORB_RADIUS=12

TEXT_BOX_WIDTH=400
TEXT_BOX_HEIGHT=100

LYRIC_BOX_WIDTH=300
LYRIC_BOX_HEIGHT=200
LYRIC_X_OFFSET=600
LYRIC_FONT_SIZE=30

PLAY_BUTTON_IDX=2
PAUSE_BAR1_IDX=3
PAUSE_BAR2_IDX=4
BACK_TRIANGLE_IDX=5
BACK_BAR_IDX=6
FORWARD_TRIANGLE_IDX=7
FORWARD_BAR_IDX=8
MEASURE_SLIDER_IDX=9
ORB_IDX=10
TEXT_BOX_IDX=11
LYRICS_IDX=12

# Microcontroller things
DEBUG = True
BAUDRATE=115200
MAX_LATENCY=10

NUM_NS_IN_ONE_MINUTE=60000000000
NUM_BEATS_IN_MEASURE=8
QUARTER_NOTE_RATIO=2
TEMPO=80 # in BPM