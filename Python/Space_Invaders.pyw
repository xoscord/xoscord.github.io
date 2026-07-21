import random
import time
import turtle
import json
import os


title=r"""
 __                         _____                     _               
/ _\_ __   __ _  ___ ___    \_   \_ ____   ____ _  __| | ___ _ __ ___ 
\ \| '_ \ / _` |/ __/ _ \    / /\/ '_ \ \ / / _` |/ _` |/ _ \ '__/ __|
_\ \ |_) | (_| | (_|  __/ /\/ /_ | | | \ V / (_| | (_| |  __/ |  \__ \
\__/ .__/ \__,_|\___\___| \____/ |_| |_|\_/ \__,_|\__,_|\___|_|  |___/
   |_|                                                                
"""


FRAME_RATE = 30
TIME_FOR_1_FRAME = 1 / FRAME_RATE

# Base values (levels scale these)
CANNON_STEP = 15
LASER_SPEED = 20
BASE_ALIEN_SPEED = 3.5
ALIEN_SPAWN_INTERVAL = 1.2

window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("Space Invaders")

# --- Window Optimization and Security ---
# Get the underlying Tkinter window root
canvas = window.getcanvas()
root = canvas.winfo_toplevel()

# 1. Lock window dimensions to prevent resizing bugs
root.resizable(False, False)

# 2. Safely capture the window cross close ("X") button event to avoid terminal errors
keep_running = True
def handle_window_close():
    global keep_running
    keep_running = False

root.protocol("WM_DELETE_WINDOW", handle_window_close)

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

# --- Exact Shape Cloning from Image ---
# Continuous path outlining the inner and outer strokes of the rectangles
# --- Exact Shape Cloned from Image (Rotated 90° Counter-Clockwise) ---
cannon_shape = (
    (-30, -3), (-30, 3), (-10, 3),              # Top box outer (now pointing left)
    (-10, 45), (5, 45),                         # Left horizontal wing outer
    (5, 3), (15, 3),                            # Stem outer
    (15, 8), (20, 8), (20, 3), (30, 3),         # Side wing and tail outer
    (30, -3), (20, -3), (20, -8), (15, -8),     # Right tail base outer
    (15, -3), (5, -3),                          # Stem outer
    (5, -45), (-10, -45),                       # Right horizontal wing outer
    (-10, -3), (-30, -3),                       # Back to top box
    (-30, 0),                                   # Direct bridge to interior
    (-10, -3), (-10, 3), (5, 3), (5, -3), (-10, -3) # Hollow core intersecting lines
)
window.register_shape("cannon_ship", cannon_shape)

alien_shape = ((0, -6), (4, -2), (10, -2), (6, 2), (0, 8), (-6, 2), (-10, -2), (-4, -2))
window.register_shape("alien_ship", alien_shape)

# --- Global Entities ---
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.fillcolor("") # Keeps inside hollow exactly like the original drawing method
cannon.shape("cannon_ship")
cannon.setposition(0, FLOOR_LEVEL + 15)
cannon.cannon_movement = 0
cannon.hideturtle()

text = turtle.Turtle()
text.penup()
text.hideturtle()
text.color(1, 1, 1)

ui_text = turtle.Turtle()
ui_text.penup()
ui_text.hideturtle()
ui_text.color("white")

lasers = []
aliens = []

# --- Game State Variables ---
game_state = "MENU"
score = 0
current_level = 1
game_timer = 0
alien_timer = 0

# --- Database Functions ---
def load_leaderboard():
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def show_menu():
    global game_state
    game_state = "MENU"
    ui_text.clear()
    text.clear()
    cannon.hideturtle()
    
    for a in aliens: a.hideturtle()
    for l in lasers: l.hideturtle()
    aliens.clear()
    lasers.clear()
    
    ui_text.goto(0, 180)
    # ui_text.write("SPACE INVADERS", font=("Courier", 36, "bold"), align="center")
    ui_text.write(title, font=("Courier", 5, "bold"), align="center")
    
    ui_text.goto(0, 100)
    ui_text.write("--- LEADERBOARD ---", font=("Courier", 18, "bold"), align="center")
    
    scores_data = load_leaderboard()
    sorted_scores = sorted(scores_data.items(), key=lambda x: x[1]['score'], reverse=True)[:5]
    
    y_pos = 60
    if not sorted_scores:
        ui_text.goto(0, y_pos)
        ui_text.write("No scores yet!", font=("Courier", 14, "normal"), align="center")
    else:
        for i, (user, data) in enumerate(sorted_scores):
            lvl = data.get("level", 1)
            ui_text.goto(0, y_pos - (i * 28))
            ui_text.write(f"{i+1}. {user} | Score: {data['score']} | Lvl: {lvl}", font=("Courier", 13, "bold"), align="center")

    ui_text.goto(0, -150)
    ui_text.write("Press SPACE to Start\nPress Q to Quit to Menu (In-Game)\nPress E to Exit Game Completely", font=("Courier", 14, "normal"), align="center")
    window.update()
    window.listen()

