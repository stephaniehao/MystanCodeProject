"""
File: 
Name:
----------------------
TODO:
"""

from campy.graphics.gobjects import GRect, GOval, GLabel, GLine, GPolygon, GArc
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
import random

#constant
W = 600
H = 440

#global
window = GWindow(W, H, title="Snoopy's Sleepy Night")
# Zzz
z = None
z_y = 245
z_stage = 0 #current stage: 0 → Z, 1 → Zz, 2 → Zzz, 3 → Zzz..., 4 → empty
z_timer = 0 #frame count


def main():
    """
    TODO:
    """
    draw_background()
    draw_stars()
    draw_doghouse()
    draw_tag()

    while True:
        animate_zzz()
        pause(50) # pause 1 sec

def draw_background():
    bg = GRect(W,H)
    bg.filled = True
    window.add(bg)

def draw_stars():
    """
    Draws 80 small white stars randomly across the top area of the screen.
    Each star is a small white circle with random size and position.
    """
    for i in range(80):
        size = random.randint(1,4) # star size
        # Make sure the star stays within the specified area.
        x = random.randint(0, W-size)
        y = random.randint(0, 250)
        star = GOval(size, size, x=x, y=y)
        star.filled = True
        star.color = 'white'
        star.fill_color = 'white'
        window.add(star)


def draw_doghouse():
    roof1 = GPolygon()
    roof1.add_vertex((177.5, 180))
    roof1.add_vertex((372.5, 180))
    roof1.add_vertex((410, 320))
    roof1.add_vertex((140, 320))
    roof1.filled = True
    roof1.fill_color = 'crimson'
    window.add(roof1)

    roof2 = GPolygon()
    roof2.add_vertex((140, 320))
    roof2.add_vertex((410, 320))
    roof2.add_vertex((402.5, 330))
    roof2.add_vertex((147.5, 330))
    roof2.color = 'crimson'
    window.add(roof2)

    for i in range(3):  # 3px
        line1 = GLine(165, 230 + i, 385, 230 + i)
        window.add(line1)
    for i in range(3):  # 3px
        line2 = GLine(152.5, 280 + i, 397.5, 280 + i)
        window.add(line2)

    wall = GRect(180, 90, x=185, y=330)
    wall.filled = True
    wall.fill_color = 'crimson'
    wall.color = 'crimson'
    window.add(wall)

    for i in range(3):  # 3px
        line3 = GLine(185, 360 + i, 365, 360 + i)
        window.add(line3)
    for i in range(3):  # 3px
        line4 = GLine(185, 390 + i, 365, 390 + i)
        window.add(line4)


    door1 = GArc(90, 180, 0, 180)
    door1.filled = True
    door1.fill_color = 'black'
    door1.color = 'black'
    window.add(door1, x=230, y=330)

    door2 = GRect(90, 45, x=230, y=375)
    door2.filled = True
    door2.fill_color = 'black'
    door2.color = 'black'
    window.add(door2)

def draw_tag():
    tag1 = GOval(130, 60)
    tag1.filled = True
    tag1.fill_color = 'saddlebrown'
    tag1.color = 'saddlebrown'
    window.add(tag1, x=215, y=205)


    tag2 = GOval(130, 60)
    tag2.filled = True
    tag2.fill_color = 'peru'
    tag2.color = 'saddlebrown'
    window.add(tag2, x=210, y=200)

    label = GLabel('SNOOPY', x=235, y=245)
    label.font = 'Comic Sans MS-20-BoldItalic'
    window.add(label)


def animate_zzz():
    """
    The zzz label floats upward and changes text every 30 frames
    """
    global z, z_y, z_timer, z_stage

    if z_stage == 0:
        text = 'Z'
    elif z_stage ==1:
        text = 'Zz'
    elif z_stage ==2:
        text ='Zzz'
    elif z_stage ==3:
        text = 'Zzz...'
    else:
        text = ''

    # remove old one
    if z is not None:
        window.remove(z)
    # update location
    z_y -= 0.8  # Move the object upward to simulate a drifting-up animation.
    # new Z
    z = GLabel(text)
    z.color = 'dodgerblue'
    z.font = 'Courier-30'
    window.add(z, x=130, y=z_y)
    # Update the timer so the text changes only once per second,
    # while the same text continues floating upward during that second.
    z_timer += 1
    if z_timer %20 == 0:
        # 20 explanation:
        # pause(50) pauses the animation for 50 milliseconds.
        # One second = 1000 milliseconds → 1000 / 50 = 20.
        # This means the animation loop runs 20 times per second.
        # → So after 20 cycles (≈1 second), we update the text to the next one.
        z_stage += 1
        if z_stage > 4:
            z_stage = 0
            z_y = 245



if __name__ == '__main__':
    main()
