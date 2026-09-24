""" Game Menu """
import pyxel
from snake import SnakeEngine
from hangman import HangmanEngine
from platformer import PlatformerEngine

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 160

MENU = 0
SNAKE = 1
HANGMAN = 2
PLATFORMER = 3

class ArcadeApp:
  def __init__(self):
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Arcade")
    self.current_state = MENU
    self.menu_selection = 0

    # Instantiate standalone logic engine contexts
    self.snake_game = SnakeEngine()
    self.hangman_game = HangmanEngine()
    self.platformer_game = PlatformerEngine()

    pyxel.run(self.update, self.draw)

  def update(self):
    if self.current_state == MENU:
      if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
        self.menu_selection = (self.menu_selection - 1) % 3
      elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
        self.menu_selection = (self.menu_selection + 1) %3

      if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
        if self.menu_selection == 0:
          self.snake_game.reset()
          self.current_state = SNAKE
        elif self.menu_selection == 1:
          self.hangman_game.reset()
          self.current_state = HANGMAN
        elif self.menu_selection == 2:
          self.platformer_game.reset()
          self.current_state = PLATFORMER

    else:
      # Let 'M' return to menu from either game
      if pyxel.btnp(pyxel.KEY_M):
        self.current_state = MENU
        return

      # Route inputs directly down to sub-module loops
      if self.current_state == SNAKE:
        self.snake_game.update()
      elif self.current_state == HANGMAN:
        self.hangman_game.update()
      elif self.current_state == PLATFORMER:
        self.platformer_game.update()

  def draw(self):
    pyxel.cls(0)

    if self.current_state == MENU:
      pyxel.text(50, 30, "RETRO ARCADE", 10)
      col1 = 11 if self.menu_selection == 0 else 7
      col2 = 11 if self.menu_selection == 1 else 7
      col3 = 11 if self.menu_selection == 2 else 7
      pyxel.text(40, 60, f"{'> ' if self.menu_selection == 0 else '  '}1. PLAY SNAKE", col1)
      pyxel.text(40, 80, f"{'> ' if self.menu_selection == 1 else '  '}2. PLAY HANGMAN", col2)
      pyxel.text(40, 100, f'{"> " if self.menu_selection == 2 else " "}3. PLAY SUPER MARIO RUN', col3)
      pyxel.text(25, 130, "Press Enter to Select", 5)
    else:
      # Render active state view frames & menu bar anchor
      pyxel.text(110, 4, "M: Menu", 5)
      if self.current_state == SNAKE:
        self.snake_game.draw()
      elif self.current_state == HANGMAN:
        self.hangman_game.draw()
      elif self.current_state == PLATFORMER:
        self.platformer_game.draw()

if __name__ == "__main__":
  ArcadeApp()

