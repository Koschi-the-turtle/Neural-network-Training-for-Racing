import pygame
import math
import time
import random
pygame.init()
pygame.mixer.init()

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, Tleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=Tleft).center)
    win.blit(rotated_image, new_rect.topleft)

FONT  = pygame.font.SysFont("Gadugi", 18)
FONT2 = pygame.font.SysFont("Gadugi", 28)
FONT3 = pygame.font.SysFont("Comis Sans MS", 22)
PINK   = (255, 150, 235)
GREEN  = (70, 255, 200)
YELLOW = (255, 230, 50)
WHITE  = (255, 245, 250)
DARK   = (10, 5, 10)

# assets
TRACK          = scale_image(pygame.image.load("environment/track.png"), 1.5)
PLAYABLE_LIMIT = scale_image(pygame.image.load("environment/playable-border.png"), 1.5)
PLAYABLE_LIMIT_MASK = pygame.mask.from_surface(PLAYABLE_LIMIT)
TRACK_LIMIT    = scale_image(pygame.image.load("environment/track-border.png"), 1.5)
TRACK_LIMIT_MASK = pygame.mask.from_surface(TRACK_LIMIT)
FINISH         = pygame.transform.rotate(pygame.image.load("environment/finish.png"), 65)
FINISH_MASK    = pygame.mask.from_surface(FINISH)
FINISH_POS     = (556, 410)

TREES   = pygame.image.load("environment/trees.png")
LAKE    = pygame.transform.rotate(pygame.image.load("environment/lake.png"), 20)
FIELD   = scale_image(pygame.image.load("environment/field.png"), 0.3)
COUNTER = pygame.transform.rotate(pygame.image.load("environment/counter.png"), -30)
MENUBG  = scale_image(pygame.image.load("environment/menu_background.png"), 1.5)

# checkpoints defined as line segments (p1, p2)
CHECKPOINTS = [
    ((325, 155), (355, 195)),   # 1
    ((278, 470), (295, 420)),   # 2
    ((140, 210), (110, 170)),   # 3
    ((820, 210), (830, 170)), # 4
]

# tank images (and other types of misceleanous vehicles lol)
KPFPZ70  = scale_image(pygame.image.load("tanks/KpfPz-70.png"),         0.08)
TIGERH1  = scale_image(pygame.image.load("tanks/TigerH1.png"),          0.08)
M48A1    = scale_image(pygame.image.load("tanks/M48A1-Pitbull.png"),    0.08)
M1ABRAMS = scale_image(pygame.image.load("tanks/M1-Abrams.png"),        0.08)
M4SHERMAN= scale_image(pygame.image.load("tanks/M4Sherman.png"),        0.08)
DAVINCI  = scale_image(pygame.image.load("tanks/DaVinciConcept.png"),   0.08)
TIGER2   = scale_image(pygame.image.load("tanks/TigerII.png"),          0.08)
T62      = scale_image(pygame.image.load("tanks/T-62.png"),             0.08)
MAUS     = scale_image(pygame.image.load("tanks/Maus.png"),             0.09)
PANZERIV = scale_image(pygame.image.load("tanks/PanzerIV.png"),         0.08)
THOMAS   = scale_image(pygame.image.load("tanks/Thomas.png"),           0.08)
LEOPARD1 = scale_image(pygame.image.load("tanks/Leopard1.png"),         0.08)
T90A     = scale_image(pygame.image.load("tanks/T-90A.png"),            0.08)
LEOPARD2 = scale_image(pygame.image.load("tanks/Leopard2.png"),         0.08)
MULTIPLA = scale_image(pygame.image.load("tanks/1000tipla.png"),        0.08)

