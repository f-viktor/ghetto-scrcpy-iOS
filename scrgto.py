import socket
import time
import xdo
import pynput
from pynput.mouse import Listener, Button, Controller
from pynput import keyboard

''' set these 3 values custom to your device '''
#the IP of your iphone/ipad
device_ip="192.168.0.158"

#resolution for scaling HxW (iphone6s example)
device_screen_height=1334
device_screen_width=750



# touch event types
TOUCH_UP = 0
TOUCH_DOWN = 1
TOUCH_MOVE = 2
SET_SCREEN_SIZE = 9

#global var to see if a finger is currently held down on the device
TOUCH_HOLD = False
keymap = {}
specialKeymap = {}

#trying to automate adjusting the key locations
#if your keys are off, try adjusting this
#everything is in pixels
#keyboards will be slightly different based on what field you are typing in, so you know
#would be nice if you could just send a keyboard event, but maybe you should've thought about that before buying that phone.
class KeyTable:

    def __init__(self, x, y, shift=False, number=False):
        self.x = x
        self.y = y
        self.shift = shift
        self.number = number

#it assumes US layout
def generateKeymap():
    global keymap
    global specialKeymap


    ''' You will very likely have to tweak these 6 values to align your keyboard correctly'''
    #approx. how many pixels wide and high are keys:
    keyHeight=120
    keyWidth=75

    # base offset for the row letters, try to align it with the center of the buttons in each row
    # row 1 is the bottom row (space, enter, etc)
    row1_x = 50
    row2_x = 140
    row3_x = 75
    row4_x = 50


    #set the height of the keyboard rows
    row1_y=(device_screen_height-keyHeight/2)
    row2_y=row1_y-keyHeight
    row3_y=row2_y-keyHeight
    row4_y=row3_y-keyHeight


    keymap ={
        # top row
        'q' : KeyTable(row4_x,row4_y),
        'w' : KeyTable(row4_x+1*keyWidth,row4_y),
        'e' : KeyTable(row4_x+2*keyWidth,row4_y),
        'r' : KeyTable(row4_x+3*keyWidth,row4_y),
        't' : KeyTable(row4_x+4*keyWidth,row4_y),
        'y' : KeyTable(row4_x+5*keyWidth,row4_y),
        'u' : KeyTable(row4_x+6*keyWidth,row4_y),
        'i' : KeyTable(row4_x+7*keyWidth,row4_y),
        'o' : KeyTable(row4_x+8*keyWidth,row4_y),
        'p' : KeyTable(row4_x+9*keyWidth,row4_y),
        # mid row
        'a' : KeyTable(row3_x,row3_y),
        's' : KeyTable(row3_x+1*keyWidth,row3_y),
        'd' : KeyTable(row3_x+2*keyWidth,row3_y),
        'f' : KeyTable(row3_x+3*keyWidth,row3_y),
        'g' : KeyTable(row3_x+4*keyWidth,row3_y),
        'h' : KeyTable(row3_x+5*keyWidth,row3_y),
        'j' : KeyTable(row3_x+6*keyWidth,row3_y),
        'k' : KeyTable(row3_x+7*keyWidth,row3_y),
        'l' : KeyTable(row3_x+8*keyWidth,row3_y),
        # bottom row
        'z' : KeyTable(row2_x,row2_y),
        'x' : KeyTable(row2_x+1*keyWidth,row2_y),
        'c' : KeyTable(row2_x+2*keyWidth,row2_y),
        'v' : KeyTable(row2_x+3*keyWidth,row2_y),
        'b' : KeyTable(row2_x+4*keyWidth,row2_y),
        'n' : KeyTable(row2_x+5*keyWidth,row2_y),
        'm' : KeyTable(row2_x+6*keyWidth,row2_y),
    }

    # special keys
    specialKeymap = {
        keyboard.Key.shift  :  KeyTable(row1_x,row2_y),
        keyboard.Key.shift_r  :  KeyTable(row1_x,row2_y),
        keyboard.Key.ctrl  :  KeyTable(row1_x,row1_y),
        keyboard.Key.ctrl_r  :  KeyTable(row1_x,row1_y),
        keyboard.Key.space  :  KeyTable(row1_x+3*keyWidth,row1_y),
        keyboard.Key.enter  :  KeyTable(device_screen_width-keyWidth, row1_y),
        keyboard.Key.backspace  :  KeyTable(device_screen_width-keyWidth, row2_y),
    }

