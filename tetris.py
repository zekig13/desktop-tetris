import os
import random
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENDOR_DIR = os.path.join(BASE_DIR, "vendor")
if VENDOR_DIR not in sys.path:
    sys.path.insert(0, VENDOR_DIR)

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 32
PANEL_WIDTH = 220
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE
FPS = 60

EMPTY = ""
BG = (16, 18, 24)
BOARD_BG = (24, 28, 37)
GRID = (41, 48, 61)
TEXT = (236, 240, 248)
MUTED = (170, 178, 194)
GHOST_ALPHA = 90

COLORS = {
    "I": (62, 197, 255),
    "J": (79, 124, 255),
    "L": (255, 159, 67),
    "O": (255, 217, 61),
    "S": (76, 217, 100),
    "T": (176, 108, 255),
    "Z": (255, 92, 92),
}

SHAPES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
}

LEVEL_SPEEDS = [
    700, 620, 540, 470, 400,
    340, 290, 250, 210, 180,
    150, 125, 105, 90, 80,
]


def build_fonts():
    return (
        pygame.font.SysFont("segoeui", 34, bold=True),
        pygame.font.SysFont("segoeui", 24, bold=True),
        pygame.font.SysFont("segoeui", 18),
        pygame.font.SysFont("segoeui", 38, bold=True),
    )


