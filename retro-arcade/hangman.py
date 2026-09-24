""" Hangman Game """
import random
import pyxel

WORD_BANK = [
  "PYTHON", "DOCKER", "CONTAINER", "DEVELOPER", "COMPUTER",
  "SOFTWARE", "PROGRAMMING", "TERMINAL", "KEYBOARD", "NETWORK",
  "JUPITER", "GALAXY", "ADVENTURE", "HORIZON", "PARADOX"
]

class HangmanEngine:
  """ Hangman Engine """
  def __init__(self):
    self.reset()

  def reset(self):
    """ reset """
    self.secret = random.choice(WORD_BANK)
    self.guessed = set()
    self.wrong = 0
    self.max_wrong = 6
    self.game_over = False
    self.won = False

  def update(self):
    """ update """
    if self.game_over or self.won:
      if pyxel.btnp(pyxel.KEY_R):
        self.reset()
      return

    for i in range(26):
      if pyxel.btnp(pyxel.KEY_A + i):
        char = chr(65 + i)
        if char not in self.guessed:
          self.guessed.add(char)
          if char not in self.secret:
            self.wrong += 1
            if self.wrong >= self.max_wrong:
              self.game_over = True

    if all(letter in self.guessed for letter in self.secret):
      self.won = True

  def draw(self):
    pyxel.line(20, 110, 70, 110, 13)
    pyxel.line(40, 110, 40, 40, 13)
    pyxel.line(40, 40, 75, 40, 13)
    pyxel.line(75, 40, 75, 50, 13)

    if self.wrong > 0: pyxel.circb(75, 55, 4, 7)
    if self.wrong > 1: pyxel.line(75, 59, 75, 80, 7)
    if self.wrong > 2: pyxel.line(75, 65, 65, 72, 7)
    if self.wrong > 3: pyxel.line(75, 65, 85, 72, 7)
    if self.wrong > 4: pyxel.line(75, 80, 65, 95, 7)
    if self.wrong > 5: pyxel.line(75, 80, 85, 95, 7)

    disp = "".join([f"{l} " if l in self.guessed else "_ " for l in self.secret])
    pyxel.text(20, 130, f"Word: {disp}", 7)

    used = ", ".join(sorted(list(self.guessed)))
    pyxel.text(20, 145, f"Used: {used}", 5)

    if self.won:
      pyxel.text(100, 65, "YOU WIN!", 11)
      pyxel.text(95, 80, "R to Restart", 7)
    elif self.game_over:
      pyxel.text(100, 65, "GAME OVER!", 8)
      pyxel.text(95, 80, "R to Restart", 7)
      pyxel.text(20, 120, f"Answer: {self.secret}", 8)

