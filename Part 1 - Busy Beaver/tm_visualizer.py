import sys
import math
import random
import pygame
from turing_machine import TuringMachine
import os

TRANSITIONS = {
    ('A', '0'): ('B', '1', 'R'),
    ('A', '1'): ('Z', '1', 'R'),
    ('B', '0'): ('B', '1', 'L'),
    ('B', '1'): ('C', '0', 'R'),
    ('C', '0'): ('C', '1', 'L'),
    ('C', '1'): ('A', '1', 'L')
}

INPUT_TAPE = ""
START_STATE = 'A'
HALT_STATE = 'Z'
# BLANK = '□'
BLANK = '0'

pygame.init()
pygame.font.init()

pygame.mixer.init()

def generate_beep(freq=700, duration=80):
    sample_rate = 22050
    n = int(sample_rate * duration / 1000)
    buf = bytearray()

    for i in range(n):
        t = i / sample_rate
        val = int(127 * math.sin(2 * math.pi * freq * t) + 128)
        buf.extend([val, val])

    return pygame.mixer.Sound(buffer=bytes(buf))

STEP_SOUND = generate_beep(900, 60)
HALT_SOUND = generate_beep(250, 220)

WIDTH, HEIGHT = 1600, 920
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Neon Glass Turing Machine Visualizer")
CLOCK = pygame.time.Clock()

FONT_TITLE = pygame.font.SysFont("segoeui", 40, bold=True)
FONT_H1 = pygame.font.SysFont("segoeui", 28, bold=True)
FONT_H2 = pygame.font.SysFont("consolas", 24, bold=False)
FONT_BODY = pygame.font.SysFont("consolas", 20)
FONT_SMALL = pygame.font.SysFont("consolas", 16)
FONT_TAPE = pygame.font.SysFont("consolas", 34, bold=True)
FONT_BUTTON = pygame.font.SysFont("segoeui", 20, bold=True)

THEMES = {
    "dark": {
        "bg1": (7, 10, 24),
        "bg2": (17, 24, 50),
        "grid": (100, 120, 180, 28),
        "panel": (24, 28, 46, 185),
        "panel2": (30, 35, 58, 165),
        "border": (130, 190, 255, 90),
        "text": (242, 246, 255),
        "muted": (170, 182, 210),
        "accent": (80, 220, 255),
        "head": (255, 110, 180),
        "zero": (86, 126, 230),
        "one": (90, 240, 165),
        "warn": (255, 120, 120),
        "good": (80, 230, 170),
        "shadow": (0, 0, 0, 120),
        "glass": (255, 255, 255, 30),
    },
    "light": {
        "bg1": (238, 244, 255),
        "bg2": (215, 228, 245),
        "grid": (120, 140, 180, 24),
        "panel": (255, 255, 255, 170),
        "panel2": (248, 251, 255, 190),
        "border": (90, 140, 220, 90),
        "text": (28, 36, 52),
        "muted": (95, 110, 132),
        "accent": (60, 155, 255),
        "head": (255, 110, 150),
        "zero": (118, 152, 235),
        "one": (72, 194, 134),
        "warn": (220, 85, 92),
        "good": (62, 180, 120),
        "shadow": (50, 60, 80, 45),
        "glass": (255, 255, 255, 70),
    }
}

current_theme_name = "dark"

def T():
    return THEMES[current_theme_name]

def lerp(a, b, t):
    return a + (b - a) * t

def clamp(x, a, b):
    return max(a, min(b, x))

def draw_text(surface, s, font, color, pos, center=False):
    img = font.render(s, True, color)
    rect = img.get_rect()
    rect.center = pos if center else rect.center
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(img, rect)
    return rect

def round_rect(surface, rect, color, radius=18, width=0):
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)

