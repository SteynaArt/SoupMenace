 # game data

# meow meow

#from argparse import Action
from random import randint
from pgzero.actor import Actor
import pgzrun
# coucou ça merge ? CONFLIT
# hero initialisation
import pygame # for introscreen time count

WIDTH = 800
HEIGHT = 600

#game phtsics & settings - Groung & Gravity
GROUND = 500 # y-position hero stand here (height 600)
GRAVITY = 200 #Pulls the hero downward after jumping

NUMBER_OF_BACKGROUND = 2  #2 bg
GAME_SPEED = 100 # speed of game movement

JUMP_SPEED = 200 #upward speed when hero jump
JUMP_HEIGHT = 360 #height of the hero's jump

game_state = "intro"
start_time = 0
game_over = False
win = False

#1.Anemy box movement up-down 
KNIFE_UP_DOWN_SPEED = 120 # speed of box up-down movement
KNIFE_MIN_HEIGHT = 20 # minimum height box can go up
KNIFE_MAX_HEIGHT = 300 # maximum height box can go up

# enemies initialisations
KNIFE_APPARTION = (5, 9) # enemy boxes appear every 2 to 5 second rendomly
next_knife_time = randint(KNIFE_APPARTION[0], KNIFE_APPARTION[1])  #Chooses random starting spawn time
knifes = []

# Pot / Pots list init
BOX_APPARTION = (2, 8)
next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])
box = Actor("pot2", anchor=('left', 'bottom'))
box.pos = WIDTH, GROUND
boxes = []

box_image = ["pot2", "pot_c"]
box_image_index = 0

def animate_box():
    global box_image_index
    box_image_index += 1 
    if box_image_index >= len(box_image):
        box_image_index = 0
    box.image = box_image[box_image_index]

clock.schedule_interval(animate_box, 0.4)

#---------------------------- hero initialisation-------------------------
hero = Actor("leek1", anchor=('right', 'bottom')) # here leek1 is starting image
hero.pos = (200, GROUND) #place hero at x = 64, y = G
hero_speed = 0 #means hero can not move vertically

hero_image = ["leek1", "leek2", "leek3"]  #these 3 image stored for animation(gif)
hero_image_index = 0 #use this variable for hero,This keeps track of which image is currently being shown.

def animate_hero():#Defines a function that changes the hero’s image
    global hero_image_index #Without global, Python would think image_index is a new local variable inside the function.
    hero_image_index += 1 #each time moves to nex image frame,0 -> 1-> 2->....
    if hero_image_index >= len(hero_image): # hero img. 3 - it will valid until image_index reset back to 0
        hero_image_index = 0
    hero.image = hero_image[hero_image_index] #change the hero current image

clock.schedule_interval(animate_hero, 0.2) #every 0.2 seconds, play the function "animate_hero"


gameover_bg = Actor("gameover_bg", anchor=('middle', 'bottom'))
win_bg = Actor("win_bg", anchor=('middle', 'bottom'))

#------------------------------------------ CAT SPRITES ------------------------------------------------

cat = Actor("cat1", anchor=('middle', 'bottom')) 
cat.pos = (-200, 365) 

cat_sprite = ["cat1", "cat2", "cat3", "cat4", "cat5"]
cat_sprite_index = 0

def animate_cat():
    global cat_sprite_index
    cat_sprite_index += 1
    if cat_sprite_index >= len(cat_sprite):
        cat_sprite_index = 0
    cat.image = cat_sprite[cat_sprite_index]

clock.schedule_interval(animate_cat, 0.3) 

#---------------------------------------Life Sprite---------------------------------------------------------

#life count
heart = Actor("heart")
live = 3 #lives variable
score = 0 # create a score variable
win_score = 10 #win/game over settings


# background inititalisation

backgrounds_bottom = []
backgrounds_top = []

for n in range(NUMBER_OF_BACKGROUND):#run twice becz. number of bg = 2 bg
    bg_b = Actor("table", anchor=('left', 'top')) #bottom bg
    bg_b.pos = (n * WIDTH, 0)
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("kitchen_background", anchor=('left', 'top')) # bg top
    bg_t.pos = (n * WIDTH, 0)
    backgrounds_top.append(bg_t)



def draw():
    screen.clear()

    for bg in backgrounds_bottom:
        bg.draw()

    for bg in backgrounds_top:
        bg.draw()
    
    if game_state == "intro":
        screen.draw.text("SoupMenace", center=(WIDTH/2, HEIGHT/3.1), fontname="nirakolu", fontsize=60, color="hotpink")
        screen.draw.text("LEZGO", center=(WIDTH/2, HEIGHT/2), fontname="nirakolu", fontsize=90, color="plum1")
        screen.draw.text("Little leek, you might end up in tonight soup \n Get awaaaay", center=(WIDTH/2, HEIGHT/1.3), fontname="nirakolu", fontsize=25, color="yellow2")

    elif game_state == "game":
        cat.draw()
        hero.draw()

        for box in boxes:
            box.draw()

        for knife in knifes:
            knife.draw()

        #Life(heart)position 
        for i in range(live):
            heart.pos = (WIDTH - 30 - i*30,30)# last 30 is height consider top right (-30 is bottom right)
            #heart.width = 25
            #heart.height = 25
            heart.draw()
        
        ###draw score
        screen.draw.text(
            "Score: " + str(score), 
            (10, 10), color="white", 
            fontsize=30)
        
    if game_over == True:
        gameover_bg.draw()
        screen.draw.text("GAME", center=(WIDTH/2, HEIGHT/3), fontname="nirakolu", fontsize=80, color="plum1")
        screen.draw.text("OVER", center=(WIDTH/2, HEIGHT/2.01), fontname="nirakolu", fontsize=60, color="black")
        
    if win == True:
        win_bg.draw()
        screen.draw.text("You", center=(WIDTH/2, HEIGHT/3), fontname="nirakolu", fontsize=80, color="plum1")
        screen.draw.text("WIIIN", center=(WIDTH/2, HEIGHT/2.01), fontname="nirakolu", fontsize=100, color="hotpink")
        
   

