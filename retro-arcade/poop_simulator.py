import pyxel
import random
import math
import json
import os

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 160

STATE_LAB = 0
STATE_SHOP = 1

ING_OATS = 1
ING_MILK = 2
ING_CHILI = 4
ING_COFFEE = 8
ING_CHEESE = 16

class Particle:
  def __init__(self, x, y, col, vx, vy):
    self.x = x
    self.y = y
    self.col = col
    self.vx = vx
    self.vy = vy
    self.life = random.randint(20, 45)

  def update(self):
    self.x += self.vx
    self.y += self.vy
    self.vy += 0.1
    self.life -= 1

class PoopSimulator:
  def __init__(self):
    self.init_sprites()
    self.load_profile()

  def init_sprites(self):
    """Programs graphic icons and sprite textures into Pyxel Image Bank 1."""
    pyxel.images[1].set(0, 0, [
      "00777700", "07101070", "71010107", "71010107",
      "71010107", "07101070", "00777700", "00000000"
    ])
    pyxel.images[1].set(8, 0, [
      "00777700", "07000070", "07777770", "07777770",
      "07777770", "07777770", "07777770", "07777770"
    ])
    pyxel.images[1].set(16, 0, [
      "00033000", "00030000", "00888000", "08888800",
      "08888800", "00888800", "00088800", "00008000"
    ])
    pyxel.images[1].set(24, 0, [
      "00777700", "07444477", "07444470", "07444470",
      "00744470", "00777700", "00077000", "00777700"
    ])
    pyxel.images[1].set(32, 0, [
      "00aaaa00", "0aaaaaa0", "aaaaaaaa", "aaaaaaaa",
      "aaaaaaaa", "aaaaaaaa", "0aaaaaa0", "00aaaa00"
    ])

  def load_profile(self):
    """Fetches wallet dollars and log history asynchronously via server bridge."""
    self.poop_dollars = 30
    self.flush_history = []
    try:
      import pyodide.http
      response = pyodide.http.open_url("/load_poop")
      data = json.loads(response.read())
      self.poop_dollars = data.get("dollars", 30)
      self.flush_history = data.get("history", [])
    except:
      try:
        if os.path.exists("data/poop_sim.json"):
          with open("data/poop_sim.json", "r") as f:
            data = json.load(f)
            self.poop_dollars = data.get("dollars", 30)
            self.flush_history = data.get("history", [])
      except: pass
    self.reset()

  def save_profile(self):
    """Saves states securely back to the container storage volume."""
    payload = json.dumps({"dollars": self.poop_dollars, "history": self.flush_history})
    try:
      from js import XMLHttpRequest
      req = XMLHttpRequest.new()
      req.open("POST", "/save_poop", False)
      req.setRequestHeader("Content-Type", "application/json")
      req.send(payload)
    except:
      try:
        if not os.path.exists("data"): os.makedirs("data")
        with open("data/poop_sim.json", "w") as f: f.write(payload)
      except: pass

  def reset(self):
    self.state = STATE_LAB
    self.mixture_mask = 0

    self.unlocked_items = [
      {"name": "OATS", "mask": "OAT", "bit": ING_OATS, "u": 0, "unlocked": True, "cost": 0},
      {"name": "MILK", "mask": "MLK", "bit": ING_MILK, "u": 8, "unlocked": True, "cost": 0},
      {"name": "CHILI", "mask": "CHL", "bit": ING_CHILI, "u": 16, "unlocked": False, "cost": 25},
      {"name": "COFFEE", "mask": "COF", "bit": ING_COFFEE, "u": 24, "unlocked": False, "cost": 40},
      {"name": "CHEESE", "mask": "CHS", "bit": ING_CHEESE, "u": 32, "unlocked": False, "cost": 60}
    ]

    # Restore unlocked inventory items based on your current balance progression
    for item in self.unlocked_items:
      if item["cost"] > 0 and self.poop_dollars < (30 + item["cost"]):
        item["unlocked"] = False
      elif item["cost"] > 0:
        item["unlocked"] = True

    self.selector_index = 0
    self.particles = []

    # Brewing variables
    self.brew_timer = 0
    self.max_brew_time = 45 # Total frames to lock process loops

    self.reaction_color = 4
    self.reaction_speed = 1.0

  def trigger_brew(self):
    """Locks interaction routines and initializes countdown timer states."""
    self.brew_timer = self.max_brew_time

  def process_reaction(self):
    mask = self.mixture_mask
    self.reaction_color = 4
    self.reaction_speed = 1.5
    payout_multiplier = 1

    used_labels = []
    for item in self.unlocked_items:
      if mask & item["bit"]: used_labels.append(item["mask"])
    mix_string = "+".join(used_labels) if used_labels else "NONE"

    if (mask & ING_CHILI) and (mask & ING_CHEESE):
      self.reaction_color = 8
      self.reaction_speed = 4.0
      payout_multiplier = 4
    elif (mask & ING_COFFEE) and (mask & ING_MILK):
      self.reaction_color = 10
      self.reaction_speed = 5.0
      payout_multiplier = 3
    elif (mask & ING_OATS) and (mask & ING_CHEESE):
      self.reaction_color = 13
      self.reaction_speed = 0.5
      payout_multiplier = 2
    elif mask & ING_CHILI:
      self.reaction_color = 9
      self.reaction_speed = 3.0
      payout_multiplier = 2
    elif mask & ING_COFFEE:
      self.reaction_color = 4
      self.reaction_speed = 2.5
      payout_multiplier = 2

    for _ in range(40):
      ang = random.uniform(0.3, 2.8)
      mag = random.uniform(1.0, self.reaction_speed + 1.0)
      self.particles.append(Particle(50, 65, self.reaction_color, math.cos(ang)*mag, math.sin(ang)*mag))

    earned = 10 * payout_multiplier
    self.poop_dollars += earned

    self.flush_history.insert(0, {"mix": mix_string, "cash": earned})
    if len(self.flush_history) > 3: self.flush_history.pop()

    self.mixture_mask = 0
    self.save_profile() # Flush states straight to drive volume links

  def update(self):
    for p in self.particles[:]:
      p.update()
      if p.life <= 0 or p.y > 115: self.particles.remove(p)

    # Manage brewing timers
    if self.brew_timer > 0:
      self.brew_timer -= 1
      if self.brew_timer == 0:
        self.process_reaction()
      return # Freeze all keyboard cursor actions while cooking

    if self.state == STATE_LAB:
      self.update_lab()
    elif self.state == STATE_SHOP:
      self.update_shop()

  def update_lab(self):
    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
      self.selector_index = (self.selector_index - 1) % 7
    elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
      self.selector_index = (self.selector_index + 1) % 7

    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
      if self.selector_index < 5:
        item = self.unlocked_items[self.selector_index]
        if item["unlocked"]: self.mixture_mask ^= item["bit"]
      elif self.selector_index == 5:
        if self.mixture_mask > 0: self.trigger_brew()
      elif self.selector_index == 6:
        self.state = STATE_SHOP
        self.selector_index = 0

  def update_shop(self):
    locked_items = [i for i in self.unlocked_items if not i["unlocked"]]
    total_options = len(locked_items) + 1

    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
      self.selector_index = (self.selector_index - 1) % total_options
    elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
      self.selector_index = (self.selector_index + 1) % total_options

    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
      if self.selector_index < len(locked_items):
        target = locked_items[self.selector_index]
        if self.poop_dollars >= target["cost"]:
          self.poop_dollars -= target["cost"]
          for master in self.unlocked_items:
            if master["name"] == target["name"]: master["unlocked"] = True
          self.save_profile()
          self.selector_index = 0
      else:
        self.state = STATE_LAB
        self.selector_index = 0

  def draw(self):
    if self.state == STATE_LAB:
      self.draw_lab()
    elif self.state == STATE_SHOP:
      self.draw_shop()

  def draw_lab(self):
    pyxel.text(4, 4, f"CASH: ${self.poop_dollars} PP", 11)

    # Cauldron bounding boxes
    pyxel.rectb(15, 35, 75, 30, 13)
    pyxel.rect(16, 36, 73, 28, 1)

    for p in self.particles:
      pyxel.circ(int(p.x), int(p.y), random.randint(1, 2), p.col)

    # Render Animated Progress Bar if actively brewing
    if self.brew_timer > 0:
      progress_width = int(71 * (self.brew_timer / self.max_brew_time))
      pyxel.rect(17, 61, progress_width, 3, 11) # Bright lime green loader line
      pyxel.text(32, 47, "BREWING...", 11)

    # History Ledger columns
    pyxel.text(98, 4, "RECENTS HISTORY:", 7)
    pyxel.line(98, 12, 155, 12, 5)

    if not self.flush_history:
      pyxel.text(98, 18, "No flushes recorded", 5)
    else:
      for idx, history in enumerate(self.flush_history):
        y_pos = 18 + (idx * 16)
        pyxel.text(98, y_pos, history["mix"][:9], 6)
        pyxel.text(98, y_pos + 7, f"Yield: +${history['cash']}", 11)

    # Ingredient Dock Row Layouts
    pyxel.text(4, 85, "TANK INGREDIENTS:", 7)
    for i, item in enumerate(self.unlocked_items):
      x_pos = 6 + (i * 21)
      is_sel = (self.selector_index == i) and (self.brew_timer == 0)

      pyxel.rectb(x_pos, 96, 15, 15, 10 if is_sel else 5)

      if item["unlocked"]:
        pyxel.blt(x_pos + 4, 100, 1, item["u"], 0, 8, 8, 0)
        if self.mixture_mask & item["bit"]: pyxel.rect(x_pos + 1, 97, 3, 3, 11)
        pyxel.text(x_pos + 2, 114, item["mask"], 14 if is_sel else 5)
      else:
        pyxel.text(x_pos + 6, 101, "?", 2)
        pyxel.text(x_pos + 2, 114, "LCK", 2)

    # Command buttons
    is_lever_act = (self.selector_index == 5) and (self.brew_timer == 0)
    is_shop_act = (self.selector_index == 6) and (self.brew_timer == 0)

    pyxel.rect(114, 96, 40, 15, 9 if is_lever_act else (13 if self.brew_timer > 0 else 8))
    pyxel.text(122, 101, "FLUSH", 7)

    pyxel.rect(114, 114, 40, 11, 12 if is_shop_act else 5)
    pyxel.text(122, 117, "MARKET", 7)

  def draw_shop(self):
    pyxel.text(4, 4, "UPGRADES LABORATORY", 10)
    pyxel.text(4, 14, f"Wallet: ${self.poop_dollars} PP", 11)

    locked_items = [i for i in self.unlocked_items if not i["unlocked"]]
    pyxel.text(4, 35, "--- ACQUIRE EXTRA COMPOUNDS ---", 7)
    for i, item in enumerate(locked_items):
      is_sel = (self.selector_index == i)
      pyxel.text(14, 50 + (i * 12), f'{">" if is_sel else ""} UNLOCK {item["name"]}(${item["cost"]})',
                 10 if is_sel else 7)
    idx_exit = len(locked_items)
    is_exit_sel = (self.selector_index == idx_exit)
    pyxel.text(14, 60 + (idx_exit * 12), f'{">" if is_exit_sel else ""}[RETURN TO BIO-LAB]', 8 if is_exit_sel else 5)
    if not locked_items: pyxel.text(15, 80, "MAX REACTION MATRIX UNLOCKED!", 11)
