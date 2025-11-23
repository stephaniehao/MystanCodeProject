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

BRICK_SPACING = 5      # 磚塊與磚塊之間的距離
BRICK_WIDTH = 40       # 一個磚塊的寬
BRICK_HEIGHT = 15      # 一個磚塊的高
BRICK_ROWS = 10        # 磚塊的總列數
BRICK_COLS = 10        # 磚塊的總行數
BRICK_OFFSET = 50      # 第一列磚塊頂部與視窗頂部邊界的距離
BALL_RADIUS = 10       # 球的半徑
PADDLE_WIDTH = 75      # 板子的寬
PADDLE_HEIGHT = 15     # 板子的高
PADDLE_OFFSET = 50     # 板子底部與視窗底部邊界的距離
INITIAL_Y_SPEED = 7    # 球在 y 方向移動的初始速度
MAX_X_SPEED = 5        # 球在 x 方向移動的最大速度



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
        self._game_start = False # ball status >> 作為啟動click的開關 # user也會使用
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize our mouse listeners #m2
        # 如未放function 會導致__init__ 卡在這邊不會繼續往下
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

        # 先算出整排bricks的總寬度
        ttl_bricks_w = (w + s) * col - s # 會多出一個space在最右側，要減掉

        # 找出整個bricks area的x座標，使磚塊區域置中
        x_offset = (self._window.width - ttl_bricks_w)/2

        # Each brick row gets a different color to create a vertical gradient effect.
        # 每排磚塊都有不同的顏色，以產生垂直漸變效果。

        # Apply vertical gradient color based on row index
        # 根據行索引套用垂直漸層顏色
        for i in range(row):
            for j in range(col): # 先做第一行的每一列的漸層!
                x = x_offset + j * (w + s)
                y = o + i * (h + s)
                brick = GRect(w, h)
                brick.filled = True
                brick.color = 'seashell'

                # Decide gradient color by row zone
                zone = i * 4 // row  # 把總磚塊數分成4個顏色的區塊 >> 從i=0開始
                if zone == 0:
                    brick.fill_color = 'palevioletred'
                elif zone == 1:
                    brick.fill_color = 'lightcoral'
                elif zone == 2:
                    brick.fill_color = 'lightsalmon'
                else:
                    brick.fill_color = 'peachpuff'

                self._window.add(brick, x=x, y=y)  # 每走完一個j(col)就會增加一個row的漸層 >> 從 i=0 開始

    def has_bricks(self):
        """
        Check if there are any bricks left in the window.
        """
        return self._num_bricks != 0 # is bricks!= 0 >> return True


# - - - - - - - - - - - - - - - - - - - - - - -      [ mouse ]       - - - - - - - - - - - - - - - - - - - - - - - - - -
    # onmousemoved >> move_paddle
    def _handle(self, event): # m2

        mouse_x = event.x # event.x/y 是只用來讀取資料的，所以要先變成物件才做更改
        # 當滑鼠在視窗外時
        if mouse_x <= self._paddle_w/2:
            mouse_x = self._paddle_w/2
        elif mouse_x >= self._window.width - self._paddle_w/2:
            mouse_x = self._window.width - self._paddle_w/2

        # paddle隨滑鼠移動
        # 先將滑鼠置中paddle，然後再fine tune by -1 讓滑鼠在最左和最右時，讓paddle視覺上在視窗內
        self._paddle.x = mouse_x - self._paddle_w/2 - 1


    def _start(self, event):  # m2

        # if self.hp <= 0 or self._game_start:
        #     return  # 直接結束，不做以下的動作

        # mouseclicked only active when not game start
        if not self._game_start:  # 當_game_start = False
            self.__dx = random.randint(1, MAX_X_SPEED)
            self.__dy = INITIAL_Y_SPEED
            if random.random() > 0.5:  # 讓球隨機往左或右
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
                # 消除bricks的前置作業
                if obj is not None and obj is not self._ball and obj is not self._bg: # and obj is not self._label:
                    # 當碰到paddle時，要反彈
                    if obj is self._paddle:
                        if self.__dy > 0:
                            fine_tuned = self._paddle.height + 0.6 # >> fine-tuned for better visual
                            # 當球其中一個角碰到paddle top side，則反彈
                            if self._paddle.y <= self._ball.y + self._ball.height <= self._paddle.y + fine_tuned:
                                self.__dy = - self.__dy
                            # 當球的一角的x=paddle left x, 且 y 在 paddle top y ~ bottom y 之間
                            if self._paddle.y <= self._ball.y <= self._paddle.y + self._paddle.height and\
                                (((self._ball.x + self._ball.width) == self._paddle.x) or\
                                 ((self._ball.x == self._paddle.x) + self._paddle.width)):
                                self.__dy = - self.__dy

                    else:
                        # 消除bricks
                        self._window.remove(obj)
                        self._num_bricks -= 1 # 用來計算bricks remain, 全消掉為win
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