# preview images
KPFPZPREVIEW   = scale_image(pygame.image.load("preview/KpfPz-70preview.png"),        0.6)
TIGERH1PREVIEW = scale_image(pygame.image.load("preview/Tiger H1preview.png"),        0.6)
M48A1PREVIEW   = scale_image(pygame.image.load("preview/M48-A1preview.png"),          0.6)
M1ABRAMSPREVIEW= scale_image(pygame.image.load("preview/M1-Abramspreview.png"),       0.6)
M4SHERMANPREVIEW=scale_image(pygame.image.load("preview/M4 Shermanpreview.png"),      0.6)
DAVINVIPREVIEW = scale_image(pygame.image.load("preview/Da Vinci conceptpreview.png"),0.6)
TIGER2PREVIEW  = scale_image(pygame.image.load("preview/Tiger IIpreview.png"),        0.6)
T62PREVIEW     = scale_image(pygame.image.load("preview/T-62preview.png"),            0.6)
MAUSPREVIEW    = scale_image(pygame.image.load("preview/Mauspreview.png"),            0.6)
PANZERIVPREVIEW= scale_image(pygame.image.load("preview/Panzer IVpreview.png"),       0.6)
THOMASPREVIEW  = scale_image(pygame.image.load("preview/Thomaspreview.png"),          0.6)
LEOPARD1PREVIEW= scale_image(pygame.image.load("preview/Leopard1preview.png"),        0.6)
T90APREVIEW    = scale_image(pygame.image.load("preview/T-90Apreview.png"),           0.6)
LEOPARD2PREVIEW= scale_image(pygame.image.load("preview/Leopard2preview.png"),        0.6)
MULTIPLAPREVIEW= scale_image(pygame.image.load("preview/1000tiplapreview.png"),       0.6)

# window
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kawaii Tank Miniature!")

FPS   = 90
clock = pygame.time.Clock()

# game states
STATE_MENU          = "menu"
STATE_GAME          = "game"
STATE_TRAINING_INIT = "training_init"  # draws the screen first, then starts
STATE_TRAINING      = "training"
STATE_AI_WATCH      = "ai_watch"

game_state   = STATE_MENU
selected_tank = 0
player        = None
best_nn       = None
show_checkpoints = False

TANKS = [
    {"name": "KpfPz-70",         "img": KPFPZPREVIEW,    "imgmini": KPFPZ70  },
    {"name": "Tiger H1",          "img": TIGERH1PREVIEW,  "imgmini": TIGERH1  },
    {"name": "M48 A1",            "img": M48A1PREVIEW,    "imgmini": M48A1    },
    {"name": "M1 Abrams",         "img": M1ABRAMSPREVIEW, "imgmini": M1ABRAMS },
    {"name": "M4 Sherman",        "img": M4SHERMANPREVIEW,"imgmini": M4SHERMAN},
    {"name": "Da Vinci's concept","img": DAVINVIPREVIEW,  "imgmini": DAVINCI  },
    {"name": "Tiger 2",           "img": TIGER2PREVIEW,   "imgmini": TIGER2   },
    {"name": "T-62",              "img": T62PREVIEW,       "imgmini": T62      },
    {"name": "Maus",              "img": MAUSPREVIEW,      "imgmini": MAUS     },
    {"name": "Panzer IV",         "img": PANZERIVPREVIEW, "imgmini": PANZERIV },
    {"name": "Thomas the train",  "img": THOMASPREVIEW,   "imgmini": THOMAS   },
    {"name": "Leopard 1",         "img": LEOPARD1PREVIEW, "imgmini": LEOPARD1 },
    {"name": "T-90 A",            "img": T90APREVIEW,     "imgmini": T90A     },
    {"name": "Leopard 2",         "img": LEOPARD2PREVIEW, "imgmini": LEOPARD2 },
    {"name": "1000tipla",         "img": MULTIPLAPREVIEW, "imgmini": MULTIPLA },
]


