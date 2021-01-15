#ghetto-scrcpy-iOS

It's our most sophisticated and powerful ghetto script for controlling your garbage phone from a linux machine yet.

## Dependencies
Jailbroken IOS device (probably needs to be around iOS13)  ((Tested on iPhone6s iOS14.3 + Arch Linux))  
This thing https://github.com/xuan32546/IOS13-SimulateTouch for simulating touch    
This thing https://github.com/antimof/UxPlay for mirroring your screen    

xdotool for locating windows on your desktop  
The python api for xdotool (make sure to pip install python-libxdo https://rshk.github.io/python-libxdo/genindex.html not just xdo)  

## What does it do?
Control your Jailbroken iOS device from your linux computer.  
Touch/drag/hold/scroll  
Type on your keyboard*  
*this is really ghetto and you will probably need to tweak some values to actually get it working  
(would be nice to fake a bluetooth keyboard or smthn)  

<Insert video of it being cool>  

## How to set it up
1. Get a jailbroken device  
2. Install xdotool https://archlinux.org/packages/community/x86_64/xdotool/  
3. Install this on the device https://github.com/xuan32546/IOS13-SimulateTouch (it will start listening on tcp/6000)  
4. Install this on your machine https://github.com/antimof/UxPlay  (It's in aur, might throw some avahi error, ignore it.)  
If it doesn't work right away, try this:  
```
systemctl stop systemd-resolved.service
systemctl restart avahi-daemon.service
```
5. Mirror your screen to UxPlay  
6. Once that all works, edit the `device_ip`,`device_screen_height`,`device_screen_width` lines in the `scrgto.py` script to align with reality  
7. setup a venv for the script `python3 -m venv ghetto`  
8. install `pip install python-libxdo`  
9. start this script `python3 scrgto.py`  
10. Click on the window with your mirrored screen  

## What does it not do
Work on non-jailbroken iOS devices  
Work on inferior operating systems(Windows,Mac)  
Provide a smooth user experience  
copy-paste  

# If your keyboard types double
Congrats! It seems that for you, sending characters via the API actually works.  
Simply remove the ghetto keyboard parts from the code from the `pressKey` and `pressSpecialKey` functions:

```
s.send(("101" + formatSocketData(TOUCH_DOWN, 7, keymap[key].x, keymap[key].y)).encode())
time.sleep(0.01)
s.send(("101" + formatSocketData(TOUCH_UP, 7, keymap[key].x, keymap[key].y)).encode())
```
and
```
s.send(("101" + formatSocketData(TOUCH_DOWN, 7, specialKeymap[key].x, specialKeymap[key].y)).encode())
time.sleep(0.01)
s.send(("101" + formatSocketData(TOUCH_UP, 7, specialKeymap[key].x, specialKeymap[key].y)).encode())
```
Now you should be typing normally.

# How to get the keyboard better aligned
If you aren't using an iPhone6s with the default keyboard, you might find the keyboard is misaligned, or isn't working.  
The touch sim API we are using is kinda incosistent on sending characters, and doesn't work on my phone, therefore I actually tap the virtual keyboard on the screen with the script.  
I know.... maybe next time you'll think about that before buying a phone.  
So because of this, based on the resolution/aspect ratio/keyboard layout of your specific device, it might be kinda weird.  
You have these 6 variables to tweak all aspects of keyboard positioning:  

```py
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
```
`keyHeight` and `keyWidth` is the height and width of a button on your virtual keyboard in pixels.  
Set them to the closest approximation you can. It's a trial and error process.  

`row1-4_x` is the offset from the left side of the first button on your virtual keyboard (Excluding shift!)    
It's set so it offsets to the CENTER of the button.  
`row4` is the top row (q,w,e,r,t,y)  and `row1` is the bottom row (modifier keys, space, enter etc)  

If your space or enter is misaligned, edit these lines in the code:  
```py
keyboard.Key.space  :  KeyTable(row1_x+3*keyWidth,row1_y),
keyboard.Key.enter  :  KeyTable(device_screen_width-keyWidth, row1_y),
```

That should mostly set you up, thankfully it only has to be set once per device.  

## Protips
Set your phone to never lock itself, as you cannot unlock it remotely  
Middlemouse is "home" but it's not simulating the actual home button, it's actually calling the springboard app.  
Because of that it's kinda janky, and you'll need to click once to make it behave.  
If you have gesture control on your phone you might be able to somehow program a home gesture, but I didn't have much luck with that.  

## Todo
Create a fake bluetooth device so we can finally type like human beings, and copy-paste.  
Make home invocation less glitchy.  
Bankrupt Apple so they don't make any more trash.  