TOAST_TYPE_SUCCESS = 4
TOAST_TYPE_NORMAL = 3
TOAST_TYPE_WARNING = 2
TOAST_TYPE_ERROR = 1

def showToast(s, type, content, duration):
    s.send(("22" + str(type) + ";;" + str(content) + ";;" + str(duration) + "\r\n").encode())
    print(s.recv(1024))


def pressKey(key):
    try:
        s.send(("101" + formatSocketData(TOUCH_DOWN, 7, keymap[key].x, keymap[key].y)).encode())
        time.sleep(0.01)
        s.send(("101" + formatSocketData(TOUCH_UP, 7, keymap[key].x, keymap[key].y)).encode())

        # this should work, but doesn't on my phone
        s.send(("241;;"+key+"\r\n").encode())

    except:
        print("key pressed pressed isnt mapped", key)


def pressSpecialKey(key):
    try:
        s.send(("101" + formatSocketData(TOUCH_DOWN, 7, specialKeymap[key].x, specialKeymap[key].y)).encode())
        time.sleep(0.01)
        s.send(("101" + formatSocketData(TOUCH_UP, 7, specialKeymap[key].x, specialKeymap[key].y)).encode())

        # I have managed to improve the Python language in a way
        if key == keyboard.Key.space:
                    s.send(("241;;"+" \r\n").encode())
        if key == keyboard.Key.backspace:
                    s.send("244;;1\r\n".encode())
        if key == keyboard.Key.left:
                    s.send("243;;-1\r\n".encode())
        if key == keyboard.Key.right:
                    s.send("243;;1\r\n".encode())

    except:
        print("key pressed pressed isnt mapped", key)


# you can copy and paste these methods to your code
def formatSocketData(type, index, x, y):
    return '{}{:02d}{:05d}{:05d}'.format(type, index, int(x*10), int(y*10))

def goHome(s):
    s.send("11com.apple.springboard".encode())

    #something like this would be nice to un-bug the springboard laucher
    #time.sleep(0.2)
    #s.send(("101" + formatSocketData(TOUCH_DOWN, 7, 700, 1000)).encode())  # touch down "10" at the beginning means "perform touch event". The third digit("1") is the data count.
    #time.sleep(0.02)
    #s.send(("101"+formatSocketData(TOUCH_UP, 7, 700, 1000)).encode())


def tap(x,y):
    global TOUCH_HOLD
    s.send(("101" + formatSocketData(TOUCH_DOWN, 7, x, y)).encode())
    TOUCH_HOLD = True

def holdMove(x,y):
    s.send(("101"+formatSocketData(TOUCH_MOVE, 7, x, y)).encode())

def Kazuo_Ishiguro(x,y):
    global TOUCH_HOLD
    s.send(("101"+formatSocketData(TOUCH_UP, 7, x, y)).encode())
    TOUCH_HOLD = False
    # this ghetto thing just makes it smoother.
    time.sleep(0.01)
    s.send(("101"+formatSocketData(TOUCH_UP, 7, x, y)).encode())
    time.sleep(0.01)
    s.send(("101"+formatSocketData(TOUCH_UP, 7, x, y)).encode())

def verticalSwipe(scrollUp):
        y=500
        s.send(("101" + formatSocketData(TOUCH_DOWN, 7, 300, y)).encode())  # touch down "10" at the beginning means "perform touch event". The third digit("1") is the data count.
        # the above code is equal to s.send(("1011070300010000").encode())
        time.sleep(0.02) # if you run this script on your computer, change sleep time to 0.2. (This is weird that python sleeps much longer on iOS than it should)

        if scrollUp>0:
            while y <= 1000:
                s.send(("101" + formatSocketData(TOUCH_MOVE, 7, 300, y)).encode())  # move our finger 7 to the right
                y += 30
                time.sleep(0.02)
        else:
            while y >= 100:
                s.send(("101" + formatSocketData(TOUCH_MOVE, 7, 300, y)).encode())  # move our finger 7 to the left
                y -= 30
                time.sleep(0.02)

        s.send(("101" + formatSocketData(TOUCH_UP, 7, 300, y)).encode())  # release finger

