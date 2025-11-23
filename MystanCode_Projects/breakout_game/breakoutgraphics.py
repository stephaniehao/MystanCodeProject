"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball



class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):  # , hp=3):

        # store all args as attributes for future access
        self._ball_r = ball_radius
        self._paddle_w = paddle_width
        self._paddle_h = paddle_height
        self._paddle_o = paddle_offset
        self._row = brick_rows
        self._col = brick_cols
        self._brick_w = brick_width
        self._brick_h = brick_height
        self._brick_s = brick_spacing
        self._brick_o = brick_offset
        # self.hp = hp

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self._window = GWindow(width=window_width, height=window_height, title=title)

        # background
        self._bg = GRect(window_width, window_height)
        self._bg.filled = True
        self._bg.fill_color = 'seashell'
        self._bg.color = 'seashell'
        self._window.add(self._bg)

        # Create a paddle
        self._paddle = GRect(paddle_width, paddle_height)
        self._paddle.filled = True
        self._paddle.fill_color = 'mistyrose'
        self._paddle.color = 'lightcoral'
        self._window.add(self._paddle, x=(window_width-paddle_width)/2, y=(window_height-paddle_height-paddle_offset))

        # Draw bricks
        self._draw_bricks()

        # bricks cnts
        self._num_bricks = brick_rows * brick_cols

        # Center a filled ball in the graphical window
        self._ball = GOval(ball_radius*2, ball_radius*2)
        self._ball.filled = True
        self._ball.fill_color = 'salmon'
        self._ball.color = 'indianred'
        self._window.add(self._ball, x=(window_width-self._ball.width)/2, y=(window_height-self._ball.height)/2)

        # # score board
        # self._label = GLabel("")
        # self._label.font = 'Comic Sans MS-10-BoldItalic'
        # self._label.color = 'darkslateblue'
        # self._window.add(self._label)
        #
        # self._score = 0
        # self.update_label()

        # initial setting
        self._game_start = False # ball_status >> acts as the switch that enables the click-to-start behavior.
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize our mouse listeners #m2
        print ('Mouse event listener is active!')
        onmouseclicked(self._start)
        onmousemoved(self._handle)




# - - - - - - - - - - - - - - - - - - - - - -      [ bricks  ]       - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _draw_bricks(self): #m1

        row = self._row
        col = self._col
        w = self._brick_w
        h = self._brick_h
        s = self._brick_s
        o = self._brick_o

        # First, compute the total width of the brick row, including all bricks and the gaps between them.
        ttl_bricks_w = (w + s) * col - s # There will be an extra space on the far right, so we need to subtract it.

        # Compute the x-coordinate of the entire brick area so that the bricks are centered horizontally.
        x_offset = (self._window.width - ttl_bricks_w)/2

        # Each brick row gets a different color to create a vertical gradient effect.
        # Apply vertical gradient color based on row index
        for i in range(row):
            for j in range(col): # First, apply the gradient colors to each column in the first row.
                x = x_offset + j * (w + s)
                y = o + i * (h + s)
                brick = GRect(w, h)
                brick.filled = True
                brick.color = 'seashell'

                # Decide gradient color by row zone
                zone = i * 4 // row  # Divide the total number of bricks into four color sections (starting from i = 0).
                if zone == 0:
                    brick.fill_color = 'palevioletred'
                elif zone == 1:
                    brick.fill_color = 'lightcoral'
                elif zone == 2:
                    brick.fill_color = 'lightsalmon'
                else:
                    brick.fill_color = 'peachpuff'

                # Once all columns (j) are processed, move to the next row and raise the gradient level (i starts at 0).
                self._window.add(brick, x=x, y=y)

    def has_bricks(self):
        """
        Check if there are any bricks left in the window.
        """
        return self._num_bricks != 0 # is bricks!= 0 >> return True


# - - - - - - - - - - - - - - - - - - - - - - -      [ mouse ]       - - - - - - - - - - - - - - - - - - - - - - - - - -
    # onmousemoved >> move_paddle
    def _handle(self, event): # m2

        # Since event.x and event.y are read-only event attributes, we need to store them
        # in our own object/variable before applying any changes.
        mouse_x = event.x
        # When the mouse cursor is outside the window.
        if mouse_x <= self._paddle_w/2:
            mouse_x = self._paddle_w/2
        elif mouse_x >= self._window.width - self._paddle_w/2:
            mouse_x = self._window.width - self._paddle_w/2

        # Move the paddle according to the mouse position.
        # First center the paddle under the mouse, then fine-tune it by -1
        # so that when the mouse reaches the far left or far right,
        # the paddle still appears visually inside the window.
        self._paddle.x = mouse_x - self._paddle_w/2 - 1


    def _start(self, event):  # m2

        # if self.hp <= 0 or self._game_start:
        #     return  # Stop here and do not execute the code that follows.

        # mouseclicked only active when not game start
        if not self._game_start:  # when _game_start = False
            self.__dx = random.randint(1, MAX_X_SPEED)
            self.__dy = INITIAL_Y_SPEED
            if random.random() > 0.5:  # Randomize the initial horizontal direction of the ball (left or right).
                self.__dx = - self.__dx

            self._game_start = True


