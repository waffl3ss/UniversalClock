import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time
import adafruit_ntp
import socketpool
import wifi
from digitalio import DigitalInOut, Direction

displayio.release_displays()

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

wifi.radio.connect(secrets["ssid"], secrets["password"])

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0)

# send register
R1 = DigitalInOut(board.GP2)
G1 = DigitalInOut(board.GP3)
B1 = DigitalInOut(board.GP4)
R2 = DigitalInOut(board.GP5)
G2 = DigitalInOut(board.GP8)
B2 = DigitalInOut(board.GP9)
CLK = DigitalInOut(board.GP11)
STB = DigitalInOut(board.GP12)
OE = DigitalInOut(board.GP13)

R1.direction = Direction.OUTPUT
G1.direction = Direction.OUTPUT
B1.direction = Direction.OUTPUT
R2.direction = Direction.OUTPUT
G2.direction = Direction.OUTPUT
B2.direction = Direction.OUTPUT
CLK.direction = Direction.OUTPUT
STB.direction = Direction.OUTPUT
OE.direction = Direction.OUTPUT

OE.value = True
STB.value = False
CLK.value = False

MaxLed = 64

c12 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
c13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c12[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 12):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c13[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 13):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

R1.deinit()
G1.deinit()
B1.deinit()
R2.deinit()
G2.deinit()
B2.deinit()
CLK.deinit()
STB.deinit()
OE.deinit()

matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=32,
    bit_depth=1,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11,
    latch_pin=board.GP12,
    output_enable_pin=board.GP13,
    doublebuffer=True,
)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

display.rotation = 180


def createTimeValues():
    current_time_struct = ntp.datetime

    # Adjust UTC time to CET (UTC+1)
    cet_hour = (current_time_struct.tm_hour + 1) % 24

    # Adjust UTC time to IST (UTC+5:30)
    ist_hour = (current_time_struct.tm_hour + 5) % 24
    ist_minute = (current_time_struct.tm_min + 30) % 60

    current_time_string_utc = "{:02}:{:02}".format(
        current_time_struct.tm_hour, current_time_struct.tm_min
    )

    current_time_string_cet = "{:02}:{:02}".format(cet_hour, current_time_struct.tm_min)

    current_time_string_ist = "{:02}:{:02}".format(ist_hour, ist_minute)

    line1 = adafruit_display_text.label.Label(
        terminalio.FONT, color=0xFF0000, text="UTC " + str(current_time_string_utc)
    )
    line1.x = 5
    line1.y = 5

    line2 = adafruit_display_text.label.Label(
        terminalio.FONT, color=0xFF0000, text="CET " + str(current_time_string_cet)
    )
    line2.x = 5
    line2.y = 16

    line3 = adafruit_display_text.label.Label(
        terminalio.FONT, color=0xFF0000, text="IST " + str(current_time_string_ist)
    )
    line3.x = 5
    line3.y = 27

    g = displayio.Group()
    g.append(line1)
    g.append(line2)
    g.append(line3)

    return g


while True:
    try:
        display.root_group = createTimeValues()
        display.refresh(minimum_frames_per_second=0)
        time.sleep(1)
    except Exception as e:
        print("!-!-!-!-!ERROR!-!-!-!-!")
        print(e)
        time.sleep(2)
