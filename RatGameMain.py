import pygame
import sys
import os
import sqlite3

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Rat")

# Change the current working directory to the folder where your script is located
script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

WIDTH, HEIGHT, GRID_SIZE, BACKGROUND = 800, 800, 40, pygame.image.load("background_1.png")
# Set up display
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
current_rat_image, tick = "rat_1.png", 0
rat_image = pygame.image.load(current_rat_image)
apple_tree_image = pygame.image.load("tree_apple.png").convert_alpha()
apple_1_image = pygame.image.load("apple.png")
rat_image_rect = rat_image.get_rect()
apple_tree_rect = apple_tree_image.get_rect()
apple_1_rect = apple_1_image.get_rect()
rat_image_mask = pygame.mask.from_surface(rat_image)
apple_tree_mask = pygame.mask.from_surface(apple_tree_image)
apple_1_mask = pygame.mask.from_surface(apple_1_image)
holding = False
apple_x = 400
apple_y = 400
apple_screen = "screen12"

current_screen = "main"

rat_x, rat_y, rat_image1, rat_image2, rat_image3, rat_image4, rat_speed = 400, 400, "rat_1.png", "rat_2.png", "rat_3.png", "rat_4.png", 1

# SQLite Database
conn = sqlite3.connect('game_database.db')
cursor = conn.cursor()
conn.commit()

def new_screen():
    cursor.execute("INSERT INTO player_data (screen, x, y) VALUES (?, ?, ?)", ("main", rat_x, rat_y))
    conn.commit()

def draw_screen():
    global holding, rat_image1, rat_image2, normal, sprint, current_rat_image, apple_screen

    # Clear the screen
    if current_screen == "cloud":
        SCREEN.fill((0, 0, 0))
    else:
        SCREEN.blit(BACKGROUND, (0, 0))

    # Draw rat
    rat_image = pygame.image.load(current_rat_image)
    rat_image_rect = rat_image.get_rect(center = (rat_x, rat_y))
    rat_image_mask = pygame.mask.from_surface(rat_image)

    if current_screen == apple_screen:
        if rat_image_mask.overlap(apple_1_mask, (apple_1_rect.x - rat_image_rect.x + apple_x, apple_1_rect.y - rat_image_rect.y + apple_y)) and sprinting == False:
            rat_image1, rat_image2 = "rat_1_apple.png", "rat_2_apple.png"
            if current_rat_image == "rat_1.png":
                current_rat_image = "rat_1_apple.png"
            if current_rat_image == "rat_2.png":
                current_rat_image = "rat_2_apple.png"
            holding = True
        elif holding == False:
            rat_image1, rat_image2 = "rat_1.png", "rat_2.png"
            SCREEN.blit(apple_1_image, (apple_x, apple_y))

    # Draw the image on the screen
    SCREEN.blit(rat_image, rat_image_rect.topleft)

    if current_screen == "screen11":
        if rat_image_mask.overlap(apple_tree_mask, (apple_tree_rect.x - rat_image_rect.x + 180, apple_tree_rect.y - rat_image_rect.y + 50)):
            apple_tree_image.set_alpha(128)
            SCREEN.blit(apple_tree_image, (180, 50))
        else:
            apple_tree_image.set_alpha(256)
            SCREEN.blit(apple_tree_image, (180, 50))

    normal = move(rat_image1, rat_image2, rat_image3, rat_image4, 3)
    sprint = move(rat_image3, rat_image4, rat_image1, rat_image2, 6)

    # Update the display
    pygame.display.flip()

def update_rat():
    global rat_image_rect
    old_rat_image_rect = rat_image_rect.copy()
    rat_image_rect = rat_image.get_rect()
    pygame.display.update([old_rat_image_rect, rat_image_rect])
    
def screen_up():
    global rat_y
    if rat_y <= 20:
        new_screen()
        rat_y = HEIGHT - 22
        return True
    
def screen_down():
    global rat_y
    if rat_y >= HEIGHT - 20:
        new_screen()
        rat_y = 22
        return True
    