# - - - - - - - - - - - - - - - - - - - - - - -      [ ball ]       - - - - - - - - - - - - - - - - - - - - - - - - - -

    def move_ball(self):  # m2
        self._ball.move(self.__dx, self.__dy) # move the ball by dx, dy
        # bounce off the left/right edge
        if self._ball.x <= 0 or self._ball.x + self._ball.width >= self._window.width:
            self.__dx = - self.__dx
        # bounce off the top edge
        if self._ball.y <= 0:
            self.__dy = - self.__dy
            # bounce off the bottom edge >> remove from the screen
            if self._ball.y + self._ball.height >= self._window.height:
                self._window.remove(self._ball)

    def reset_ball(self):
        self._window.add(self._ball, x=(self._window.width - self._ball.width) / 2,
                         y=(self._window.height - self._ball.height) / 2)
        self.__dx = 0
        self.__dy = 0

    def check_collision(self):
        # check 4 corners of ball:
        # (0,0) (ball.x+ball.width, 0) (0, ball.y+ball.height) (ball.x+ball.width, ball.y+ball.height)
        for i in (0,1): # x
            for j in (0,1): # y
                x = self._ball.x + i * self._ball.width
                y = self._ball.y + j * self._ball.height
                obj = self._window.get_object_at(x, y)
                # Perform the necessary pre-removal procedures before deleting the brick.
                if obj is not None and obj is not self._ball and obj is not self._bg: # and obj is not self._label:
                    # Bounce the ball when it hits the paddle.
                    if obj is self._paddle:
                        if self.__dy > 0:
                            fine_tuned = self._paddle.height + 0.6 # >> fine-tuned for better visual
                            # Bounce the ball only when one of its corners collides with the paddle's top edge.
                            if self._paddle.y <= self._ball.y + self._ball.height <= self._paddle.y + fine_tuned:
                                self.__dy = - self.__dy
                            # When one corner of the ball has x equal to the paddle's left x,
                            # and its y lies between the paddle's top y and bottom y.
                            if self._paddle.y <= self._ball.y <= self._paddle.y + self._paddle.height and\
                                (((self._ball.x + self._ball.width) == self._paddle.x) or\
                                 ((self._ball.x == self._paddle.x) + self._paddle.width)):
                                self.__dy = - self.__dy

                    else:
                        # Remove the brick.
                        self._window.remove(obj)
                        self._num_bricks -= 1 # Count how many bricks are left; if none remain, the player wins.
                        # self._score += 1
                        # self.update_label()
                        self.__dy = - self.__dy
                    return

# # - - - - - - - - - - - - - - - - - - - - - -     [ score board]       - - - - - - - - - - - - - - - - - - - - - - - - -
#
#     def update_label(self):
#         self._label.text = "Hits: " + str(self._score) + " |  balls Left:  " + str(self.hp)
#         self._label.x = (self._window.width - self._label.width) / 2
#         self._label.y = self._window.height - PADDLE_OFFSET / 2 + self._label.ascent / 2


# - - - - - - - - - - - - - - - - - - - - - - -      [ getting]       - - - - - - - - - - - - - - - - - - - - - - - - -

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def get_game_start(self):
        return self._game_start

    def get_lost(self):
        # bounce off the bottom edge >> remove from the screen
        if self._ball.y + self._ball.height >= self._window.height:
            self._window.remove(self._ball)
            # self.hp -= 1
            # self.update_label()
            self._game_start = False
            return True
        return False

# - - - - - - - - - - - - - - - - - - - - - - -      [ label ]       - - - - - - - - - - - - - - - - - - - - - - - - - -

    def game_over_label(self):  # m4 extend
        game_over = GLabel("Game Over")
        game_over.font = 'Comic Sans MS-50-BoldItalic'
        game_over.color = 'black'
        self._window.add(game_over, (self._window.width - game_over.width) / 2,
                         (self._window.height + game_over.ascent) / 2)

    def win_label_1(self):
        label = GLabel("YOU DID IT!")
        label.font = "Courier-40-bold"
        label.color = "salmon"
        self._window.add(label,x=(self._window.width - label.width) / 2,
                         y=self._window.height * 0.3)

    def win_label_2(self):
        label = GLabel("ALL BLOCKS CLEARED!")
        label.font = "Courier-26-bold"
        label.color = "lightcoral"
        self._window.add(label,x=(self._window.width - label.width) / 2,
                         y=self._window.height * 0.3 + 50)