# tank classes
class AbstractTank:
    IMG = M48A1

    def __init__(self, vmax, vrotation, start_pos):
        self.img        = self.IMG
        self.vmax       = vmax
        self.v          = 0
        self.vrotation  = vrotation
        self.angle      = 65
        self.x, self.y  = start_pos
        self.acceleration = 0.12
        self.last_bounce_sound = 0
        self.bounce_cooldown = 0

    def rotate(self, left=False, right=False, amount=None):
        if amount is not None:
            self.angle += amount
        else:
            if left:  self.angle += self.vrotation
            if right: self.angle -= self.vrotation

    def move(self):
        if self.bounce_cooldown > 0:
            self.bounce_cooldown -= 1
        rad = math.radians(self.angle)
        self.x -= math.sin(rad) * self.v
        self.y -= math.cos(rad) * self.v

    def undo_move(self):
        """Step back exactly one move — call before bounce so tank exits the wall."""
        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.v
        self.y += math.cos(rad) * self.v

    # Speed-change methods: adjust self.v only, never call move() themselves.
    # move() is called exactly once per frame by the game loop after all inputs.
    def accelerate(self):
        if self.bounce_cooldown > 0:
            return   # can't accelerate while still bouncing away
        self.v = min(self.v + self.acceleration, self.vmax)

    def forward(self):
        self.accelerate()

    def braking(self):
        if self.bounce_cooldown > 0:
            return
        self.v = max(self.v - self.acceleration / 1.5, -self.vmax * 0.5)

    def reduce_speed(self):
        if self.v > 0:
            self.v = max(self.v - self.acceleration / 10, 0)
        elif self.v < 0:
            self.v = min(self.v + self.acceleration / 10, 0)

    def bounce(self):
        self.undo_move()
        # guarantee a meaningful pushback regardless of incoming speed
        MIN_BOUNCE = 1.5
        self.v = -self.v * 0.6
        if abs(self.v) < MIN_BOUNCE:
            self.v = -MIN_BOUNCE if self.v <= 0 else MIN_BOUNCE
        self.bounce_cooldown = 18   # ~0.2s at 90fps — tank coasts away before re-accel
        self.move()
        self.nya_until = time.time() + 0.5
        now = time.time()
        if now - self.last_bounce_sound > 0.1:
            self.last_bounce_sound = now

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def collide(self, mask, x=0, y=0):
        tank_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        return mask.overlap(tank_mask, offset)

    def fully_on_mask(self, mask, tolerance=0.85):
        tank_mask = pygame.mask.from_surface(self.img)
        overlap = mask.overlap_mask(tank_mask, (int(self.x), int(self.y)))
        return overlap.count() / tank_mask.count() >= tolerance

    def out_of_bounds(self):
        """True if the tank has escaped through a hole into totally off-map space.
        Uses the playable-area mask — if almost none of the tank overlaps the
        playable surface, it has gone somewhere it shouldn't be."""
        tank_mask = pygame.mask.from_surface(self.img)
        overlap = PLAYABLE_LIMIT_MASK.overlap_mask(tank_mask, (int(self.x), int(self.y)))
        # overlap here means pixels that are BOTH on the playable surface AND the tank
        # if that's nearly zero the tank is off the mat entirely
        return overlap.count() / tank_mask.count() < 0.1


class PlayerTank(AbstractTank):
    def __init__(self):
        super().__init__(3.2, 3.0, (603, 380))
        self.lap              = 0
        self.next_checkpoint  = 0
        self.on_zone          = False
        self.lap_start_time   = time.time()
        self.sector_start_time= time.time()
        self.current_sectors  = []
        self.best_sectors     = []
        self.last_lap_time    = None
        self.best_lap_time    = None
        self.timer_flash_color= WHITE
        self.timer_flash_until= 0
        self.nya_until        = time.time() - 1
        self.last_bounce_sound= 0
        self.sector_sound_played = False

class PlayerTankCustom(PlayerTank):
    def __init__(self, tank):
        super().__init__()
        self.img = tank["imgmini"]


# AI stuff
START_POS   = (603, 380)
MAX_STEPS   = 4050  # if I ain't straight up autistic that's equal to 45 seconds at 90fps, should be enough for a whole lap
POP_SIZE    = 80
GENERATIONS = 40
SURVIVORS   = 8

# raycasts (somehow that works so don't touch)
def raycast_distance(x, y, angle, mask, max_dist=140):
    rad = math.radians(angle)
    cx  = x + 10   # approximate centre of tank sprite
    cy  = y + 10
    for d in range(0, max_dist, 3):
        px = int(cx - math.sin(rad) * d)
        py = int(cy - math.cos(rad) * d)
        if px < 0 or py < 0 or px >= WIDTH or py >= HEIGHT:
            return d / max_dist
        if mask.get_at((px, py)):
            return d / max_dist
    return 1.0


# Neural Network (also don't touch)
N_IN, N_HID, N_OUT = 10, 14, 2

