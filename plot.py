#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
# from matplotlib.animation import FuncAnimation
import glob

# IMPORTING FROM ANIMATE2
# get the filenames, make sure they are sorted in time
fnames='run1/tab/LinWave*tab'
f = glob.glob(fnames)
f.sort()
length = len(f)
#print('DEBUG: %s has %d files' % (fnames,len(f)))

# global vars
current_frame = 0
is_playing = False
loop = False

delay= 10 / 1000

# getting the variable names
file = open(f[0]) # just use the first file
file.readline()
variables = file.readline().split()[2:]
file.close()

# function that draws each frame of the animation
def animate(i):
    global xcol, ycol, current_frame
    # print(f[i])
    d = np.loadtxt(f[i]).T
    x = d[ixcol]
    y = d[iycol]
    file = open(f[i]) # open file to retreive time information
    # first line is target
    # terribly lazy but it works, maybe just use regex
    time = file.readline().split('=')[1].split(' ')[0]
    file.close()
    ax.clear()
    ax.plot(x, y)
    #ax.set_xlim([0,20])
    #ax.set_ylim([0,10])
    ax.set_title(f'Frame: {current_frame} / {length}\nTime: {time}')
    ax.set_xlabel(xcol)
    ax.set_ylabel(ycol)  
# END IMPORT

# pauses the animation
def pause(self=None):
    global is_playing
    if is_playing:
        fig.canvas.stop_event_loop()
        is_playing = False

# plays the animation (either starts or resumes)
def play(self=None):
    global is_playing, current_frame, ax, length
    if not is_playing:
        is_playing = True
        while current_frame < length and is_playing:
            animate(current_frame)
            current_frame += 1
            fig.canvas.draw_idle()
            fig.canvas.start_event_loop(delay)
        is_playing = False
        if loop:
            restart()

# loops the animation
def loopf(self=None):
    global loop, bloop
    if loop:
        bloop.color = '0.85' # this is the default color
    else:
        bloop.color = 'cyan' # highlighted color
    loop = not loop

# restarts the animation from the beginning
def restart(self=None):
    global current_frame
    pause()
    current_frame=0
    play()

# select the horizontal variable
def select_h(label):
    global current_frame, ycol
    update_cols(label, ycol)
    restart()

# select the verticle variable
def select_v(label):
    global current_frame, xcol
    update_cols(xcol, label)
    restart()

def update_cols(x, y):
    global xcol, ycol, ixcol, iycol
    xcol=x
    ycol=y
    ixcol = variables.index(x)
    iycol = variables.index(y)

# 0-based, change from animate2
xcol=variables[0]
ycol=variables[0]
ixcol = 0
iycol = 0

# plotting configuration
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.33, bottom=0.2)
# pause on close otherwise we might freeze
# i wonder if this actually works
fig.canvas.mpl_connect('close_event', lambda _: pause())

rax = fig.add_axes([0.05, 0.7, 0.15, 0.15])
radio = RadioButtons(rax, tuple(variables))
rax.text(-0.055, 0.07, 'Horizontal Axis')
    
radio.on_clicked(select_h)
rax = fig.add_axes([0.05, 0.4, 0.15, 0.15])

radio2 = RadioButtons(rax, tuple(variables))
rax.text(-0.055, 0.07, 'Vertical Axis')
radio2.on_clicked(select_v)

# button shift
lshift = 0.65

bloop = Button(fig.add_axes([1.028 - lshift, 0.05, 0.1, 0.075]), 'Loop')
bloop.on_clicked(loopf)

brestart = Button(fig.add_axes([0.919 - lshift, 0.05, 0.1, 0.075]), 'Restart')
brestart.on_clicked(restart)

bres = Button(fig.add_axes([0.81 - lshift, 0.05, 0.1, 0.075]), 'Play')
bres.on_clicked(play)

bpause = Button(fig.add_axes([0.7 - lshift, 0.05, 0.1, 0.075]), 'Pause')
bpause.on_clicked(pause)

plt.show()