#should do a back move but doesnt work
def horizontalSwipe():
    x = 0
    s.send(("101" + formatSocketData(TOUCH_DOWN, 7, x, 1000)).encode())  # touch down "10" at the beginning means "perform touch event". The third digit("1") is the data count.
    # the above code is equal to s.send(("1011070300010000").encode())
    time.sleep(0.01) # if you run this script on your computer, change sleep time to 0.2. (This is weird that python sleeps much longer on iOS than it should)
    while x <= 400:
        print("sent",x)
        s.send(("101" + formatSocketData(TOUCH_MOVE, 7, x, 1000)).encode())  # move our finger 7 to the right
        x += 20
        time.sleep(0.01)


    s.send(("101" + formatSocketData(TOUCH_UP, 7, x, 1000)).encode())  # release finger

# why you need math for programming
# the window is going to be constrained either by the width or the height of the screen
# this is really only a question on a tiling vm but that's the onyl vm worth using anyway
# the dimension where the ratio is bigger is the one that is going to constrain the screen
# we use the ratio of that dimension to scale the location of the click
def projectToScreen(mouse_location, window_location, window_size):
    x = mouse_location.x-window_location.x
    y = mouse_location.y-window_location.y
    scale = device_screen_height/window_size.height
    horizontal_offset=0
    vertical_offset=0
    if scale < device_screen_width/window_size.width:
        scale = device_screen_width/window_size.width
        #offset for the letterboxing
        vertical_offset=int((window_size.height/2)-device_screen_height/scale/2)
    else:
        horizontal_offset=int((window_size.width/2)-device_screen_width/scale/2)

    #print(x, y, "scaled by", scale, "to", int((x-horizontal_offset)*scale), int((y-vertical_offset)*scale), "offset", horizontal_offset, vertical_offset)
    return int((x-horizontal_offset)*scale), int((y-vertical_offset)*scale)

#get the location of the mouse and the window
def getLocations():
    return xdo.get_mouse_location(), xdo.get_window_location(win_id), xdo.get_window_size(win_id)

# if the click happened within the confinds of the window
def inTargetWindow(mouse_location, window_location, window_size):
    if window_location.x < mouse_location.x < window_location.x + window_size.width \
    and window_location.y < mouse_location.y < window_location.y + window_size.height \
    and mouse_location.screen_num == window_location.screen.root:
        return True
    else:
        return False

# mouseclick event
def on_click(x, y, button, pressed):
    mouse_location, window_location, window_size = getLocations()
    if inTargetWindow(mouse_location, window_location, window_size):
        #home button is location independent
        if pressed and button == pynput.mouse.Button.middle:
            goHome(s)
        else:
            #left and right are position dependent
            if pressed and button == pynput.mouse.Button.right:
                horizontalSwipe()
            else:
                x,y = projectToScreen(mouse_location, window_location, window_size)
                if pressed and button == pynput.mouse.Button.left:
                    tap(x,y)
                if not pressed and button == pynput.mouse.Button.left:
                    Kazuo_Ishiguro(x,y)
#mouse movement event
def on_move(x, y):
    global TOUCH_HOLD
    if TOUCH_HOLD:
        mouse_location, window_location, window_size = getLocations()
        if inTargetWindow(mouse_location, window_location, window_size):
            x,y = projectToScreen(mouse_location, window_location, window_size)
            holdMove(x,y)

#mouse scrolling event
def on_scroll(x, y, dx, dy):
    mouse_location, window_location, window_size = getLocations()
    if inTargetWindow(mouse_location, window_location, window_size):
        verticalSwipe(dy)

#keyboard press event
def on_press(key):
    if (xdo.get_focused_window() == win_id):
        try:
            pressKey(key.char)
        except AttributeError:
            pressSpecialKey(key)




if __name__ == '__main__':

    # Connect to the device on port 6000 via ZXTouch tweak
    s = socket.socket()
    s.connect((device_ip, 6000))  # connect to the tweak
    time.sleep(0.1)  # please sleep after connection.

    #Pick your UxPlay window to determine location
    print("Please click on your UxPlay window or other screen mirroring tool")
    xdo = xdo.Xdo()
    win_id = xdo.select_window_with_click()
    print("UxPlay window id selected: ", win_id)

    generateKeymap()
    #listen to keypresses without blocking
    klistener = keyboard.Listener(
        on_press=on_press
        )
    klistener.start()

    with Listener( on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll) as listener:
        listener.join()


    time.sleep(1)


    s.close()
