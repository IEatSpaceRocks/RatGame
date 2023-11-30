import pygame
import sys
import os
import sqlite3
import random

os.environ['SOL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption("Rat")

Info = pygame.display.Info()
ScreenWidth, ScreenHeight = Info.current_w, Info.current_h

# Change the current working directory to the folder where your script is located
script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

# SQLite Database
conn = sqlite3.connect('game_database.db')
cursor = conn.cursor()
conn.commit()

# Set up display
SCREEN = pygame.display.set_mode((900, 800), pygame.RESIZABLE)









class Image():
    def __init__(self, Image):
        self.Image = pygame.image.load(rf"Images/{Image}.png").convert_alpha()
        self.Rect = self.Image.get_rect()
        self.Mask = pygame.mask.from_surface(self.Image)

class RatStats():
    def __init__(self, x, y, Speed, Holding, Sprinting, Facing, Health):
        self.x = x
        self.y = y
        self.Speed = Speed
        self.Holding = Holding
        self.Sprinting = Sprinting
        self.Facing = Facing
        self.Health = Health
        
BACKGROUNDS = [
    Image("background_1"), Image("background_2"), Image("background_3"), Image("background_4"),
    Image("background_5"), Image("background_6"), Image("background_7"), Image("background_8"),
    Image("background_9"), Image("background_10"), Image("background_11"), Image("background_12"),
    Image("background_13"), Image("background_14"), Image("background_15"), Image("background_16"),
    Image("background_17"), Image("background_18"), Image("background_19")
]
Apple = Image("apple")
Blackberry = Image("blackberry")
AppleTree = Image("tree_apple")
BlackberryBush = Image("bush_blackberry")
AppleTreeMirrored = Image("tree_apple2")
BlackberryBushMirrored = Image("bush_blackberry2")
PickBerries = Image("pick_berries")
RatStandard = [Image("rat_1"), Image("rat_2")]
RatApple = [Image("rat_1_apple"), Image("rat_2_apple")]
RatBlackberry = [Image("rat_1_blackberry"), Image("rat_2_blackberry")]
RatSprinting = [Image("rat_3"), Image("rat_4")]

Tick = 0
InBush = False
CurrentRatImage = RatStandard
Items = []
CurrentScreen = "main"
CurrentBackground = BACKGROUNDS[0]

Rat = RatStats(400, 400, 4, False, False, 0, 100)









def new_screen():
    cursor.execute("INSERT INTO player_data (screen, x, y) VALUES (?, ?, ?)", ("main", Rat.x, Rat.y))
    conn.commit()

def update_rat():
    global CurrentRatImage
    OldRatImageRect = CurrentRatImage[Rat.Facing].Rect.copy()
    CurrentRatImage[Rat.Facing].Mask = pygame.mask.from_surface(CurrentRatImage[Rat.Facing].Image)
    CurrentRatImage[Rat.Facing].Rect = CurrentRatImage[Rat.Facing].Image.get_rect()
    pygame.display.update([OldRatImageRect, CurrentRatImage[Rat.Facing].Rect])
    pygame.display.update([Rat.x - 40, Rat.y - 60, 80, 120])
    
def screen_up():
    if Rat.y <= 20:
        new_screen()
        Rat.y = 778
        return True
    
def screen_down():
    if Rat.y >= 780:
        new_screen()
        Rat.y = 22
        return True
    
def screen_left():
    if Rat.x <= 20:
        new_screen()
        Rat.x = 778
        return True
    
def screen_right():
    if Rat.x >= 780:
        new_screen()
        Rat.x = 22
        return True

def move_rat():
    global CurrentRatImage
    if Rat.Sprinting:
        CurrentRatImage = RatSprinting
    elif Rat.Sprinting == False and Rat.Holding == False:
        CurrentRatImage = RatStandard

    if key[pygame.K_a] and Rat.x > 20:
        Rat.x -= Rat.Speed
        Rat.Facing = 0
        update_rat()

    if key[pygame.K_d] and Rat.x < 780:
        Rat.x += Rat.Speed
        Rat.Facing = 1
        update_rat()

    if key[pygame.K_w] and Rat.y > 20:
        Rat.y -= Rat.Speed
        update_rat()

    if key[pygame.K_s] and Rat.y < 780:
        Rat.y += Rat.Speed
        update_rat()









class Item():

    def __init__(self, Image, x, y, Screen, RatImage, Holding):

        self.Image = Image
        self.x = x
        self.y = y
        self.Screen = Screen
        self.RatImage = RatImage
        self.Holding = Holding

    def check_item(self):
        global CurrentRatImage
        if self.Holding:
            self.Screen = CurrentScreen
            self.x = Rat.x
            self.y = Rat.y
        if self.Holding and Rat.Sprinting:
            self.Holding = False
        if CurrentScreen == self.Screen:
            if CurrentRatImage[Rat.Facing].Mask.overlap(self.Image.Mask, (self.Image.Rect.x  - CurrentRatImage[Rat.Facing].Rect.x + self.x, self.Image.Rect.y  - CurrentRatImage[Rat.Facing].Rect.y + self.y)) and Rat.Sprinting == False and Rat.Holding == False:
                CurrentRatImage = self.RatImage
                self.Holding, Rat.Holding = True, True
                draw_screen()
            if self.Holding == False:
                SCREEN.blit(self.Image.Image, (self.x, self.y))

def new_item(Image, FromX, RangeX, FromY, RangeY, Screen, RatImage):
                    NewItem = Item(Image, rand(0, RangeX) + FromX, rand(0, RangeY) + FromY, Screen, RatImage, False)
                    Items.append(NewItem)









class screen():

    def __init__(self, Up, Down, Left, Right, Type, Background):
        self.Up = Up
        self.Down = Down
        self.Left = Left
        self.Right = Right
        self.Type = Type
        self.Background = Background
        self.ListY = []
        self.ListX = []
        self.Facing = []

    def check_if_new_screen(self):
        global CurrentScreen
        if self.Up and screen_up():
            CurrentScreen = self.Up
        elif self.Down and screen_down():
            CurrentScreen = self.Down
        elif self.Left and screen_left():
            CurrentScreen = self.Left
        elif self.Right and screen_right():
            CurrentScreen = self.Right

def update_screen():
    global CurrentBackground, InBush
    CurrentBackground = BACKGROUNDS[ScreenVariables[CurrentScreen].Background]
    if ScreenVariables[CurrentScreen].Type == 1:
        for X, Y, Facing in zip(ScreenVariables[CurrentScreen].ListX, ScreenVariables[CurrentScreen].ListY, ScreenVariables[CurrentScreen].Facing):
            if Facing == 0:
                if CurrentRatImage[Rat.Facing].Mask.overlap(AppleTree.Mask, (AppleTree.Rect.x - CurrentRatImage[Rat.Facing].Rect.x + X, AppleTree.Rect.y - CurrentRatImage[Rat.Facing].Rect.y + Y)):
                    AppleTree.Image.set_alpha(128)
                    SCREEN.blit(AppleTree.Image, (X, Y))
                else:
                    AppleTree.Image.set_alpha(256)
                    SCREEN.blit(AppleTree.Image, (X, Y))
            else:
                if CurrentRatImage[Rat.Facing].Mask.overlap(AppleTreeMirrored.Mask, (AppleTreeMirrored.Rect.x - CurrentRatImage[Rat.Facing].Rect.x + X, AppleTreeMirrored.Rect.y - CurrentRatImage[Rat.Facing].Rect.y + Y)):
                    AppleTreeMirrored.Image.set_alpha(128)
                    SCREEN.blit(AppleTreeMirrored.Image, (X, Y))
                else:
                    AppleTreeMirrored.Image.set_alpha(256)
                    SCREEN.blit(AppleTreeMirrored.Image, (X, Y))
    if ScreenVariables[CurrentScreen].Type == 2:
        InBush = False
        for X, Y, Facing in zip(ScreenVariables[CurrentScreen].ListX, ScreenVariables[CurrentScreen].ListY, ScreenVariables[CurrentScreen].Facing):
            if Facing == 0:
                if CurrentRatImage[Rat.Facing].Mask.overlap(BlackberryBush.Mask, (BlackberryBush.Rect.x - CurrentRatImage[Rat.Facing].Rect.x + X, BlackberryBush.Rect.y - CurrentRatImage[Rat.Facing].Rect.y + Y)):
                    BlackberryBush.Image.set_alpha(128)
                    SCREEN.blit(BlackberryBush.Image, (X, Y))
                    InBush = True
                else:
                    BlackberryBush.Image.set_alpha(256)
                    SCREEN.blit(BlackberryBush.Image, (X, Y))
            else:
                if CurrentRatImage[Rat.Facing].Mask.overlap(BlackberryBushMirrored.Mask, (BlackberryBushMirrored.Rect.x - CurrentRatImage[Rat.Facing].Rect.x + X, BlackberryBushMirrored.Rect.y - CurrentRatImage[Rat.Facing].Rect.y + Y)):
                    BlackberryBushMirrored.Image.set_alpha(128)
                    SCREEN.blit(BlackberryBushMirrored.Image, (X, Y))
                    InBush = True
                else:
                    BlackberryBushMirrored.Image.set_alpha(256)
                    SCREEN.blit(BlackberryBushMirrored.Image, (X, Y))
                

def rand(From, To):
    return random.randint(From, To)

main = screen(None, None, None, "screen11", 0, 0)
screen11 = screen(None, "screen21", "main", "screen12", rand(0, 3), rand(0, 18))
screen12 = screen(None, "screen22", "screen11", "screen13", rand(0, 3), rand(0, 18))
screen13 = screen(None, "screen23", "screen12", "screen14", rand(0, 3), rand(0, 18))
screen14 = screen(None, "screen24", "screen13", None, rand(0, 3), rand(0, 18))
screen21 = screen("screen11", "screen31", None, "screen22", rand(0, 3), rand(0, 18))
screen22 = screen("screen12", "screen32", "screen21", "screen23", rand(0, 3), rand(0, 18))
screen23 = screen("screen13", "screen33", "screen22", "screen24", rand(0, 3), rand(0, 18))
screen24 = screen("screen14", "screen34", "screen23", None, rand(0, 3), rand(0, 18))
screen31 = screen("screen21", "screen41", None, "screen32", rand(0, 3), rand(0, 18))
screen32 = screen("screen22", "screen42", "screen31", "screen33", rand(0, 3), rand(0, 18))
screen33 = screen("screen23", "screen43", "screen32", "screen34", rand(0, 3), rand(0, 18))
screen34 = screen("screen24", "screen44", "screen33", None, rand(0, 3), rand(0, 18))
screen41 = screen("screen31", None, None, "screen42", rand(0, 3), rand(0, 18))
screen42 = screen("screen32", None, "screen41", "screen43", rand(0, 3), rand(0, 18))
screen43 = screen("screen33", None, "screen42", "screen44", rand(0, 3), rand(0, 18))
screen44 = screen("screen34", None, "screen43", "cloud", rand(0, 3), rand(0, 18))
cloud = screen(None, None, "screen44", None, 0, 0)

Screens = ["main", "screen11", "screen12", "screen13", "screen14", "screen21", "screen22", "screen23", "screen24", "screen31", "screen32", "screen33", "screen34", "screen41", "screen42", "screen43", "screen44", "cloud"]
ScreenVariables = {"main": main, "screen11": screen11, "screen12": screen12, "screen13": screen13, "screen14": screen14, "screen21": screen21, "screen22": screen22, "screen23": screen23, "screen24": screen24, "screen31": screen31, "screen32": screen32, "screen33": screen33, "screen34": screen34, "screen41": screen41, "screen42": screen42, "screen43": screen43, "screen44": screen44, "cloud": cloud}

for Screen in Screens:
    if ScreenVariables[Screen].Type == 1:
        ScreenVariables[Screen].ListX.append(rand(0, 200))
        ScreenVariables[Screen].ListY.append(rand(0, 200))
        ScreenVariables[Screen].Facing.append(rand(0, 1))
    if ScreenVariables[Screen].Type == 2:
        for i in range(rand(5, 8)):
            ScreenVariables[Screen].ListX.append(40 + 30 * rand(0, 11))
            ScreenVariables[Screen].ListY.append(30 + 30 * rand(0, 18))
            ScreenVariables[Screen].Facing.append(rand(0, 1))
        ScreenVariables[Screen].ListY.sort()

for Screen in Screens:
    print(Screen)
    print(f"Layout{ScreenVariables[Screen].Type}")
    print(f"Back{ScreenVariables[Screen].Background}")
    print("---------------------------")









def draw_screen():
    pygame.draw.rect(SCREEN, (139, 69, 19), (0, 0, ScreenWidth, ScreenHeight))

    # Clear the screen
    if CurrentScreen == "cloud":
        SCREEN.fill((0, 0, 0))
    else:
        SCREEN.blit(CurrentBackground.Image, (0, 0))

    CurrentRatImage[Rat.Facing].Rect.center = (Rat.x, Rat.y)

    for item in Items:
        item.check_item()
    
    # Draw the image on the screen
    SCREEN.blit(CurrentRatImage[Rat.Facing].Image, CurrentRatImage[Rat.Facing].Rect.topleft)

    update_screen()

    pygame.draw.rect(SCREEN, (211, 211, 211),(Rat.x - 26, Rat.y - 41, 52, 12))
    pygame.draw.rect(SCREEN, (0, 255, 0), (Rat.x - 25, Rat.y - 40, Rat.Health / 2, 10))

    pygame.draw.rect(SCREEN, (139, 69, 19), (800, 0, 100, 800))
    number = 28
    for i in range(10):
        pygame.draw.rect(SCREEN, (192, 163, 187), (825, number, 52, 52))
        number += 77

    pygame.display.flip()









# Game loop
running = True
while running:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False

    if key[pygame.K_SPACE]:
        Rat.Sprinting = True
        Rat.Holding = False
        Rat.Speed = 8
    else:
        Rat.Sprinting = False
        Rat.Speed = 4

    if InBush:
        Rat.Speed /= 2
        if Tick % 12 == 0:
            Rat.Health -= 1

    move_rat()

    # Display the current screen
    for Screen in Screens:
        if CurrentScreen == Screen:
            ScreenVariables[Screen].check_if_new_screen()
        if ScreenVariables[Screen].Type == 1:
            if Tick % 900 == 0:
                for X, Y in zip(ScreenVariables[Screen].ListX, ScreenVariables[Screen].ListY):
                    new_item(Apple, X + 10, 580, Y + 500, 100, Screen, RatApple)

    Tick += 1
        
    if Rat.Health == 0:
        CurrentScreen = "main"
        Rat.Health = 100
        Rat.x, Rat.y = 400, 400
        CurrentRatImage = RatStandard
        InBush = False
        for i in Items:
            i.Holding = False

    # Draw the screen
    draw_screen()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Close the database connection
conn.close()

# Quit Pygame
pygame.quit()
sys.exit()
