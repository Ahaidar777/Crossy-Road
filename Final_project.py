import py5_tools
 
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)
ROAD_HEIGHT = 100
ROAD_SPACING = 150
(VEHICLE_WIDTH, VEHICLE_HEIGHT) = (100, 50)
VEHICLE_SPEED = 10
WHEEL_RADIUS = 30
DASHED_LINE_WIDTH = 5
DASHED_LINE_SPACING = 10
score = -1
last_road_crossed = -1

# Colors
YELLOW = color(250, 213, 165)
GRAY_COLOR = color(105, 105, 105)
WHITE = color(255, 255, 255)
BLACK = color(0)
RED = color(255, 0, 0)

# Player
player_pos = [SCREEN_WIDTH // 2 - 60 // 2, SCREEN_HEIGHT - 60]
player_speed = 8

# Roads
roads = []
for i in range(4):
    roads.append({"x": 0, "y": i * ROAD_SPACING, "w": SCREEN_WIDTH, "h": ROAD_HEIGHT})

# Vehicle
vehicle = {
    "pos": [
        0,
        random.randint(roads[0]["y"], roads[0]["y"] + ROAD_HEIGHT - VEHICLE_HEIGHT),
    ],
    "speed": VEHICLE_SPEED,
    "road": random.randint(0, 3),
}

# Game loop variables
gameover = False
running = True
move_left = move_right = move_up = move_down = False
first_movement_made = False


def setup():
    size(SCREEN_WIDTH, SCREEN_HEIGHT)
    global chicken_image
    # The chicken image
    chicken_image = load_image(
        "C:\\Users\\aliha\\OneDrive\\Desktop\\CS 125\\chicken.png"
    )


def draw():
    global score, last_road_crossed, gameover, running, move_left, move_right, move_up, move_down, first_movement_made
    background(YELLOW)

    if not gameover:
        update_game_state()

    draw_scene()


def update_game_state():
    global score, last_road_crossed, gameover, vehicle
    # Player position
    if move_left and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if move_right and player_pos[0] < SCREEN_WIDTH - 60:
        player_pos[0] += player_speed
    if move_up and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if move_down and player_pos[1] < SCREEN_HEIGHT - 60:
        player_pos[1] += player_speed

    # Vehicle position
    if vehicle["road"] != 4:
        vehicle["pos"][0] += vehicle["speed"]
        if vehicle["pos"][0] > SCREEN_WIDTH:
            vehicle["speed"] = 10
            vehicle["pos"][0] = 0
            vehicle["pos"][1] = random.randint(
                roads[vehicle["road"]]["y"],
                roads[vehicle["road"]]["y"] + ROAD_HEIGHT - VEHICLE_HEIGHT,
            )
            vehicle["road"] += 1
            if vehicle["road"] == 4:
                vehicle["road"] = 0
    # Check collision
    if rect_collision(
        player_pos[0],
        player_pos[1],
        60,
        60,
        vehicle["pos"][0],
        vehicle["pos"][1],
        VEHICLE_WIDTH,
        VEHICLE_HEIGHT,
    ):
        gameover = True

    # Score
    current_road = player_pos[1] // ROAD_SPACING
    if current_road != last_road_crossed:
        score += 1
        last_road_crossed = current_road


def rect_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    """Check if two rectangles (x1, y1, w1, h1) and (x2, y2, w2, h2) overlap."""
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2


def draw_scene():
    global gameover, score
    # Draw roads
    for road in roads:
        fill(GRAY_COLOR)
        rect(road["x"], road["y"], road["w"], road["h"])
        # Draw dashed lines
        dash_start = road["x"]
        while dash_start < road["w"]:
            dash_end = min(dash_start + DASHED_LINE_WIDTH, road["w"])
            stroke(WHITE)
            line(
                dash_start,
                road["y"] + ROAD_HEIGHT / 2,
                dash_end,
                road["y"] + ROAD_HEIGHT / 2,
            )
            dash_start += DASHED_LINE_WIDTH + DASHED_LINE_SPACING

    # Draw Vehicle
    fill(RED)
    rect(vehicle["pos"][0], vehicle["pos"][1], VEHICLE_WIDTH, VEHICLE_HEIGHT)

    # Draw wheels for the vehicle
    fill(BLACK)
    ellipse(
        vehicle["pos"][0] + 10,
        vehicle["pos"][1] + VEHICLE_HEIGHT,
        WHEEL_RADIUS,
        WHEEL_RADIUS,
    )
    ellipse(
        vehicle["pos"][0] + VEHICLE_WIDTH - 10,
        vehicle["pos"][1] + VEHICLE_HEIGHT,
        WHEEL_RADIUS,
        WHEEL_RADIUS,
    )

    # Draw windows for the vehicle
    fill(WHITE)
    rect(vehicle["pos"][0] + 10, vehicle["pos"][1] + 10, 20, 15)
    rect(vehicle["pos"][0] + VEHICLE_WIDTH - 30, vehicle["pos"][1] + 10, 20, 15)
    # Draw player
    chicken_width = 60
    chicken_height = 60
    image(chicken_image, player_pos[0], player_pos[1], chicken_width, chicken_height)

    # Display score
    fill(BLACK)
    text_size(20)
    text(f"Score: {score}", 10, SCREEN_HEIGHT - 20)

    # Game over screen
    if gameover:
        fill(WHITE)
        rect(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 100, 400, 200)
        fill(BLACK)
        text_size(30)
        text("Game Over", SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2)


def key_pressed():
    global move_left, move_right, move_up, move_down
    if key_code == LEFT:
        move_left = True
    elif key_code == RIGHT:
        move_right = True
    elif key_code == UP:
        move_up = True
    elif key_code == DOWN:
        move_down = True


def key_released():
    global move_left, move_right, move_up, move_down, gameover, score, player_pos, vehicle
    if key_code == LEFT:
        move_left = False
    elif key_code == RIGHT:
        move_right = False
    elif key_code == UP:
        move_up = False
    elif key_code == DOWN:
        move_down = False

    # Reset game after game over
    if gameover:
        gameover = False
        score = 0
        player_pos = [SCREEN_WIDTH // 2 - 60 // 2, SCREEN_HEIGHT - 60]
        vehicle = {
            "pos": [
                0,
                random.randint(
                    roads[0]["y"], roads[0]["y"] + ROAD_HEIGHT - VEHICLE_HEIGHT
                ),
            ],
            "speed": VEHICLE_SPEED,
            "road": random.randint(0, 3),
        }


py5_tools.animated_gif("Final_project.gif", 100, 0.05, 0.05)
