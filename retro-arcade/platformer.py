import pyxel
import random

# Screen Configuration
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 160

# Physics Parameters
GRAVITY = 0.4
JUMP_STRENGTH = -6.5
MAX_FALL_SPEED = 6.0
PLAYER_SPEED = 1.8

# Tile definitions
TILE_EMPTY = 0
TILE_FLOOR = 1
TILE_BLOCK = 2

class Goomba:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.vx = -0.6  # Patrol speed moving left initially
    self.width = 8
    self.height = 8
    self.is_alive = True

  def update(self, engine):
    if not self.is_alive:
      return

    # Check ahead for gaps or wall collisions to turn around
    next_x = self.x + self.vx
    # Primitive floor check ahead
    grid_x = int((next_x + (self.width if self.vx > 0 else 0)) // 8)
    grid_y = int((self.y + self.height + 2) // 8)

    # Reverse direction if hitting a wall or walking toward a pit edge
    if engine.check_collision(next_x, self.y) or engine.map_grid.get((grid_x, grid_y), TILE_EMPTY) == TILE_EMPTY:
      self.vx *= -1
    else:
      self.x += self.vx

  def draw(self):
    if not self.is_alive:
      return
    # Animate walking legs by flipping the sprite frame horizontally over time
    u_offset = 8 if (pyxel.frame_count // 6) % 2 == 0 else 16
    # Blit Goomba from bank 0 (U: 8/16, V: 0, W: 8, H: 8, colorkey: 0/black)
    pyxel.blt(self.x, self.y, 0, u_offset, 0, 8, 8, 0)


class PlatformerEngine:
  def __init__(self):
    self.init_sprites()
    self.reset()

  def init_sprites(self):
    """Programs retro textures directly into Pyxel's Image Bank 0."""
    p_data = [
      "00333300",
      "00314100",
      "00344400",
      "00088000",
      "00888800",
      "08088080",
      "00088000",
      "00600600",
      "00600600",
      "06600660",
      "06000060",
      "66000066"
    ]
    for y, row in enumerate(p_data):
      for x, col in enumerate(row):
        pyxel.images[0].pset(x, y, int(col, 16))

    g_data_a = [
      "00444400",
      "04444440",
      "44144144",
      "44444444",
      "04222240",
      "00222200",
      "01100000",
      "11100000"
    ]
    g_data_b = [
      "00444400",
      "04444440",
      "44144144",
      "44444444",
      "04222240",
      "00222200",
      "00000110",
      "00001111"
    ]
    for y in range(8):
      for x in range(8):
        pyxel.images[0].pset(8 + x, y, int(g_data_a[y][x], 16))
        pyxel.images[0].pset(16 + x, y, int(g_data_b[y][x], 16))

  def reset(self):
    self.x = 20
    self.y = 100
    self.vx = 0
    self.vy = 0
    self.width = 8
    self.height = 12
    self.is_grounded = False
    self.facing_right = True

    self.camera_x = 0
    self.world_width = 600

    self.coins = [80, 96, 112, 200, 216, 320, 336]
    self.score = 0
    self.game_over = False
    self.game_won = False

    # Instantiate Goombas along safe floor intervals
    self.enemies = [
      Goomba(180, 136),
      Goomba(290, 136),
      Goomba(420, 136)
    ]

    self.map_grid = {}
    for col in range(0, self.world_width // 8):
      self.map_grid[(col, 18)] = TILE_FLOOR
      self.map_grid[(col, 19)] = TILE_FLOOR
      # Pits
      if col in [30, 31, 32, 55, 56]:
        self.map_grid[(col, 18)] = TILE_EMPTY
        self.map_grid[(col, 19)] = TILE_EMPTY
      # Floating blocks
      if col in [15, 16, 17, 18, 40, 41, 42]:
        self.map_grid[(col, 12)] = TILE_BLOCK

  def get_tile(self, world_x, world_y):
    grid_x = int(world_x // 8)
    grid_y = int(world_y // 8)
    return self.map_grid.get((grid_x, grid_y), TILE_EMPTY)

  def check_collision(self, next_x, next_y):
    points = [
      (next_x, next_y),
      (next_x + self.width - 1, next_y),
      (next_x, next_y + self.height - 1),
      (next_x + self.width - 1, next_y + self.height - 1)
    ]
    for px, py in points:
      if self.get_tile(px, py) in [TILE_FLOOR, TILE_BLOCK]:
        return True
    return False

  def update(self):
    if self.game_over or self.game_won:
      if pyxel.btnp(pyxel.KEY_R):
        self.reset()
      return

    # Horizontal Inputs
    self.vx = 0
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
      self.vx = -PLAYER_SPEED
      self.facing_right = False
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
      self.vx = PLAYER_SPEED
      self.facing_right = True

    # Gravity simulation
    self.vy += GRAVITY
    if self.vy > MAX_FALL_SPEED:
      self.vy = MAX_FALL_SPEED

    # Jump processing
    if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_SPACE)) and self.is_grounded:
      self.vy = JUMP_STRENGTH
      self.is_grounded = False

    # Apply Horizontal displacement
    if not self.check_collision(self.x + self.vx, self.y):
      self.x += self.vx
    else:
      self.vx = 0

    # Apply Vertical displacement
    if not self.check_collision(self.x, self.y + self.vy):
      self.y += self.vy
      self.is_grounded = False
    else:
      if self.vy > 0:
        self.is_grounded = True
      self.vy = 0

    # Camera tracking interpolation limits
    self.camera_x = self.x - SCREEN_WIDTH // 2
    if self.camera_x < 0: self.camera_x = 0
    if self.camera_x > self.world_width - SCREEN_WIDTH: self.camera_x = self.world_width - SCREEN_WIDTH

    # Update Enemies and Process Combat/Stomp Logic
    for enemy in self.enemies:
      if not enemy.is_alive:
        continue
      enemy.update(self)

      if (self.x < enemy.x + enemy.width and self.x + self.width > enemy.x and
          self.y < enemy.y + enemy.height and self.y + self.height > enemy.y):

        if self.vy > 0 and self.y + self.height - self.vy <= enemy.y + 3:
          enemy.is_alive = False
          self.vy = JUMP_STRENGTH * 0.7
          self.score += 5
        else:
          self.game_over = True

    # Parse Coins Collection
    for coin_x in self.coins[:]:
      if (self.x < coin_x + 6 and self.x + self.width > coin_x and
          self.y < 100 + 6 and self.y + self.height > 100):
        self.score += 1
        self.coins.remove(coin_x)

    if self.y > SCREEN_HEIGHT:
      self.game_over = True

    if self.x >= self.world_width - 24:
      self.game_won = True

  def draw(self):
    pyxel.camera(self.camera_x, 0)

    # Render static levels map tiles
    start_col = int(self.camera_x // 8)
    end_col = int((self.camera_x + SCREEN_WIDTH) // 8) + 1
    for col in range(start_col, end_col):
      for row in range(0, 20):
        tile = self.map_grid.get((col, row), TILE_EMPTY)
        if tile == TILE_FLOOR:
          pyxel.rect(col * 8, row * 8, 8, 8, 4)
        elif tile == TILE_BLOCK:
          pyxel.rect(col * 8, row * 8, 8, 8, 9)

    # Castle Goal elements
    pyxel.rect(self.world_width - 24, 40, 2, 104, 7)
    pyxel.rect(self.world_width - 22, 42, 10, 8, 8)

    for coin_x in self.coins:
      pyxel.circ(coin_x + 3, 100 + 3, 3, 10)

    # Draw moving enemies
    for enemy in self.enemies:
      enemy.draw()

    # Draw Pixel-Art Player from Image Memory Bank 0
    p_w = self.width if self.facing_right else -self.width
    pyxel.blt(self.x, self.y, 0, 0, 0, p_w, self.height, 0)

    # Re-normalize view UI strings
    pyxel.camera(0, 0)
    pyxel.text(4, 4, f"SCORE: {self.score}", 7)

    if self.game_won:
      pyxel.rect(30, 60, 100, 40, 0)
      pyxel.text(62, 70, "STAGE CLEAR!", 11)
      pyxel.text(46, 85, "R to Play Again", 7)
    elif self.game_over:
      pyxel.rect(30, 60, 100, 40, 0)
      pyxel.text(65, 70, "GAME OVER", 8)
      pyxel.text(46, 85, "R to Play Again", 7)