class TetrisGame:
    def __init__(self):
        self.restart()

    def restart(self):
        self.board = [[EMPTY for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.paused = False
        self.game_over = False
        self.bag = []
        self.current = None
        self.next_piece = self._take_from_bag()
        self.spawn_piece()

    def _take_from_bag(self):
        if not self.bag:
            self.bag = list(SHAPES.keys())
            random.shuffle(self.bag)
        return self.bag.pop()

    def spawn_piece(self):
        self.current = {"kind": self.next_piece, "rotation": 0, "x": 3, "y": 0}
        self.next_piece = self._take_from_bag()
        if self.collides(self.current["x"], self.current["y"], self.current["rotation"]):
            self.game_over = True

    def current_cells(self, x=None, y=None, rotation=None, kind=None):
        piece = self.current
        kind = kind or piece["kind"]
        x = piece["x"] if x is None else x
        y = piece["y"] if y is None else y
        rotation = piece["rotation"] if rotation is None else rotation
        return [(x + dx, y + dy) for dx, dy in SHAPES[kind][rotation]]

    def collides(self, x, y, rotation):
        for cell_x, cell_y in self.current_cells(x=x, y=y, rotation=rotation):
            if cell_x < 0 or cell_x >= BOARD_WIDTH or cell_y >= BOARD_HEIGHT:
                return True
            if cell_y >= 0 and self.board[cell_y][cell_x] != EMPTY:
                return True
        return False

    def move(self, dx, dy):
        if self.paused or self.game_over:
            return False
        new_x = self.current["x"] + dx
        new_y = self.current["y"] + dy
        if self.collides(new_x, new_y, self.current["rotation"]):
            return False
        self.current["x"] = new_x
        self.current["y"] = new_y
        return True

    def rotate(self):
        if self.paused or self.game_over:
            return False
        next_rotation = (self.current["rotation"] + 1) % 4
        for kick in (0, -1, 1, -2, 2):
            if not self.collides(self.current["x"] + kick, self.current["y"], next_rotation):
                self.current["x"] += kick
                self.current["rotation"] = next_rotation
                return True
        return False

    def soft_drop(self):
        if self.move(0, 1):
            self.score += 1
            return True
        if not self.paused and not self.game_over:
            self.lock_piece()
        return False

    def hard_drop(self):
        if self.paused or self.game_over:
            return
        distance = 0
        while self.move(0, 1):
            distance += 1
        self.score += distance * 2
        self.lock_piece()

    def update(self):
        if self.paused or self.game_over:
            return
        if not self.move(0, 1):
            self.lock_piece()

    def lock_piece(self):
        kind = self.current["kind"]
        for x, y in self.current_cells():
            if y < 0:
                self.game_over = True
                return
            self.board[y][x] = kind
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        kept_rows = [row for row in self.board if any(cell == EMPTY for cell in row)]
        cleared = BOARD_HEIGHT - len(kept_rows)
        if not cleared:
            return
        while len(kept_rows) < BOARD_HEIGHT:
            kept_rows.insert(0, [EMPTY for _ in range(BOARD_WIDTH)])
        self.board = kept_rows
        self.lines += cleared
        self.level = 1 + self.lines // 10
        self.score += {1: 100, 2: 300, 3: 500, 4: 800}[cleared] * self.level

    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused

    def ghost_y(self):
        drop_y = self.current["y"]
        while not self.collides(self.current["x"], drop_y + 1, self.current["rotation"]):
            drop_y += 1
        return drop_y

    def fall_delay(self):
        return LEVEL_SPEEDS[min(self.level - 1, len(LEVEL_SPEEDS) - 1)]


def draw_block(surface, x, y, color, ghost=False):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    if ghost:
        ghost_surface = pygame.Surface((CELL_SIZE - 6, CELL_SIZE - 6), pygame.SRCALPHA)
        ghost_surface.fill((*color, GHOST_ALPHA))
        surface.blit(ghost_surface, (rect.x + 3, rect.y + 3))
        pygame.draw.rect(surface, color, rect.inflate(-6, -6), 2, border_radius=6)
        return
    pygame.draw.rect(surface, color, rect.inflate(-2, -2), border_radius=7)
    highlight = tuple(min(255, channel + 50) for channel in color)
    pygame.draw.rect(surface, highlight, (rect.x + 4, rect.y + 4, CELL_SIZE - 16, CELL_SIZE - 16), border_radius=5)


def draw_preview(surface, piece_kind):
    preview_origin_x = BOARD_WIDTH * CELL_SIZE + 48
    preview_origin_y = 150
    coords = SHAPES[piece_kind][0]
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)
    preview_cell = 24
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    offset_x = preview_origin_x + (120 - width * preview_cell) // 2
    offset_y = preview_origin_y + (80 - height * preview_cell) // 2

    box = pygame.Rect(preview_origin_x, preview_origin_y, 120, 80)
    pygame.draw.rect(surface, (27, 31, 41), box, border_radius=12)
    pygame.draw.rect(surface, (48, 58, 74), box, 1, border_radius=12)

    for x, y in coords:
        rect = pygame.Rect(
            offset_x + (x - min_x) * preview_cell,
            offset_y + (y - min_y) * preview_cell,
            preview_cell,
            preview_cell,
        )
        pygame.draw.rect(surface, COLORS[piece_kind], rect.inflate(-2, -2), border_radius=6)


def render(screen, game, fonts):
    title_font, label_font, small_font, overlay_font = fonts
    screen.fill(BG)

    board_rect = pygame.Rect(0, 0, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE)
    pygame.draw.rect(screen, BOARD_BG, board_rect)

    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            pygame.draw.rect(screen, GRID, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            cell = game.board[y][x]
            if cell != EMPTY:
                draw_block(screen, x, y, COLORS[cell])

    if not game.game_over:
        for x, y in game.current_cells(y=game.ghost_y()):
            draw_block(screen, x, y, COLORS[game.current["kind"]], ghost=True)
        for x, y in game.current_cells():
            draw_block(screen, x, y, COLORS[game.current["kind"]])

    panel_x = BOARD_WIDTH * CELL_SIZE + 24
    screen.blit(title_font.render("TETRIS", True, TEXT), (panel_x, 24))
    screen.blit(label_font.render(f"Skor: {game.score}", True, TEXT), (panel_x, 80))
    screen.blit(label_font.render(f"Satir: {game.lines}", True, TEXT), (panel_x, 110))
    screen.blit(label_font.render(f"Seviye: {game.level}", True, TEXT), (panel_x, 140))
    screen.blit(label_font.render("Siradaki", True, TEXT), (panel_x, 186))

    draw_preview(screen, game.next_piece)

    controls = [
        "Sol / Sag: Hareket",
        "Yukari: Dondur",
        "Asagi: Hizli indir",
        "Bosluk: Sert dusur",
        "P: Duraklat",
        "R: Yeniden baslat",
    ]
    screen.blit(label_font.render("Kontroller", True, TEXT), (panel_x, 268))
    y = 305
    for line in controls:
        screen.blit(small_font.render(line, True, MUTED), (panel_x, y))
        y += 28

    if game.paused or game.game_over:
        overlay = pygame.Surface((BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE), pygame.SRCALPHA)
        overlay.fill((8, 10, 14, 180))
        screen.blit(overlay, (0, 0))
        message = "DURAKLATILDI" if game.paused else "OYUN BITTI"
        screen.blit(overlay_font.render(message, True, TEXT), (28, 250))
        if game.game_over:
            score_text = label_font.render("R ile yeniden baslat", True, TEXT)
            screen.blit(score_text, (54, 300))

    pygame.display.flip()


def build_showcase_game():
    game = TetrisGame()
    layout = [
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "..........",
        "...T......",
        "...TT.....",
        "...T......",
        "..SS......",
        ".SS..OO...",
        ".J...OO...",
        ".JJJ..L...",
        "..ZZ.LL...",
        "...ZZ.L...",
        "IIIII.....",
        "TT..SS.JJ.",
        "TTOOSSJJL.",
        "ZZOOLLJLL.",
    ]
    game.board = [
        [cell if cell != "." else EMPTY for cell in row]
        for row in layout
    ]
    game.score = 4820
    game.lines = 27
    game.level = 3
    game.current = {"kind": "I", "rotation": 1, "x": 4, "y": 2}
    game.next_piece = "Z"
    game.game_over = False
    game.paused = False
    return game


def export_screenshot(output_path):
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen = pygame.display.get_surface()
    render(screen, build_showcase_game(), build_fonts())
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pygame.image.save(screen, output_path)
    pygame.quit()


def run_game():
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    fonts = build_fonts()

    game = TetrisGame()
    last_fall = pygame.time.get_ticks()
    running = True

    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.soft_drop()
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                elif event.key == pygame.K_p:
                    game.toggle_pause()
                elif event.key == pygame.K_r:
                    game.restart()
                if event.key in (pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_SPACE):
                    last_fall = now

        if now - last_fall >= game.fall_delay():
            game.update()
            last_fall = now

        render(screen, game, fonts)
        clock.tick(FPS)

    pygame.quit()


def run_self_test():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((320, 240))
    game = TetrisGame()
    fonts = build_fonts()
    screen = pygame.display.get_surface()
    render(screen, game, fonts)
    pygame.quit()


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        run_self_test()
    elif len(sys.argv) == 3 and sys.argv[1] == "--export-screenshot":
        export_screenshot(sys.argv[2])
    else:
        run_game()