class NeuralNetwork:
    def __init__(self, weights=None):
        if weights is None:
            self.w1 = [[random.uniform(-1, 1) for _ in range(N_IN)]  for _ in range(N_HID)]
            self.b1 = [random.uniform(-1, 1) for _ in range(N_HID)]
            self.w2 = [[random.uniform(-1, 1) for _ in range(N_HID)] for _ in range(N_OUT)]
            self.b2 = [random.uniform(-1, 1) for _ in range(N_OUT)]
        else:
            self.w1, self.b1, self.w2, self.b2 = weights

    def forward(self, inputs):
        # hidden layer
        h = []
        for i in range(N_HID):
            s = self.b1[i] + sum(self.w1[i][j] * inputs[j] for j in range(N_IN))
            h.append(math.tanh(s))
        # output layer
        out = []
        for i in range(N_OUT):
            s = self.b2[i] + sum(self.w2[i][j] * h[j] for j in range(N_HID))
            out.append(math.tanh(s))

        steer    = out[0]               # [-1, 1]
        throttle = (out[1] + 1) / 2    # [ 0, 1]
        return steer, throttle

    def mutate(self, rate=0.12):
        def m(x): return x + random.gauss(0, 0.4) if random.random() < rate else x
        self.w1 = [[m(x) for x in row] for row in self.w1]
        self.b1 = [m(x) for x in self.b1]
        self.w2 = [[m(x) for x in row] for row in self.w2]
        self.b2 = [m(x) for x in self.b2]

    def crossover(self, other):
        """Uniform crossover — each weight independently from either parent."""
        def cx(a, b): return a if random.random() < 0.5 else b
        child = self.clone()
        child.w1 = [[cx(self.w1[i][j], other.w1[i][j]) for j in range(N_IN)]  for i in range(N_HID)]
        child.b1 = [cx(self.b1[i], other.b1[i]) for i in range(N_HID)]
        child.w2 = [[cx(self.w2[i][j], other.w2[i][j]) for j in range(N_HID)] for i in range(N_OUT)]
        child.b2 = [cx(self.b2[i], other.b2[i]) for i in range(N_OUT)]
        return child

    def clone(self):
        return NeuralNetwork((
            [row[:] for row in self.w1],
            self.b1[:],
            [row[:] for row in self.w2],
            self.b2[:]
        ))


class SimulatedTank(AbstractTank):
    def __init__(self):
        super().__init__(vmax=3.2, vrotation=3.0, start_pos=START_POS)


def _build_inputs(tank, cp_index):
    """Build the neural network input vector.
    Raycasts return 0.0 = wall right here, 1.0 = wall far away (or none).
    We pass them directly so LOW values = danger signal the network can react to.
    """
    cx = tank.x + tank.img.get_width()  // 2
    cy = tank.y + tank.img.get_height() // 2

    front  = raycast_distance(cx, cy, tank.angle,       TRACK_LIMIT_MASK)
    fl     = raycast_distance(cx, cy, tank.angle + 30,  TRACK_LIMIT_MASK)
    fr     = raycast_distance(cx, cy, tank.angle - 30,  TRACK_LIMIT_MASK)
    fl2    = raycast_distance(cx, cy, tank.angle + 60,  TRACK_LIMIT_MASK)
    fr2    = raycast_distance(cx, cy, tank.angle - 60,  TRACK_LIMIT_MASK)
    left   = raycast_distance(cx, cy, tank.angle + 90,  TRACK_LIMIT_MASK)
    right  = raycast_distance(cx, cy, tank.angle - 90,  TRACK_LIMIT_MASK)

    if cp_index < len(CHECKPOINTS):
        p1, p2    = CHECKPOINTS[cp_index]
        tx, ty    = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        dx, dy    = tx - cx, ty - cy
        desired   = math.degrees(math.atan2(dx, -dy))
        angle_err = ((desired - tank.angle + 180) % 360 - 180) / 180
        dist      = min(math.hypot(dx, dy) / 600, 1.0)
    else:
        angle_err, dist = 0.0, 0.0

    speed = tank.v / tank.vmax

    # 10 inputs total: 7 rays + angle to checkpoint + dist to checkpoint + speed
    return [front, fl, fr, fl2, fr2, left, right, angle_err, dist, speed]


