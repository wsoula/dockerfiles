""" Snake Game """
import pyxel
import random

CELL_SIZE = 8
GRID_WIDTH = 20
GRID_HEIGHT = 20

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeEngine:
  def __init__(self):
    self.reset()

  def reset(self):
    self.snake = [(10, 10), (9, 10), (8, 10)]
    self.dir = RIGHT
    self.next_dir = RIGHT
    self.score = 0
    self.game_over = False
    self.spawn_food()

  def spawn_food(self):
    while True:
      self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
      if self.food not in self.snake:
        break

  def update(self):
    if self.game_over:
      if pyxel.btnp(pyxel.KEY_R):
        self.reset()
      return

    if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W)) and self.dir != DOWN:
      self.next_dir = UP
    elif (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S)) and self.dir != UP:
      self.next_dir = DOWN
    elif (pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A)) and self.dir != RIGHT:
      self.next_dir = LEFT
    elif (pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D)) and self.dir != LEFT:
      self.next_dir = RIGHT

    if pyxel.frame_count % 5 == 0:
      self.dir = self.next_dir
      head_x, head_y = self.snake[0]
      dir_x, dir_y = self.dir
      new_head = (head_x + dir_x, head_y + dir_y)

      if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
          new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
          new_head in self.snake):
        self.game_over = True
        return

      self.snake.insert(0, new_head)
      if new_head == self.food:
        self.score += 10
        self.spawn_food()
      else:
        self.snake.pop()

  def draw(self):
    pyxel.rect(self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE, 8)
    for seg in self.snake[1:]:
      pyxel.rect(seg[0] * CELL_SIZE, seg[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE, 11)
    pyxel.rect(self.snake[0][0] * CELL_SIZE, self.snake[0][1] * CELL_SIZE, CELL_SIZE, CELL_SIZE, 3)
    pyxel.text(4, 4, f"SCORE: {self.score}", 7)

    if self.game_over:
      pyxel.rect(30, 60, 100, 40, 0)
      pyxel.text(60, 70, "GAME OVER", 8)
      pyxel.text(46, 85, "R to Play Again", 7)

