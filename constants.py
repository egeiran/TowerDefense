from enemy_data import ENEMY_SPAWN_DATA

ROWS, COLS = 15, 15
TILE_SIZE = 48
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS   * TILE_SIZE
FPS = 100
# The speed the game was tuned at. Browsers usually cap rendering at 60 FPS,
# so movement is scaled against this to keep web and desktop playing alike.
REFERENCE_FPS = 100
HEALTH = 50
MONEY = 650
SIDE_PANEL = 300
TOTAL_LEVELS = len(ENEMY_SPAWN_DATA)

# Enemy constants
SPAWN_COOLDOWN = 400

# Turret constants
TURRET_LEVELS = 4
BUY_COST = 150
UPGRADE_COST = 100
LEVEL_COMPLETE_REWARD = 100
ANIMATION_STEPS = 8
ANIMATION_DELAY = 15
DAMAGE = 5