# ---------------- UPDATE ----------------
def update(dt):

    global box, next_box_time, next_knife_time, hero_speed, live, score, game_over, win

    if game_state == "intro":
        introscreen()
        return
    
    if game_state == "win":
        win()
        return
    
    next_box_time -= dt
    next_knife_time -= dt

    for i in cat:
        x, y = cat.pos
        x -= GAME_SPEED/8 * -dt
        cat.pos = x, y
    

    if next_knife_time <= 0:
        knife = Actor("knife", anchor=('left', 'bottom'))
        knife.pos = (WIDTH, GROUND)

         # 2.Enemy OX RANDOM UP-DOWN MOVEMENT
        knife.direction = -1 # -1 means box starts going up first
        knife.jump_height = randint(KNIFE_MIN_HEIGHT,KNIFE_MAX_HEIGHT) # each box gets different height
        knifes.append(knife)
        next_knife_time = randint(KNIFE_APPARTION[0], KNIFE_APPARTION[1])

    # ---------------- UPDATE KNIVES ----------------
    for knife in knifes[:]: #for each box inside this loop, box1,box2..
        x, y = knife.pos
        x -= GAME_SPEED * dt

        #Box random up-down movement, box goes-up
        y += knife.direction * KNIFE_UP_DOWN_SPEED * dt #Move box up-down

         # If box reaches its own random top height, then move down
        if y <= GROUND - knife.jump_height:
            y = GROUND - knife.jump_height
            knife.direction = 1
       
       # If box reaches ground again, then move up
        if y >= GROUND:
            y = GROUND
            knife.direction = -1

        knife.pos = (x, y)
        a, b = hero.pos
        if knife.colliderect(hero):
            live -= 1
            knifes.remove(knife)

            if live == 0 :
                game_over = True
        
        elif knife.pos[0] <= -32: # elif knife.x <= -50:
            knifes.remove(knife)
            score += 1
            if score == 10:
                win = True
    # ---------------- SPAWN BOX ----------------
    if next_box_time <= 0:
        boxes.append(box)
        next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])


    for box in boxes[:]:
        x, y = box.pos
        x -= GAME_SPEED * dt
        box.pos = x, y
        a, b = hero.pos

        if box.pos[0] <= -32: 
            boxes.remove(box)
            score += 1
            if score == 10:
                    win = True    
        elif box.pos[0] <= -32: #elif box.x <= -50:
            boxes.remove(box)
        elif box.colliderect(hero):
            a = x
            #si les deux se rencotrent, la position y hero et la même que y box
            hero.pos = a,b
            if a < -29:
                game_over = True

    ### hero update
    #global hero_speed
    hero_speed -= GRAVITY * dt
    x, y = hero.pos
    y -= hero_speed * dt

    if y > GROUND:
        y = GROUND
        hero_speed = 0

    hero.pos = x, y

    # bg update
    for bg in backgrounds_bottom:
        x, y = bg.pos
        x -= GAME_SPEED * dt
        bg.pos = x, y

    if backgrounds_bottom[0].pos[0] <= - WIDTH:
        bg = backgrounds_bottom.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_bottom.append(bg)

    for bg in backgrounds_top:
        x, y = bg.pos
        x -= GAME_SPEED/3 * dt
        bg.pos = x, y

    if backgrounds_top[0].pos[0] <= - WIDTH:
        bg = backgrounds_top.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_top.append(bg)


secondjump = False
jump = False
nbjumps = 0

def on_key_down(key):
    global hero_speed, nbjumps

    if hero.y == GROUND:
        nbjumps = 0

    if (key == keys.SPACE) :
        if (hero.y == GROUND): # the single jump
            hero_speed = JUMP_HEIGHT
            nbjumps += 1
    
        elif hero.y < GROUND :
            if nbjumps == 1:
                hero_speed = JUMP_HEIGHT/2 # the double jump
                nbjumps += 1
            elif nbjumps >= 2:
                pass
    


# Game states for making the screens
def introscreen():
    global game_state
    if pygame.time.get_ticks() - start_time > 6000:
        game_state = "game"

def win():
    global game_state
    if (score == 3):
        game_state = "win"

# def gameover():
#     global game_state
#     if 
#         game_state = "over"


pgzrun.go()