def simulate_network(nn):
    tank    = SimulatedTank()
    cp      = 0
    fitness = 0.0

    total_collisions = 0
    steps_since_cp   = 0
    CP_TIMEOUT       = int(FPS * 20)
    MAX_COLLISIONS   = 8

    def cp_midpoint(i):
        p1, p2 = CHECKPOINTS[i]
        return (p1[0]+p2[0])/2, (p1[1]+p2[1])/2

    mx, my    = cp_midpoint(0)
    best_dist = math.hypot(mx - tank.x, my - tank.y)

    for step in range(MAX_STEPS):

        inputs = _build_inputs(tank, cp)
        steer, throttle = nn.forward(inputs)

        tank.rotate(amount=steer * tank.vrotation)
        if throttle > 0.3:
            tank.forward()
        else:
            tank.reduce_speed()
        tank.move()

        # wall / bounds
        if tank.out_of_bounds():
            fitness -= 5000
            break

        if tank.fully_on_mask(TRACK_LIMIT_MASK):
            tank.bounce()
            total_collisions += 1
            fitness -= 200
            if total_collisions > MAX_COLLISIONS:
                break

        # progress reward only while moving forward
        if tank.v > 0 and cp < len(CHECKPOINTS):
            mx, my   = cp_midpoint(cp)
            dist_now = math.hypot(mx - tank.x, my - tank.y)
            if dist_now < best_dist:
                fitness   += (best_dist - dist_now) * 4.0
                best_dist  = dist_now

        fitness += max(tank.v, 0) * 0.15

        steps_since_cp += 1
        if steps_since_cp > CP_TIMEOUT:
            fitness -= 3000
            break

        # checkpoint
        if cp < len(CHECKPOINTS):
            p1, p2 = CHECKPOINTS[cp]
            if tank_crosses_line(tank, p1, p2):
                fitness       += 3000
                cp            += 1
                steps_since_cp = 0
                if cp < len(CHECKPOINTS):
                    mx, my    = cp_midpoint(cp)
                    best_dist = math.hypot(mx - tank.x, my - tank.y)
                else:
                    fx, fy    = FINISH_POS[0] + 30, FINISH_POS[1] + 30
                    best_dist = math.hypot(fx - tank.x, fy - tank.y)
                    fitness  += 3000

        # finish line only valid after ALL checkpoints, line cross only
        # Using tank_crosses_line against a synthetic finish segment to avoid
        # the start-position false-positive from mask overlap.
        if cp == len(CHECKPOINTS) and cp > 0:
            # Build a line segment from FINISH_MASK position approximation
            finish_p1 = (FINISH_POS[0],      FINISH_POS[1] + 60)
            finish_p2 = (FINISH_POS[0] + 60, FINISH_POS[1])
            if tank.v > 0 and cp == len(CHECKPOINTS):
                fx, fy   = FINISH_POS[0] + 30, FINISH_POS[1] + 30
                dist_fin = math.hypot(fx - tank.x, fy - tank.y)
                if dist_fin < best_dist:
                    fitness   += (best_dist - dist_fin) * 4.0
                    best_dist  = dist_fin
            if tank_crosses_line(tank, finish_p1, finish_p2):
                fitness += 15000
                break

    return fitness


# Generational algorithm
training_log = []   # list of (gen, best_fitness) shown on screen

def train_ai():
    """Run the GA; yields progress info by updating training_log."""
    global training_log
    training_log = []

    population = [NeuralNetwork() for _ in range(POP_SIZE)]

    for gen in range(GENERATIONS):

        scored = []
        for nn in population:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            scored.append((simulate_network(nn), nn))
        scored.sort(key=lambda x: x[0], reverse=True)

        best_fitness = scored[0][0]
        training_log.append((gen, best_fitness))
        print(f"Gen {gen+1}/{GENERATIONS} | Best fitness: {best_fitness:.1f}")

        _draw_training_screen(gen, best_fitness)

        survivors  = [nn for _, nn in scored[:SURVIVORS]]
        best_score = scored[0][0]

        # Always keep the single best network completely unchanged (true elitism)
        population = [scored[0][1].clone()]

        # Fill rest with crossover + mutation
        # Weight selection toward higher-ranked survivors
        weights = [SURVIVORS - i for i in range(SURVIVORS)]  # rank-based weights

        while len(population) < POP_SIZE:
            parent_a = random.choices(survivors, weights=weights, k=1)[0]
            parent_b = random.choices(survivors, weights=weights, k=1)[0]
            if parent_a is not parent_b:
                child = parent_a.crossover(parent_b)
            else:
                child = parent_a.clone()
            # adaptive mutation: mutate more aggressively if progress has stalled
            stale = len(training_log) > 5 and all(
                abs(training_log[-i][1] - best_score) < 50
                for i in range(1, 6)
            )
            child.mutate(rate=0.20 if stale else 0.12)
            population.append(child)

    return max(population, key=simulate_network)


