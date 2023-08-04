#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button, Slider
from argparse import ArgumentParser
import glob

# IMPORTING FROM ANIMATE2
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
    ax.set_title(f'Time: {float(time)}', loc='left')
    ax.set_xlabel(xcol)
    ax.set_ylabel(ycol)  
# END IMPORT

# hard-pauses the animation
# that is, the only way to unpause is by using the play or restart button
def hpause(self=None):
    global hard_paused
    hard_paused = True
    bpause.color = '0.5'
    pause()

# pauses the animation
def pause():
    global is_playing, fig
    if is_playing:
        fig.canvas.stop_event_loop()
        is_playing = False

# plays the animation (either starts or resumes)
def play(self=None):
    global is_playing, current_frame, ax, length, frame_sliding, hard_paused
    if not is_playing:
        is_playing = True
        hard_paused = False
        bpause.color = '0.85'
        while current_frame < length and is_playing:
            animate(current_frame)
            current_frame += 1
            fig.canvas.draw_idle()
            fig.canvas.start_event_loop(delay)
            frame_sliding = False
            fslider.set_val(current_frame)
        is_playing = False
        if loop and current_frame == length:
            restart()

# loops the animation
def loopf(self=None):
    global loop, bloop
    if loop:
        bloop.color = '0.85' # this is the default color
    else:
        bloop.color = '0.5' # highlighted color
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
    if not hard_paused:
        restart()
    else:
        animate(current_frame)
        fig.canvas.draw_idle()


# select the verticle variable
def select_v(label):
    global current_frame, xcol
    update_cols(xcol, label)
    if not hard_paused:
        restart()
    else:
        animate(current_frame)
        fig.canvas.draw_idle()

def update_cols(x, y):
    global xcol, ycol, ixcol, iycol
    xcol=x
    ycol=y
    ixcol = variables.index(x)
    iycol = variables.index(y)

# TODO logarithmic delay slider
def update_delay(x):
    global delay
    delay = x / 1000

def update_fslider(n):
    global frame_sliding, current_frame
    current_frame = n
    animate(current_frame - 1)
    fig.canvas.draw_idle()

def entered_fslider(e):
    if e.inaxes == fax:
        pause()

# BUG: if mouse moves off slider and directly onto something else too fast it might not play
def left_fslider(e):
    if e.inaxes == fax and not hard_paused:
        play()

argparser = ArgumentParser(description='plots the athena tab files specified')
argparser.add_argument('-d', '--dir', help='the directory containing the tab files')
args = argparser.parse_args()

# fnames='run1/tab/LinWave*tab'
f = glob.glob(args.dir + '/*tab')
f.sort()
length = len(f)
#print('DEBUG: %s has %d files' % (fnames,len(f)))

# global vars
current_frame = 0
is_playing = False
hard_paused = True
loop = False
frame_sliding = False

# the time in seconds between frames
delay= 100 / 1000

# getting the variable names
file = open(f[0]) # just use the first file
file.readline()
variables = file.readline().split()[2:]
file.close()

# 0-based, change from animate2
xcol=variables[0]
ycol=variables[0]
ixcol = 0
iycol = 0

# plotting configuration
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.34, bottom=0.32, top=0.85) # old bottom was 0.34
# pause on close otherwise we might freeze
# i wonder if this actually works
# i think it does
fig.canvas.mpl_connect('close_event', hpause)

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

bloop = Button(fig.add_axes([1.028 - lshift, 0.125, 0.1, 0.075]), 'Loop')
bloop.on_clicked(loopf)

brestart = Button(fig.add_axes([0.919 - lshift, 0.125, 0.1, 0.075]), 'Restart')
brestart.on_clicked(restart)

bres = Button(fig.add_axes([0.81 - lshift, 0.125, 0.1, 0.075]), 'Play')
bres.on_clicked(play)

bpause = Button(fig.add_axes([0.7 - lshift, 0.125, 0.1, 0.075]), 'Pause', color='0.5') # by default it is paused
bpause.on_clicked(hpause)

# make slider nonlinear
delay_slider = Slider(
    ax=fig.add_axes([0.18, 0.05, 0.65, 0.03]),
    label='Delay (ms)',
    valmin=1,
    valmax=1000,
    valinit=2,
)

delay_slider.on_changed(update_delay)

fax = fig.add_axes([0.18, 0.95, 0.65, 0.03])
fslider = Slider(
    ax=fax,
    label='Frame',
    valmin=1,
    valmax=length,
    valinit=1,
    valstep=1
)

fslider.on_changed(update_fslider)

# in order to pause the animation when using the frame slider
fig.canvas.mpl_connect('axes_enter_event', entered_fslider)
fig.canvas.mpl_connect('axes_leave_event', left_fslider)

plt.show()