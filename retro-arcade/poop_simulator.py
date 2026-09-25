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
    """Programs graphic icons and sprite textures into Pyxel Image Banks 0 and 1."""
    # --- BANK 1: INGREDIENT ICONS (8x8 pixels) ---
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

    # --- BANK 0: SIDE PROFILE MAN (16x24 pixels at U:0, V:32) ---
    # Fixed: Swapped color 1 (invisible dark blue) for color 7 (bright white)
    # and color 4 for color 6 (light gray) so the body shape pops off the dark screen.
    man_data = [
      "0000077777000000",
      "0000776767700000",
      "0000776767770000",
      "0000077777770000",
      "0000007777000000",
      "0000777777770000",
      "0007777777777000",
      "0077777777777100",
      "0777777777777770",
      "0777777777777770",
      "7777777777777777",
      "7777777777777777",
      "7777777777777777",
      "7777777777777777",
      "0777777777777770",
      "0777777777777770",
      "0077777777777700",
      "0007777777777000",
      "0000777777770000",
      "0000770000770000",
      "0000770000770000",
      "0000770000770000",
      "0007770007770000",
      "0077770077770000"
    ]

    # Loop over rows to cleanly commit the updated color profile to the canvas layer
    for y, row_string in enumerate(man_data):
      pyxel.images[0].set(0, 32 + y, [row_string])


  def load_profile(self):
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
    for item in self.unlocked_items:
      if item["cost"] > 0 and self.poop_dollars < (30 + item["cost"]):
        item["unlocked"] = False
      elif item["cost"] > 0:
        item["unlocked"] = True
    self.selector_index = 0
    self.particles = []
    self.brew_timer = 0
    self.max_brew_time = 45
    self.reaction_color = 4
    self.reaction_speed = 1.0

  def trigger_brew(self):
    self.brew_timer = self.max_brew_time
    self.particles = []

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
      self.reaction_speed = 4.2
      payout_multiplier = 4
    elif (mask & ING_COFFEE) and (mask & ING_MILK):
      self.reaction_color = 10
      self.reaction_speed = 5.0
      payout_multiplier = 3
    elif (mask & ING_OATS) and (mask & ING_CHEESE):
      self.reaction_color = 13
      self.reaction_speed = 0.6
      payout_multiplier = 2
    elif mask & ING_CHILI:
      self.reaction_color = 9
      self.reaction_speed = 3.2
      payout_multiplier = 2
    elif mask & ING_COFFEE:
      self.reaction_color = 4
      self.reaction_speed = 2.5
      payout_multiplier = 2

    for _ in range(45):
      ang = random.uniform(2.2, 3.8)
      mag = random.uniform(1.2, self.reaction_speed + 1.2)
      self.particles.append(Particle(38, 56, self.reaction_color, math.cos(ang)*mag, math.sin(ang)*mag))

    earned = 10 * payout_multiplier
    self.poop_dollars += earned
    self.flush_history.insert(0, {"mix": mix_string, "cash": earned})
    if len(self.flush_history) > 3: self.flush_history.pop()
    self.mixture_mask = 0
    self.save_profile()

  def update(self):
    for p in self.particles[:]:
      p.update()
      if p.life <= 0 or p.y > 75 or p.x < 16:
        self.particles.remove(p)

    if self.brew_timer > 0:
      self.brew_timer -= 1
      if self.brew_timer == 0:
        self.process_reaction()
      return

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

    # 1. Main Viewing Box Frame
    pyxel.rectb(15, 35, 75, 42, 13)
    pyxel.rect(16, 36, 73, 40, 1) # Dark Blue background color 1

    # Draw any active streaming physics particles trailing outwards
    for p in self.particles:
      pyxel.circ(int(p.x), int(p.y), random.randint(1, 2), p.col)

    man_x = 44
    man_y = 44

    # Determine what reaction color index theme is active
    preview_col = 4
    if (self.mixture_mask & ING_CHILI) and (self.mixture_mask & ING_CHEESE): preview_col = 8
    elif (self.mixture_mask & ING_COFFEE) and (self.mixture_mask & ING_MILK): preview_col = 10
    elif (self.mixture_mask & ING_OATS) and (self.mixture_mask & ING_CHEESE): preview_col = 13
    elif self.mixture_mask & ING_CHILI: preview_col = 9

    # Calculate current filling line threshold (0 to 24 pixels from bottom of head down)
    fill_threshold = 0 if self.brew_timer == 0 else int(24 * (1.0 - (self.brew_timer / self.max_brew_time)))

    # --- 2. PIXEL-PERFECT LAYER STENCIL ENGINE ---
    # Look directly at the sprite pixels on Image Bank 0 (U:0 to 16, V:32 to 56)
    for row_y in range(24):
      for col_x in range(16):
        # Sample the exact pixel on the sprite sheet template
        sprite_pixel = pyxel.images[0].pget(col_x, 32 + row_y)

        if sprite_pixel != 0: # Skip completely transparent spacer pixels
          screen_pixel_x = man_x + col_x
          screen_pixel_y = man_y + row_y

          # Stencil Rule: If it's a solid inner body pixel (color 6 or 7)
          # and sits below our active filling line threshold, fill it with the reaction color!
          if self.brew_timer > 0 and sprite_pixel in [6, 7] and row_y <= fill_threshold:
            pyxel.pset(screen_pixel_x, screen_pixel_y, 11)
          else:
            # Draw standard gray/white shell pixels if empty/unreached
            pyxel.pset(screen_pixel_x, screen_pixel_y, sprite_pixel)

    if self.brew_timer > 0:
      pyxel.text(20, 26, "PROCESSING...", preview_col)

    # 3. Recents History columns
    pyxel.text(98, 4, "RECENTS HISTORY:", 7)
    pyxel.line(98, 12, 155, 12, 5)
    if not self.flush_history:
      pyxel.text(98, 18, "No flushes recorded", 5)
    else:
      for idx, history in enumerate(self.flush_history):
        y_pos = 18 + (idx * 16)
        pyxel.text(98, y_pos, history["mix"][:9], 6)
        pyxel.text(98, y_pos + 7, f"Yield: +${history['cash']}", 11)

    # 4. Dock Row Slots Layout
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

    # 5. Control buttons
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
      pyxel.text(14, 50 + (i * 12), f"{'>' if is_sel else ' '} UNLOCK {item['name']} (${item['cost']})", 10 if is_sel else 7)
      pyxel.blt(120, 48 + (i * 12), 1, item["u"], 0, 8, 8, 0)
    idx_exit = len(locked_items)
    is_exit_sel = (self.selector_index == idx_exit)
    pyxel.text(14, 60 + (idx_exit * 12), f"{'>' if is_exit_sel else ' '} [RETURN TO BIO-LAB]", 8 if is_exit_sel else 5)
    if not locked_items: pyxel.text(15, 80, "MAX REACTION MATRIX UNLOCKED!", 11)
