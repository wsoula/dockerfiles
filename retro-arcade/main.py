import pyxel
from snake import SnakeEngine
from hangman import HangmanEngine
from platformer import PlatformerEngine
from shooter import ShooterEngine
from poop_simulator import PoopSimulator

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 160

MENU = 0
SNAKE = 1
HANGMAN = 2
PLATFORMER = 3
SHOOTER = 4
POOP_SIM = 5

class ArcadeApp:
  def __init__(self):
    pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Arcade")

    # Enable native engine cursor / touch tracking immediately
    pyxel.mouse(True)

    self.current_state = MENU
    self.menu_selection = 0

    self.snake_game = SnakeEngine()
    self.hangman_game = HangmanEngine()
    self.platformer_game = PlatformerEngine()
    self.shooter_game = ShooterEngine()
    self.poop_sim_game = PoopSimulator()

    pyxel.run(self.update, self.draw)

  def update(self):
    if self.current_state == MENU:
      pyxel.mouse(True)

      # 1. Keyboard Nav Fallbacks
      if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
        self.menu_selection = (self.menu_selection - 1) % 5
      elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
        self.menu_selection = (self.menu_selection + 1) % 5
      if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
        self.launch_game()

      # 2. PURE NATIVE POLLING MOUSE/TOUCH HITBOXES
      # Pyxel maps browser touches natively to mouse coordinates
      mx = pyxel.mouse_x
      my = pyxel.mouse_y

      # Box horizontal boundary limits are X: 15 to 145
      if 15 <= mx <= 145:
        for idx in range(5):
          button_top = 34 + (idx * 20)
          button_bottom = button_top + 14

          if button_top <= my <= button_bottom:
            self.menu_selection = idx

            # Check for native click/tap activation frames
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
              self.launch_game()

    else:
      if pyxel.btnp(pyxel.KEY_M):
        self.current_state = MENU
        return

      if self.current_state == SNAKE:
        self.snake_game.update()
      elif self.current_state == HANGMAN:
        self.hangman_game.update()
      elif self.current_state == PLATFORMER:
        self.platformer_game.update()
      elif self.current_state == SHOOTER:
        self.shooter_game.update()
      elif self.current_state == POOP_SIM:
        self.poop_sim_game.update()

  def launch_game(self):
    if self.menu_selection == 0:
      self.snake_game.reset()
      self.current_state = SNAKE
    elif self.menu_selection == 1:
      self.hangman_game.reset()
      self.current_state = HANGMAN
    elif self.menu_selection == 2:
      self.platformer_game.reset()
      self.current_state = PLATFORMER
    elif self.menu_selection == 3:
      self.shooter_game.reset()
      self.current_state = SHOOTER
    elif self.menu_selection == 4:
      self.poop_sim_game.reset()
      self.current_state = POOP_SIM

  def draw(self):
    pyxel.cls(0)
    if self.current_state == MENU:
      pyxel.text(50, 12, "RETRO ARCADE", 10)

      game_titles = [
        "1. PLAY SNAKE",
        "2. PLAY HANGMAN",
        "3. SUPER MARIO RUN",
        "4. ENDLESS SHOOTER",
        "5. POOP SIMULATOR"
      ]

      for idx, title in enumerate(game_titles):
        x_pos = 15
        y_pos = 34 + (idx * 20)
        is_highlighted = (self.menu_selection == idx)

        pyxel.rectb(x_pos, y_pos, 130, 14, 11 if is_highlighted else 5)
        pyxel.text(x_pos + 10, y_pos + 4, title, 14 if is_highlighted else 7)

      pyxel.text(25, 145, "Press Enter or Tap to Select", 5)
    else:
      pyxel.text(110, 4, "M: Menu", 5)
      if self.current_state == SNAKE:
        self.snake_game.draw()
      elif self.current_state == HANGMAN:
        self.hangman_game.draw()
      elif self.current_state == PLATFORMER:
        self.platformer_game.draw()
      elif self.current_state == SHOOTER:
        self.shooter_game.draw()
      elif self.current_state == POOP_SIM:
        self.poop_sim_game.draw()

if __name__ == "__main__":
  ArcadeApp()