def gradient_bg(surface, c1, c2):
    for y in range(surface.get_height()):
        p = y / max(1, surface.get_height() - 1)
        c = (
            int(lerp(c1[0], c2[0], p)),
            int(lerp(c1[1], c2[1], p)),
            int(lerp(c1[2], c2[2], p)),
        )
        pygame.draw.line(surface, c, (0, y), (surface.get_width(), y))

def draw_grid(surface):
    t = T()
    grid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for x in range(0, WIDTH, 42):
        pygame.draw.line(grid, t["grid"], (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 42):
        pygame.draw.line(grid, t["grid"], (0, y), (WIDTH, y), 1)
    surface.blit(grid, (0, 0))

def draw_glow(surface, center, color, radius=60, alpha=90, layers=6):
    glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(layers, 0, -1):
        r = int(radius * i / layers)
        a = int(alpha * ((i / layers) ** 2))
        pygame.draw.circle(glow, (*color, a), (radius, radius), r)
    surface.blit(glow, (center[0] - radius, center[1] - radius), special_flags=pygame.BLEND_PREMULTIPLIED)

def glass_panel(surface, rect, fill_rgba, border_rgba, radius=28, shadow=True):
    if shadow:
        sh = pygame.Surface((rect.width + 32, rect.height + 32), pygame.SRCALPHA)
        round_rect(sh, pygame.Rect(16, 16, rect.width, rect.height), T()["shadow"], radius=radius)
        surface.blit(sh, (rect.x - 16, rect.y - 10))
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    round_rect(panel, pygame.Rect(0, 0, rect.width, rect.height), fill_rgba, radius=radius)
    round_rect(panel, pygame.Rect(0, 0, rect.width, rect.height), border_rgba, radius=radius, width=2)
    gloss = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    round_rect(gloss, pygame.Rect(12, 10, rect.width - 24, 34), T()["glass"], radius=20)
    panel.blit(gloss, (0, 0))
    surface.blit(panel, rect.topleft)

def count_ones(config):
    left = config["left_hand_side"]
    right = config["right_hand_side"]
    current = config["symbol"]
    return left.count('1') + right.count('1') + (1 if current == '1' else 0)

class Particle:
    def __init__(self, x, y, color):
        self.x = x + random.uniform(-10, 10)
        self.y = y + random.uniform(-10, 10)
        self.vx = random.uniform(-0.8, 0.8)
        self.vy = random.uniform(-2.2, -0.4)
        self.life = random.randint(22, 46)
        self.max_life = self.life
        self.radius = random.uniform(1.8, 4.5)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life <= 0:
            return
        a = int(150 * (self.life / self.max_life))
        s = pygame.Surface((22, 22), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, a), (11, 11), int(self.radius))
        surface.blit(s, (self.x - 11, self.y - 11), special_flags=pygame.BLEND_PREMULTIPLIED)

class Button:
    def __init__(self, rect, label, accent_color, key_hint=""):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.accent = accent_color
        self.key_hint = key_hint
        self.hover = False

    def draw(self, surface):
        t = T()
        fill = t["panel2"] if not self.hover else (*self.accent, 70)
        border = (*self.accent, 170) if self.hover else t["border"]
        glass_panel(surface, self.rect, fill, border, radius=20, shadow=False)
        if self.hover:
            draw_glow(surface, self.rect.center, self.accent, radius=40, alpha=55, layers=4)
        draw_text(surface, self.label, FONT_BUTTON, t["text"], (self.rect.centerx, self.rect.centery - 8), center=True)
        if self.key_hint:
            draw_text(surface, self.key_hint, FONT_SMALL, t["muted"], (self.rect.centerx, self.rect.centery + 16), center=True)

    def handle_mouse(self, pos):
        self.hover = self.rect.collidepoint(pos)
        return self.hover

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