def _draw_training_screen(gen, best_fitness):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    WIN.fill(DARK)
    title = FONT2.render("Training AI…", True, PINK)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    if gen == -1:
        msg = FONT.render("Preparing…", True, WHITE)
        WIN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 160))
        pygame.display.update()
        return

    prog = FONT.render(f"Generation  {gen + 1} / {GENERATIONS}", True, WHITE)
    WIN.blit(prog, (WIDTH // 2 - prog.get_width() // 2, 140))

    fit = FONT.render(f"Best fitness: {best_fitness:.1f}", True, GREEN)
    WIN.blit(fit, (WIDTH // 2 - fit.get_width() // 2, 175))

    bar_w = int((gen + 1) / GENERATIONS * 400)
    pygame.draw.rect(WIN, (60, 60, 60), (WIDTH // 2 - 200, 220, 400, 20))
    pygame.draw.rect(WIN, GREEN,        (WIDTH // 2 - 200, 220, bar_w, 20))

    y = 270
    for g, f in training_log[-8:]:
        line = FONT.render(f"  gen {g+1:2d}  →  {f:.0f}", True, YELLOW)
        WIN.blit(line, (WIDTH // 2 - 100, y))
        y += 22

    hint = FONT.render("please wait…", True, (150, 150, 150))
    WIN.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 60))

    pygame.display.update()


# AI movements/inputs
def move_ai(tank, nn):
    inputs = _build_inputs(tank, tank.next_checkpoint)
    steer, throttle = nn.forward(inputs)
    tank.rotate(amount=steer * tank.vrotation)
    if throttle > 0.3:
        tank.forward()
    else:
        tank.reduce_speed()

def handle_menu_input():
    global selected_tank, game_state, player, best_nn

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        selected_tank = (selected_tank - 1) % len(TANKS)
        pygame.time.wait(150)
    if keys[pygame.K_RIGHT]:
        selected_tank = (selected_tank + 1) % len(TANKS)
        pygame.time.wait(150)
    if keys[pygame.K_RETURN]:
        t      = TANKS[selected_tank]
        player = PlayerTankCustom(t)
        game_state = STATE_GAME
    if keys[pygame.K_t]:
        game_state = STATE_TRAINING_INIT


def move_player(tank):
    keys  = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  tank.rotate(left=True)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: tank.rotate(right=True)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        moved = True; tank.forward()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        moved = True; tank.braking()
    if not moved:
        tank.reduce_speed()


# Drawing stuff
def draw_ray(win, x, y, angle, length, color):
    rad   = math.radians(angle)
    end_x = x - math.sin(rad) * length
    end_y = y - math.cos(rad) * length
    pygame.draw.line(win, color, (x, y), (end_x, end_y), 2)


def draw_menu(win):
    win.blit(MENUBG, (-15, 0))
    t = TANKS[selected_tank]

    preview = scale_image(t["img"], 1)
    win.blit(preview, (WIDTH // 2 - 180, 130))

    title = FONT2.render("select your tank!", True, (70, 240, 170))
    win.blit(title, (WIDTH // 2 - title.get_width() // 2, 90))

    name = FONT2.render(t["name"], True, PINK)
    win.blit(name, (WIDTH // 2 - name.get_width() // 2 + 10, 340))

    hint = FONT.render("< / >  switch tank   |   ENTER  play   |   T  train AI", True, (240, 190, 70))
    win.blit(hint, (WIDTH // 2 - hint.get_width() // 2 + 10, 400))

    if best_nn is not None:
        ai_hint = FONT.render("AI is trained!  press W then ENTER to watch it race", True, GREEN)
        win.blit(ai_hint, (WIDTH // 2 - ai_hint.get_width() // 2, 440))

    pygame.display.update()


def draw_timer(win, tank):
    now      = time.time()
    lap_time = now - tank.lap_start_time
    minutes  = int(lap_time // 60)
    seconds  = lap_time % 60
    text     = f"{minutes:02d}:{seconds:06.3f}"
    color    = tank.timer_flash_color if now < tank.timer_flash_until else WHITE
    surf     = FONT2.render(text, True, color)
    rect     = surf.get_rect(topright=(WIDTH - 20, 10))
    win.blit(surf, rect)


def draw(win, tank):
    shake_x = random.randint(-2, 2) if tank.last_bounce_sound > time.time() - 0.1 else 0
    shake_y = random.randint(-2, 2) if tank.last_bounce_sound > time.time() - 0.1 else 0

    win.blit(TRACK,       (shake_x, shake_y))
    win.blit(FINISH,      FINISH_POS)
    win.blit(TRACK_LIMIT, (0, 0))
    win.blit(TREES,       (800, 380))
    win.blit(LAKE,        (-77, 310))
    pygame.draw.rect(win, DARK,  (5, 5, 140, 140))
    pygame.draw.rect(win, WHITE, (5, 5, 140, 140), 2)
    pygame.draw.rect(win, DARK,  (810, 10, 920, 40))
    win.blit(FIELD,   (100, 70))
    draw_timer(win, tank)
    pygame.draw.rect(win, WHITE, (810, 10, 200, 40), 2)
    win.blit(COUNTER, (775, 20))

    # draw rays from tank centre
    cx = tank.x + tank.img.get_width()  // 2
    cy = tank.y + tank.img.get_height() // 2

    ray_angles = [tank.angle, tank.angle+30, tank.angle-30,
                  tank.angle+60, tank.angle-60, tank.angle+90, tank.angle-90]
    ray_colors = [(0,255,0),(0,220,255),(255,220,0),
                  (0,150,255),(255,150,0),(180,100,255),(255,100,180)]
    for ang, col in zip(ray_angles, ray_colors):
        length = raycast_distance(tank.x, tank.y, ang, TRACK_LIMIT_MASK) * 140
        draw_ray(win, cx, cy, ang, length, col)

    if time.time() < tank.nya_until:
        txt = FONT3.render("NYA~!", True, PINK)
        win.blit(txt, (tank.x + 35, tank.y - 15))

    tank.draw(win)

    y = 6
    if tank.last_lap_time is not None:
        txt = FONT.render(f"Last lap: {tank.last_lap_time:.2f}s", True, WHITE)
        win.blit(txt, (10, y)); y += 22
    if tank.best_lap_time is not None:
        txt = FONT.render(f"Best lap: {tank.best_lap_time:.2f}s", True, WHITE)
        win.blit(txt, (10, y)); y += 22

    for i, sector_time in enumerate(tank.current_sectors):
        color = WHITE
        if i < len(tank.best_sectors):
            color = GREEN if sector_time <= tank.best_sectors[i] else YELLOW
        txt = FONT.render(f"S{i+1}: {sector_time:.2f}s", True, color)
        win.blit(txt, (10, y)); y += 22

    fps = FONT.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    win.blit(fps, (WIDTH - fps.get_width() - 10, HEIGHT - 24))

    if game_state == STATE_AI_WATCH:
        lbl = FONT.render("AI DRIVING", True, PINK)
        win.blit(lbl, (WIDTH // 2 - lbl.get_width() // 2, 10))

    if show_checkpoints:
        for i, (p1, p2) in enumerate(CHECKPOINTS):
            pygame.draw.line(win, PINK, p1, p2, 3)
            mid = ((p1[0]+p2[0])//2, (p1[1]+p2[1])//2)
            lbl = FONT2.render(str(i + 1), True, PINK)
            win.blit(lbl, (mid[0] + 4, mid[1] - 14))
        lbl = FONT2.render("F", True, YELLOW)
        win.blit(lbl, (FINISH_POS[0] + 5, FINISH_POS[1] + 5))


def _segments_intersect(p1, p2, p3, p4):
    """Return True if line segment p1-p2 intersects p3-p4."""
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    d1, d2 = cross(p3, p4, p1), cross(p3, p4, p2)
    d3, d4 = cross(p1, p2, p3), cross(p1, p2, p4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return False

def tank_crosses_line(tank, p1, p2):
    """True if the tank's movement vector this frame crossed the checkpoint line
    in the correct direction (determined by which side of the line the tank came from).
    The 'correct' side is defined as: the left-normal of p1→p2 faces the approach.
    We encode the expected approach direction per checkpoint using CHECKPOINT_NORMALS.
    """
    cx = tank.x + tank.img.get_width()  // 2
    cy = tank.y + tank.img.get_height() // 2
    rad = math.radians(tank.angle)
    px  = cx + math.sin(rad) * tank.v
    py  = cy + math.cos(rad) * tank.v

    if not _segments_intersect((px, py), (cx, cy), p1, p2):
        return False

    # Check direction: dot product of tank velocity with the checkpoint's
    # expected crossing normal must be positive.
    # Normal is the left-perpendicular of (p2-p1): (-dy, dx)
    ldx, ldy = p2[0]-p1[0], p2[1]-p1[1]
    nx, ny   = -ldy, ldx   # left-normal of the line

    # Tank velocity direction
    vx = -math.sin(rad) * tank.v
    vy = -math.cos(rad) * tank.v

    return (vx * nx + vy * ny) > 0


# checkpoint logic
def update_checkpoints(tank):
    if tank.next_checkpoint < len(CHECKPOINTS):
        p1, p2 = CHECKPOINTS[tank.next_checkpoint]

        if tank_crosses_line(tank, p1, p2) and not tank.on_zone:
            now         = time.time()
            sector_time = now - tank.sector_start_time
            tank.current_sectors.append(sector_time)

            if len(tank.best_sectors) <= tank.next_checkpoint:
                tank.best_sectors.append(sector_time)
                better = True
            else:
                if sector_time < tank.best_sectors[tank.next_checkpoint]:
                    tank.best_sectors[tank.next_checkpoint] = sector_time
                    better = True
                else:
                    better = False

            tank.timer_flash_color = GREEN if better else YELLOW
            tank.timer_flash_until = now + 0.6

            tank.sector_start_time = now
            tank.next_checkpoint  += 1
            tank.on_zone           = True

    # reset debounce: on_zone clears once the tank has moved away from all lines
    # and the finish. Use a small proximity check instead of mask overlap.
    def near_line(tank, p1, p2, threshold=30):
        cx = tank.x + tank.img.get_width()  // 2
        cy = tank.y + tank.img.get_height() // 2
        # distance from point to segment
        dx, dy = p2[0]-p1[0], p2[1]-p1[1]
        t = max(0, min(1, ((cx-p1[0])*dx + (cy-p1[1])*dy) / (dx*dx+dy*dy+1e-9)))
        nx, ny = p1[0]+t*dx, p1[1]+t*dy
        return math.hypot(cx-nx, cy-ny) < threshold

    touching = any(near_line(tank, p1, p2) for p1, p2 in CHECKPOINTS)
    if not touching and not tank.collide(FINISH_MASK, *FINISH_POS):
        tank.on_zone = False

    # finish line (still uses mask)
    if (tank.collide(FINISH_MASK, *FINISH_POS)
            and tank.next_checkpoint == len(CHECKPOINTS)
            and not tank.on_zone):
        now      = time.time()
        lap_time = now - tank.lap_start_time
        tank.last_lap_time = lap_time
        if tank.best_lap_time is None or lap_time < tank.best_lap_time:
            tank.best_lap_time = lap_time

        tank.lap             += 1
        tank.next_checkpoint  = 0
        tank.current_sectors  = []
        tank.lap_start_time   = now
        tank.sector_start_time= now
        tank.on_zone          = True


# main looooooooooooooooop
player    = PlayerTank()
running   = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                show_checkpoints = not show_checkpoints

    
    if game_state == STATE_TRAINING_INIT:
        # Draw the training screen once so the user sees it immediately,
        # then switch to the real training state next frame.
        _draw_training_screen(-1, 0)
        game_state = STATE_TRAINING

    elif game_state == STATE_TRAINING:
        best_nn = train_ai()
        print("Training complete!")
        player     = PlayerTank()
        game_state = STATE_AI_WATCH

    elif game_state == STATE_MENU:
        draw_menu(WIN)
        handle_menu_input()

    elif game_state == STATE_GAME:
        move_player(player)
        player.move()

        if player.fully_on_mask(TRACK_LIMIT_MASK):
            player.bounce()
        elif player.out_of_bounds():
            player.x, player.y = 603, 380
            player.v = 0

        update_checkpoints(player)
        draw(WIN, player)
        pygame.display.update()

    elif game_state == STATE_AI_WATCH:
        if best_nn is None:
            game_state = STATE_MENU
        else:
            move_ai(player, best_nn)
            player.move()

            if player.fully_on_mask(TRACK_LIMIT_MASK):
                player.bounce()
            elif player.out_of_bounds():
                player.x, player.y = 603, 380
                player.v = 0

            update_checkpoints(player)
            draw(WIN, player)
            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game_state = STATE_MENU

pygame.quit()