def screen_left():
    global rat_x
    if rat_x <= 20:
        new_screen()
        rat_x = WIDTH - 22
        return True
    
def screen_right():
    global rat_x
    if rat_x >= WIDTH - 20:
        new_screen()
        rat_x = 22
        return True

class move():

    def __init__(self, image1, image2, otherimage1, otherimage2, speed):
        self.image1 = image1
        self.image2 = image2
        self.otherimage1 = otherimage1
        self.otherimage2 = otherimage2
        self.speed = speed

    def move_rat(self):
        global current_rat_image, rat_x, rat_y
        if current_rat_image == self.otherimage1 or current_rat_image == "rat_1_apple.png":
            current_rat_image = self.image1
        elif current_rat_image == self.otherimage2 or current_rat_image == "rat_2_apple.png":
            current_rat_image = self.image2

        if key[pygame.K_a] and rat_x > 20:
            rat_x -= self.speed
            current_rat_image = self.image1
            update_rat()
        if key[pygame.K_d] and rat_x < WIDTH - 20:
            rat_x += self.speed
            current_rat_image = self.image2
            update_rat()
        if key[pygame.K_w] and rat_y > 20:
            rat_y -= self.speed
            update_rat()
        if key[pygame.K_s] and rat_y < HEIGHT - 20:
            rat_y += self.speed
            update_rat()
        

class screen():

    def __init__(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def check_if_new_screen(self):
        global current_screen
        if self.up and screen_up():
            current_screen = self.up
        elif self.down and screen_down():
            current_screen = self.down
        elif self.left and screen_left():
            current_screen = self.left
        elif self.right and screen_right():
            current_screen = self.right

main = screen(None, None, None, "screen11")
screen11 = screen(None, "screen21", "main", "screen12")
screen12 = screen(None, "screen22", "screen11", "screen13")
screen13 = screen(None, "screen23", "screen12", "screen14")
screen14 = screen(None, "screen24", "screen13", None)
screen21 = screen("screen11", "screen31", None, "screen22")
screen22 = screen("screen12", "screen32", "screen21", "screen23")
screen23 = screen("screen13", "screen33", "screen22", "screen24")
screen24 = screen("screen14", "screen34", "screen23", None)
screen31 = screen("screen21", "screen41", None, "screen32")
screen32 = screen("screen22", "screen42", "screen31", "screen33")
screen33 = screen("screen23", "screen43", "screen32", "screen34")
screen34 = screen("screen24", "screen44", "screen33", None)
screen41 = screen("screen31", None, None, "screen42")
screen42 = screen("screen32", None, "screen41", "screen43")
screen43 = screen("screen33", None, "screen42", "screen44")
screen44 = screen("screen34", None, "screen43", "cloud")
cloud = screen(None, None, "screen44", None)

normal = move(rat_image1, rat_image2, rat_image3, rat_image4, 3)
sprint = move(rat_image3, rat_image4, rat_image1, rat_image2, 6)

screens = ["main", "screen11", "screen12", "screen13", "screen14", "screen21", "screen22", "screen23", "screen24", "screen31", "screen32", "screen33", "screen34", "screen41", "screen42", "screen43", "screen44", "cloud"]
screen_variables = {"main": main, "screen11": screen11, "screen12": screen12, "screen13": screen13, "screen14": screen14, "screen21": screen21, "screen22": screen22, "screen23": screen23, "screen24": screen24, "screen31": screen31, "screen32": screen32, "screen33": screen33, "screen34": screen34, "screen41": screen41, "screen42": screen42, "screen43": screen43, "screen44": screen44, "cloud": cloud}

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        if holding:
            apple_x = rat_x
            apple_y = rat_y
            holding = False
        sprinting = True
        sprint.move_rat()
    else:
        sprinting = False
        normal.move_rat()

    # Display the current screen
    for i in screens:
        if current_screen == i:
            screen_variables[i].check_if_new_screen()

    if holding:
        apple_screen = current_screen
        
    # Draw the screen
    draw_screen()

    # Cap the frame rate
    clock.tick(60)

# Close the database connection
conn.close()

# Quit Pygame
pygame.quit()
sys.exit()
