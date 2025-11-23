"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    lives = NUM_LIVES

    # Add the animation loop here!
    while True:
        if graphics.get_game_start():
            graphics.move_ball()
            graphics.check_collision()
            if not graphics.has_bricks():  # win
                graphics.reset_ball()
                graphics.win_label_1()
                graphics.win_label_2()
                break
            if graphics.get_lost():
                lives -= 1
                print(lives)

                if lives == 0:  # game over
                    graphics.reset_ball()
                    graphics.game_over_label()
                    break
                graphics.reset_ball()

        pause(FRAME_RATE)




if __name__ == '__main__':
    main()
