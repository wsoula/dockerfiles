import pyxel
import random
import math
import json
import os

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 160

# Weapon Profiles
GUN_PISTOL = 0
GUN_SHOTGUN = 1
GUN_MACHINE_GUN = 2

WEAPONS = {
  GUN_PISTOL: {"name": "PISTOL", "cooldown": 12, "damage": 1, "color": 10},
  GUN_SHOTGUN: {"name": "SHOTGUN", "cooldown": 25, "damage": 2, "color": 9},
  GUN_MACHINE_GUN: {"name": "M-GUN", "cooldown": 4, "damage": 1, "color": 8}
}

class Bullet:
  def __init__(self, x, y, dx, dy, damage, color):
    self.x = x
    self.y = y
    self.dx = dx
    self.dy = dy
    self.damage = damage
    self.color = color
    self.lifetime = 50

class Monster:
  def __init__(self, x, y, type_id):
    self.x = x
    self.y = y
    self.type_id = type_id
    self.width = 8
    self.height = 8

    if type_id == 0:
      self.hp = 1
      self.speed = 1.0
      self.color = 3  # Green Runner
    else:
      self.hp = 3
      self.speed = 0.5
      self.color = 2  # Purple Tank

class ShooterEngine:
  def __init__(self):
    # Setup persistent user data directory paths safely
    self.save_dir = pyxel.user_data_dir("Arcade", "Shooter")
    self.save_file = os.path.join(self.save_dir, "save.json")
    self.high_score = self.load_high_score()

    self.init_sprites()
    self.reset()

  def load_high_score(self):
    """Loads high score from local file storage profile folder."""
    try:
      if os.path.exists(self.save_file):
        with open(self.save_file, "r") as f:
          data = json.load(f)
          return data.get("high_score", 0)
    except:
      pass
    return 0

  def save_high_score(self):
    """Saves high score out to storage media securely."""
    try:
      # Ensure data container directory tree paths exist safely
      if not os.path.exists(self.save_dir):
        os.makedirs(self.save_dir)
      with open(self.save_file, "w") as f:
        json.dump({"high_score": self.high_score}, f)
    except:
      pass

  def init_sprites(self):
    p_data = [
      "00999900",
      "09914190",
      "00914100",
      "00121200",
      "01212120",
      "00033000",
      "00300300",
      "01100110"
    ]
    pyxel.images[0].set(0, 0, p_data)

  def reset(self):
    self.px = 80.0
    self.py = 80.0
    self.player_width = 8
    self.player_height = 8
    self.player_hp = 5
    self.score = 0

    self.current_gun = GUN_PISTOL
    self.shoot_cooldown = 0

    self.bullets = []
    self.monsters = []

    self.aim_dx = 0.0
    self.aim_dy = -1.0
    self.is_auto_aiming = False
    self.game_over = False

    # Track overridden forced modifications to clear pathways
    self.cleared_spawns = set()

  def get_obstacle_at(self, tile_x, tile_y):
    """Procedurally determines static grid objects throughout the infinite space."""
    # Never block the initial starting safe zone
    if abs(tile_x - 10) < 5 and abs(tile_y - 10) < 5:
      return False
    # If this specific tile was explicitly cleared for a monster runway, return False
    if (tile_x, tile_y) in self.cleared_spawns:
      return False

    h = (tile_x * 73856093) ^ (tile_y * 19349663)
    return (h % 14) == 0  # Balanced obstruction density

  def check_collision(self, nx, ny):
    """Bounding frame corner checks against procedural map tiles."""
    corners = [
      (nx, ny),
      (nx + 7, ny),
      (nx, ny + 7),
      (nx + 7, ny + 7)
    ]
    for cx, cy in corners:
      tx = int(math.floor(cx / 8))
      ty = int(math.floor(cy / 8))
      if self.get_obstacle_at(tx, ty):
        return True
    return False

  def update(self):
    if self.game_over:
      if pyxel.btnp(pyxel.KEY_R):
        self.reset()
      return

    # Cycle Weapons
    if pyxel.btnp(pyxel.KEY_E):
      self.current_gun = (self.current_gun + 1) % 3
    elif pyxel.btnp(pyxel.KEY_Q):
      self.current_gun = (self.current_gun - 1) % 3

    # Player Movement Tracking Vectors
    vx = 0
    vy = 0
    if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT): vx = -1.2
    if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT): vx = 1.2
    if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP): vy = -1.2
    if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN): vy = 1.2

    if vx != 0 or vy != 0:
      mag = math.sqrt(vx*vx + vy*vy)
      vx = (vx / mag) * 1.2
      vy = (vy / mag) * 1.2
      if not pyxel.btn(pyxel.KEY_LSHIFT):
        self.aim_dx = vx / 1.2
        self.aim_dy = vy / 1.2

    if not self.check_collision(self.px + vx, self.py):
      self.px += vx
    if not self.check_collision(self.px, self.py + vy):
      self.py += vy

    # Target Locking Routine (Auto-Aim)
    self.is_auto_aiming = False
    if pyxel.btn(pyxel.KEY_LSHIFT) and len(self.monsters) > 0:
      closest_monster = None
      min_distance = float('inf')

      for m in self.monsters:
        dist_x = m.x - self.px
        dist_y = m.y - self.py
        actual_dist = math.sqrt(dist_x*dist_x + dist_y*dist_y)
        if actual_dist < min_distance:
          min_distance = actual_dist
          closest_monster = m

      if closest_monster:
        self.is_auto_aiming = True
        angle = math.atan2((closest_monster.y + 4) - (self.py + 4), (closest_monster.x + 4) - (self.px + 4))
        self.aim_dx = math.cos(angle)
        self.aim_dy = math.sin(angle)

    # Spawning System
    if pyxel.frame_count % 30 == 0 and len(self.monsters) < 12:
      side = random.randint(0, 3)
      # Spawn precisely 4 pixels outside the visible layout frame box
      if side == 0:    # Top edge
        mx = random.uniform(self.px - 60, self.px + 100)
        my = self.py - 84
      elif side == 1:  # Bottom edge
        mx = random.uniform(self.px - 60, self.px + 100)
        my = self.py + 84
      elif side == 2:  # Left edge
        mx = self.px - 84
        my = random.uniform(self.py - 60, self.py + 100)
      else:            # Right edge
        mx = self.px + 84
        my = random.uniform(self.py - 60, self.py + 100)

      # Force-clear map tile at spawn spot so enemies don't get trapped inside blocks
      mtx = int(math.floor(mx / 8))
      mty = int(math.floor(my / 8))
      self.cleared_spawns.add((mtx, mty))

      self.monsters.append(Monster(mx, my, random.randint(0, 1)))

    # Shooting mechanics (Accepts Spacebar or F key to clear select latency)
    if self.shoot_cooldown > 0:
      self.shoot_cooldown -= 1

    if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_F)) and self.shoot_cooldown == 0:
      gun = WEAPONS[self.current_gun]
      self.shoot_cooldown = gun["cooldown"]

      if self.current_gun == GUN_SHOTGUN:
        angles = [-0.2, 0.0, 0.2]
        for a in angles:
          sdx = self.aim_dx * math.cos(a) - self.aim_dy * math.sin(a)
          sdy = self.aim_dx * math.sin(a) + self.aim_dy * math.cos(a)
          self.bullets.append(Bullet(self.px + 3, self.py + 3, sdx * 2.5, sdy * 2.5, gun["damage"], gun["color"]))
      else:
        self.bullets.append(Bullet(self.px + 3, self.py + 3, self.aim_dx * 3.0, self.aim_dy * 3.0, gun["damage"], gun["color"]))

    # Update Bullets
    for b in self.bullets[:]:
      b.x += b.dx
      b.y += b.dy
      b.lifetime -= 1
      btx = int(math.floor(b.x / 8))
      bty = int(math.floor(b.y / 8))
      if b.lifetime <= 0 or self.get_obstacle_at(btx, bty):
        if b in self.bullets: self.bullets.remove(b)

    # Update Monsters
    for m in self.monsters[:]:
      mdx = (self.px + 4) - (m.x + 4)
      mdy = (self.py + 4) - (m.y + 4)
      dist = math.sqrt(mdx*mdx + mdy*mdy)

      if dist > 0:
        mvx = (mdx / dist) * m.speed
        mvy = (mdy / dist) * m.speed
        # Step enemies forward; clear obstacles if they manage to get pinched inside a wall
        if not self.check_collision(m.x + mvx, m.y):
          m.x += mvx
        else:
          self.cleared_spawns.add((int(math.floor((m.x+mvx)/8)), int(math.floor(m.y/8))))

        if not self.check_collision(m.x, m.y + mvy):
          m.y += mvy
        else:
          self.cleared_spawns.add((int(math.floor(m.x/8)), int(math.floor((m.y+mvy)/8))))

      # Check Bullet hits
      for b in self.bullets[:]:
        if (b.x >= m.x and b.x <= m.x + 7 and b.y >= m.y and b.y <= m.y + 7):
          m.hp -= b.damage
          if b in self.bullets: self.bullets.remove(b)
          if m.hp <= 0:
            points_earned = 10 if self.is_auto_aiming else 100
            self.score += points_earned
            if self.score > self.high_score:  # Update high score in real-time
              self.high_score = self.score
            if m in self.monsters: self.monsters.remove(m)
            break

      # Damage calculation against player health
      if m.hp > 0 and (self.px < m.x + 8 and self.px + 8 > m.x and self.py < m.y + 8 and self.py + 8 > m.y):
        self.player_hp -= 1
        if m in self.monsters: self.monsters.remove(m)
        if self.player_hp <= 0:
          self.game_over = True
          self.save_high_score() # Save immediately on death

    # Dynamic real-time score fallback tracker
    if self.score > self.high_score:
      self.high_score = self.score

  def draw(self):
    cam_x = int(self.px - SCREEN_WIDTH / 2)
    cam_y = int(self.py - SCREEN_HEIGHT / 2)
    pyxel.camera(cam_x, cam_y)

    # Draw procedural floors
    start_tx = int(math.floor(cam_x / 8))
    end_tx = int(math.floor((cam_x + SCREEN_WIDTH) / 8)) + 1
    start_ty = int(math.floor(cam_y / 8))
    end_ty = int(math.floor((cam_y + SCREEN_HEIGHT) / 8)) + 1

    for tx in range(start_tx, end_tx):
      for ty in range(start_ty, end_ty):
        if self.get_obstacle_at(tx, ty):
          pyxel.rect(tx * 8, ty * 8, 8, 8, 13)
        else:
          if (tx + ty) % 2 == 0:
            pyxel.pset(tx * 8, ty * 8, 5)

    # Target indicator direction line
    line_len = 10
    pyxel.line(self.px + 4, self.py + 4,
               self.px + 4 + self.aim_dx * line_len,
               self.py + 4 + self.aim_dy * line_len,
               9 if self.is_auto_aiming else 7)

    # Draw Bullets
    for b in self.bullets:
      pyxel.rect(int(b.x), int(b.y), 2, 2, b.color)

    # Draw Monsters
    for m in self.monsters:
      pyxel.rect(int(m.x), int(m.y), m.width, m.height, m.color)

    # Draw Player
    pyxel.blt(int(self.px), int(self.py), 0, 0, 0, 8, 8, 0)

    # Clear camera context matrix offsets to stick layout metrics cleanly on screen
    pyxel.camera(0, 0)

    gun_info = WEAPONS[self.current_gun]
    pyxel.text(4, 4, f"GUN: {gun_info['name']} (Q/E)", 7)

    # Render mini-health heads
    pyxel.text(4, 14, "HP:", 7)
    for i in range(max(0, self.player_hp)):
      pyxel.blt(18 + (i * 10), 13, 0, 0, 0, 8, 4, 0)

    pyxel.text(4, 24, "AUTO-AIM: [SHIFT]", 9 if self.is_auto_aiming else 5)

    # Score Panels
    pyxel.text(100, 4, f"SCORE: {self.score}", 7)
    pyxel.text(100, 14, f"BEST: {self.high_score}", 11) # Gold/Green color text

    if self.game_over:
      pyxel.rect(30, 60, 100, 42, 0)
      pyxel.text(62, 70, "WASTELAND DIED", 8)
      if self.score >= self.high_score and self.score > 0:
        pyxel.text(53, 80, "NEW HIGH SCORE!", 10)
      pyxel.text(46, 92, "R to Respawn", 7)