class TMVisualizer:
    def __init__(self):
        self.visible_cells = 13
        self.cell_w = 94
        self.cell_h = 96
        self.tape_y = 520
        self.auto_run = False
        self.auto_delay = 350
        self.last_auto_tick = 0
        self.history = []
        self.max_history = 8
        self.ones_history = []
        self.particles = []

        self.center_x = WIDTH // 2
        self.head_draw_x = self.center_x
        self.target_head_draw_x = self.center_x

        self.zoom = 1.0
        self.highlight_timer = 0
        self.last_written_index = None

        self.export_frames = False
        self.frame_id = 0

        self.presentation_mode = False

        self.buttons = [
            Button((60, 780, 140, 70), "STEP", (90, 220, 255), "SPACE"),
            Button((220, 780, 160, 70), "AUTO", (255, 170, 90), "ENTER"),
            Button((400, 780, 150, 70), "THEME", (180, 120, 255), "T"),
            Button((570, 780, 140, 70), "RESET", (120, 240, 170), "R"),
            Button((730, 780, 160, 70), "SHOT", (255, 120, 170), "S"),
        ]

        self.reset_machine()

    def reset_machine(self):
        self.tm = TuringMachine(
            TRANSITIONS,
            start_state=START_STATE,
            accept_state=HALT_STATE,
            blank_symbol=BLANK
        )
        self.runner = self.tm.run(INPUT_TAPE)

        self.action, self.config = next(self.runner)
        self.step_count = 0
        self.halted = False
        self.status = "READY"
        self.last_transition = self.peek_transition()
        self.history = [self.make_history_line("Init", self.config)]
        self.ones_history = [count_ones(self.config)]
        self.head_draw_x = self.center_x
        self.target_head_draw_x = self.center_x
        self.particles = []

    def peek_transition(self):
        if self.halted:
            return "Machine halted"
        state = self.config["state"]
        symbol = self.config["symbol"]
        key = (state, symbol)
        if key in TRANSITIONS:
            ns, wr, mv = TRANSITIONS[key]
            return f"{state},{symbol}  →  {wr}{mv}{ns}"
        return f"{state},{symbol}  →  no rule"

    def build_tape(self):
        left = list(reversed(self.config["left_hand_side"]))
        current = self.config["symbol"]
        right = self.config["right_hand_side"]
        tape = left + [current] + right
        head_idx = len(left)
        return tape, head_idx

    def make_history_line(self, prefix, cfg):
        st = cfg["state"]
        sy = cfg["symbol"]
        return f"{prefix}: state={st}, read={sy}, ones={count_ones(cfg)}"

    def spawn_particles(self, x, y, color, n=12):
        for _ in range(n):
            self.particles.append(Particle(x, y, color))

    def perform_step(self):
        if self.halted:
            return

        tape_before, head_before = self.build_tape()
        old_transition = self.peek_transition()

        try:
            self.action, self.config = next(self.runner)
            self.step_count += 1
            self.last_transition = self.peek_transition()

            if self.action:
                self.halted = True
                self.status = self.action.upper()
            else:
                self.status = "RUNNING"

            tape_after, head_after = self.build_tape()

            delta = head_after - head_before
            self.head_draw_x = self.center_x - delta * self.cell_w
            self.target_head_draw_x = self.center_x

            self.history.append(f"#{self.step_count}: {old_transition}")
            if len(self.history) > self.max_history:
                self.history.pop(0)

            self.ones_history.append(count_ones(self.config))
            if len(self.ones_history) > 60:
                self.ones_history.pop(0)

            self.spawn_particles(self.center_x, self.tape_y - 10, T()["accent"], n=10)

            if self.halted:
                self.spawn_particles(self.center_x, self.tape_y - 40, T()["warn"], n=28)

            if self.halted:
                HALT_SOUND.play()
            else:
                STEP_SOUND.play()

            self.highlight_timer = 15
            self.last_written_index = head_before

        except StopIteration:
            self.halted = True
            self.status = "HALTED"
            
            HALT_SOUND.play()

    def save_screenshot(self):
        filename = f"tm_visualizer_shot_{pygame.time.get_ticks()}.png"
        pygame.image.save(SCREEN, filename)
        print(f"Saved screenshot: {filename}")

    def update(self, now):
        self.head_draw_x = lerp(self.head_draw_x, self.target_head_draw_x, 0.18)

        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

        if self.auto_run and not self.halted and now - self.last_auto_tick >= self.auto_delay:
            self.perform_step()
            self.last_auto_tick = now
        
        if self.highlight_timer > 0:
            self.highlight_timer -= 1

    def draw_background(self):
        gradient_bg(SCREEN, T()["bg1"], T()["bg2"])
        draw_grid(SCREEN)

        draw_glow(SCREEN, (220, 110), T()["accent"], radius=120, alpha=26, layers=5)
        draw_glow(SCREEN, (WIDTH - 180, 160), T()["head"], radius=140, alpha=20, layers=5)

    def draw_header(self):
        rect = pygame.Rect(36, 28, WIDTH - 72, 115)
        glass_panel(SCREEN, rect, T()["panel"], T()["border"], radius=30)

        draw_text(SCREEN, "Ultimate Neon Glass Turing Machine Visualizer", FONT_TITLE, T()["text"], (62, 48))
        info = f"Theme: {current_theme_name.upper()}   •   Status: {self.status}   •   Step: {self.step_count}   •   Ones: {count_ones(self.config)}"
        draw_text(SCREEN, info, FONT_H2, T()["muted"], (64, 96))

    def draw_left_panel(self):
        rect = pygame.Rect(36, 170, 360, 570)
        glass_panel(SCREEN, rect, T()["panel"], T()["border"], radius=28)

        draw_text(SCREEN, "Machine Info", FONT_H1, T()["accent"], (58, 192))
        draw_text(SCREEN, f"Current state : {self.config['state']}", FONT_BODY, T()["text"], (58, 245))
        draw_text(SCREEN, f"Read symbol   : {self.config['symbol']}", FONT_BODY, T()["text"], (58, 280))
        draw_text(SCREEN, f"Halted        : {'Yes' if self.halted else 'No'}", FONT_BODY, T()["text"], (58, 315))
        draw_text(SCREEN, f"Auto-run      : {'ON' if self.auto_run else 'OFF'}", FONT_BODY, T()["text"], (58, 350))
        draw_text(SCREEN, f"Blank symbol  : {BLANK}", FONT_BODY, T()["text"], (58, 385))

        draw_text(SCREEN, "Current Transition", FONT_H1, T()["accent"], (58, 450))
        draw_text(SCREEN, self.peek_transition(), FONT_BODY, T()["text"], (58, 500))

        if self.halted:
            draw_glow(SCREEN, (226, 592), T()["warn"], radius=60, alpha=55, layers=5)
            draw_text(SCREEN, "HALTED", FONT_H1, T()["warn"], (226, 592), center=True)
        else:
            draw_glow(SCREEN, (226, 592), T()["good"], radius=60, alpha=38, layers=5)
            draw_text(SCREEN, "RUNNING", FONT_H1, T()["good"], (226, 592), center=True)

        draw_text(SCREEN, "Controls", FONT_H1, T()["accent"], (58, 650))
        draw_text(SCREEN, "SPACE  step", FONT_SMALL, T()["muted"], (58, 695))
        draw_text(SCREEN, "ENTER  auto-run", FONT_SMALL, T()["muted"], (58, 720))

    def draw_right_panel(self):
        rect = pygame.Rect(WIDTH - 400, 170, 360, 570)
        glass_panel(SCREEN, rect, T()["panel"], T()["border"], radius=28)

        draw_text(SCREEN, "Recent History", FONT_H1, T()["accent"], (WIDTH - 388, 192))

        y = 245
        for line in self.history[-8:]:
            draw_text(SCREEN, line, FONT_SMALL, T()["text"], (WIDTH - 388, y))
            y += 34

        draw_text(SCREEN, "Ones Trend", FONT_H1, T()["accent"], (WIDTH - 388, 540))
        self.draw_ones_chart(pygame.Rect(WIDTH - 388, 582, 320, 120))

    def draw_ones_chart(self, rect):
        if len(self.ones_history) < 2:
            return

        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        round_rect(panel, pygame.Rect(0, 0, rect.width, rect.height), T()["panel2"], radius=18)
        round_rect(panel, pygame.Rect(0, 0, rect.width, rect.height), T()["border"], radius=18, width=1)
        SCREEN.blit(panel, rect.topleft)

        vals = self.ones_history[-50:]
        mn, mx = min(vals), max(vals)
        if mn == mx:
            mn -= 1
            mx += 1

        pts = []
        for i, v in enumerate(vals):
            x = rect.x + 18 + i * (rect.width - 36) / max(1, len(vals) - 1)
            norm = (v - mn) / (mx - mn)
            y = rect.y + rect.height - 16 - norm * (rect.height - 32)
            pts.append((x, y))

        if len(pts) >= 2:
            pygame.draw.lines(SCREEN, T()["accent"], False, pts, 3)
            for p in pts[-6:]:
                draw_glow(SCREEN, (int(p[0]), int(p[1])), T()["accent"], radius=14, alpha=40, layers=4)
                pygame.draw.circle(SCREEN, T()["accent"], (int(p[0]), int(p[1])), 4)

        draw_text(SCREEN, f"min={min(vals)}", FONT_SMALL, T()["muted"], (rect.x + 10, rect.y + rect.height - 20))
        draw_text(SCREEN, f"max={max(vals)}", FONT_SMALL, T()["muted"], (rect.x + rect.width - 70, rect.y + 6))

    def draw_tape_panel(self):
        rect = pygame.Rect(420, 170, WIDTH - 840, 570)
        glass_panel(SCREEN, rect, T()["panel"], T()["border"], radius=34)

        draw_text(SCREEN, "Tape", FONT_H1, T()["accent"], (466, 192))

        tape, head_idx = self.build_tape()
        start_idx = head_idx - self.visible_cells // 2

        pulse = (math.sin(pygame.time.get_ticks() * 0.004) + 1) / 2

        for i in range(self.visible_cells):
            idx = start_idx + i
            cell_center_x = int(self.head_draw_x + (i - self.visible_cells // 2) * self.cell_w * self.zoom)
            cell_center_y = self.tape_y
            cell_w = int(self.cell_w * self.zoom)
            cell_h = int(self.cell_h * self.zoom)

            val = tape[idx] if 0 <= idx < len(tape) else BLANK
            is_head = (idx == head_idx)

            if self.highlight_timer > 0 and idx == self.last_written_index:
                pygame.draw.rect(
                    SCREEN,
                    (255, 255, 80),
                    (cell_center_x - cell_w//2, cell_center_y - cell_h//2, cell_w, cell_h),
                    4,
                    border_radius=18
                )

            color = T()["one"] if val == '1' else T()["zero"]

            shadow = pygame.Surface((cell_w + 18, cell_h + 18), pygame.SRCALPHA)
            round_rect(shadow, pygame.Rect(10, 10, self.cell_w - 4, self.cell_h - 2), T()["shadow"], radius=24)
            SCREEN.blit(shadow, (cell_center_x - self.cell_w // 2 - 1, cell_center_y - self.cell_h // 2 + 6))

            if is_head:
                draw_glow(SCREEN, (cell_center_x, cell_center_y), T()["head"], radius=84, alpha=110 + int(35 * pulse), layers=7)

            cell = pygame.Surface((self.cell_w, self.cell_h), pygame.SRCALPHA)
            round_rect(cell, pygame.Rect(0, 0, self.cell_w - 8, self.cell_h - 8), (*color, 240), radius=24)
            round_rect(cell, pygame.Rect(6, 6, self.cell_w - 20, 26), T()["glass"], radius=14)
            border = T()["head"] if is_head else T()["border"]
            round_rect(cell, pygame.Rect(0, 0, self.cell_w - 8, self.cell_h - 8), border, radius=24, width=2)

            SCREEN.blit(cell, (cell_center_x - self.cell_w // 2, cell_center_y - self.cell_h // 2))
            draw_text(SCREEN, str(val), FONT_TAPE, T()["text"], (cell_center_x, cell_center_y - 2), center=True)
            draw_text(SCREEN, str(idx), FONT_SMALL, T()["muted"], (cell_center_x, cell_center_y + 58), center=True)

            if is_head:
                draw_glow(SCREEN, (cell_center_x, cell_center_y - 84), T()["head"], radius=30, alpha=85, layers=5)
                pygame.draw.polygon(
                    SCREEN,
                    T()["head"],
                    [
                        (cell_center_x, cell_center_y - 58),
                        (cell_center_x - 18, cell_center_y - 94),
                        (cell_center_x + 18, cell_center_y - 94)
                    ]
                )
                draw_text(SCREEN, "HEAD", FONT_SMALL, T()["head"], (cell_center_x, cell_center_y - 126), center=True)

        

        for p in self.particles:
            p.draw(SCREEN)

    def draw_buttons(self, mouse_pos):
        for b in self.buttons:
            b.handle_mouse(mouse_pos)
            b.draw(SCREEN)

    def draw_footer(self):
        draw_text(
            SCREEN,
            "Presentation Mode: ON   •   Press S to save screenshot to /mnt/data",
            FONT_SMALL, T()["muted"], (WIDTH - 470, 804)
        )

    def export_frame(self):
        if not self.export_frames:
            return

        os.makedirs("frames", exist_ok=True)

        filename = f"frames/frame_{self.frame_id:05d}.png"
        pygame.image.save(SCREEN, filename)

        self.frame_id += 1

    def draw(self, mouse_pos):
        self.draw_background()
        self.draw_header()
        self.draw_left_panel()
        self.draw_tape_panel()
        self.draw_right_panel()
        self.draw_buttons(mouse_pos)
        self.draw_footer()
        pygame.display.flip()
        self.export_frame()

def main():
    global current_theme_name

    vis = TMVisualizer()

    while True:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    vis.perform_step()
                elif event.key == pygame.K_RETURN:
                    vis.auto_run = not vis.auto_run
                    vis.last_auto_tick = now
                elif event.key == pygame.K_t:
                    current_theme_name = "light" if current_theme_name == "dark" else "dark"
                elif event.key == pygame.K_r:
                    vis.reset_machine()
                elif event.key == pygame.K_s:
                    vis.save_screenshot()
                elif event.key == pygame.K_EQUALS:
                    vis.zoom = min(2.5, vis.zoom + 0.1)
                elif event.key == pygame.K_MINUS:
                    vis.zoom = max(0.6, vis.zoom - 0.1)
                elif event.key == pygame.K_g:
                    vis.export_frames = not vis.export_frames
                elif event.key == pygame.K_p:
                    vis.presentation_mode = not vis.presentation_mode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if vis.buttons[0].clicked(mouse_pos):
                    vis.perform_step()
                elif vis.buttons[1].clicked(mouse_pos):
                    vis.auto_run = not vis.auto_run
                    vis.last_auto_tick = now
                elif vis.buttons[2].clicked(mouse_pos):
                    current_theme_name = "light" if current_theme_name == "dark" else "dark"
                elif vis.buttons[3].clicked(mouse_pos):
                    vis.reset_machine()
                elif vis.buttons[4].clicked(mouse_pos):
                    vis.save_screenshot()

        vis.update(now)
        vis.draw(mouse_pos)
        CLOCK.tick(60)

if __name__ == "__main__":
    main()