def start_game():
    global game_state, score, current_level, game_timer, alien_timer
    if game_state in ["MENU", "GAMEOVER"]:
        ui_text.clear()
        score = 0
        current_level = 1
        game_timer = time.time()
        alien_timer = time.time()
        
        for a in aliens: a.hideturtle()
        for l in lasers: l.hideturtle()
        aliens.clear()
        lasers.clear()
        
        cannon.showturtle()
        cannon.setposition(0, FLOOR_LEVEL + 15)
        game_state = "PLAYING"

def handle_score_saving(final_score, final_level):
    username = window.textinput("Score Save", "Enter Username (Cancel to skip):")
    if not username:
        window.listen()
        return

    data = load_leaderboard()

    if username in data and data[username].get("password"):
        password = window.textinput("Score Save", f"Enter Password for {username}:")
        if data[username]["password"] != password:
            print("Incorrect password. Score not saved.")
            window.listen()
            return
    else:
        password = window.textinput("Score Save", "Create Password (Leave blank to save unprotected):")

    if username in data:
        if final_score > data[username]["score"]:
            data[username]["score"] = final_score
            data[username]["level"] = max(final_level, data[username].get("level", 1))
            print(f"New high score updated for {username}!")
        else:
            print(f"Score did not beat your record of {data[username]['score']}. Not saved.")
    else:
        data[username] = {
            "password": password if password else "", 
            "score": final_score,
            "level": final_level
        }
        print(f"Score of {final_score} saved successfully!")

    with open("scores.json", "w") as f:
        json.dump(data, f, indent=4)
        
    window.listen()

def end_game():
    global game_state
    game_state = "GAMEOVER"
    ui_text.goto(0, 50)
    ui_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")
    window.update()
    
    handle_score_saving(score, current_level)
    
    ui_text.goto(0, -50)
    ui_text.write("Press R to Restart\nPress Q to go to Menu\nPress E to Exit", font=("Courier", 16, "normal"), align="center")
    window.update()

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.shape("alien_ship")
    alien.color("white")
    alien.setheading(-90)
    alien.setposition(random.randint(int(LEFT + GUTTER), int(RIGHT - GUTTER)), TOP)
    aliens.append(alien)

def create_laser():
    if game_state == "PLAYING":
        laser = turtle.Turtle()
        laser.penup()
        laser.color(1, 0, 0)
        laser.shape("square")
        laser.shapesize(stretch_wid=0.1, stretch_len=1)
        laser.setheading(90)
        laser.setposition(cannon.xcor(), cannon.ycor() + 25)
        lasers.append(laser)

def remove_sprite(sprite, sprite_list):
    sprite.hideturtle()
    sprite.clear()
    if sprite in sprite_list:
        sprite_list.remove(sprite)

# --- Control Hooks ---
def space_pressed():
    if game_state in ["MENU", "GAMEOVER"]:
        start_game()
    elif game_state == "PLAYING":
        create_laser()

def r_pressed():
    if game_state == "GAMEOVER":
        start_game()

def q_pressed():
    if game_state in ["PLAYING", "GAMEOVER"]:
        show_menu()

def e_pressed():
    global keep_running
    keep_running = False

window.onkeypress(lambda: setattr(cannon, "cannon_movement", -1), "Left")
window.onkeypress(lambda: setattr(cannon, "cannon_movement", 1), "Right")
window.onkeyrelease(lambda: setattr(cannon, "cannon_movement", 0), "Left")
window.onkeyrelease(lambda: setattr(cannon, "cannon_movement", 0), "Right")
window.onkeypress(space_pressed, "space")
window.onkeypress(r_pressed, "r")
window.onkeypress(q_pressed, "q")
window.onkeypress(e_pressed, "e")
window.listen()

# --- Execution Engine ---
show_menu()

while keep_running:
    try:
        timer_this_frame = time.time()

        if game_state == "PLAYING":
            current_level = 1 + (score // 5)
            active_alien_speed = BASE_ALIEN_SPEED + (current_level - 1) * 0.8

            time_elapsed = time.time() - game_timer
            text.clear()
            text.setposition(LEFT * 0.8, TOP * 0.8)
            text.write(
                f"Time: {time_elapsed:5.1f}s\nScore: {score:5}\nLevel: {current_level:5}", 
                font=("Courier", 18, "bold")
            )
            
            new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
            if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
                cannon.setx(new_x)
                
            for laser in lasers.copy():
                laser.forward(LASER_SPEED)
                if laser.ycor() > TOP:
                    remove_sprite(laser, lasers)
                    continue
                for alien in aliens.copy():
                    if laser.distance(alien) < 25:
                        remove_sprite(laser, lasers)
                        remove_sprite(alien, aliens)
                        score += 1
                        break
                        
            if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
                create_alien()
                alien_timer = time.time()

            for alien in aliens.copy():
                alien.forward(active_alien_speed)
                if alien.ycor() < FLOOR_LEVEL:
                    end_game()
                    break

        window.update()
        
        time_for_this_frame = time.time() - timer_this_frame
        if time_for_this_frame < TIME_FOR_1_FRAME:
            time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
            
    except turtle.Terminator:
        break

try:
    window.bye()
except turtle.Terminator:
    pass
