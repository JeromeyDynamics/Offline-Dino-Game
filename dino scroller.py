import pygame
from pygame.locals import QUIT
import random  # Import random for cactus spawning

pygame.init()

width = 800
length = 400

screen = pygame.display.set_mode((width, length))
pygame.display.set_caption('Dinosaur Run!')

#background
background_img = pygame.image.load('bg.png')
background_x = 0
background_speed = 4  # Slightly faster background scrolling

#Create list with dinosaur images
dinosaur_imgs = [
  pygame.image.load('dino0.png'),
  pygame.image.load('dino1.png'),
  pygame.image.load('dino2.png')
]

#load in cactus image
cactus_img = pygame.transform.scale(pygame.image.load('cactus.png'), (40,60))

dinosaur_x = 80
dinosaur_y = 130
cactus_speed = 4      # Consistent cactus speed
cactus_x = 800        # Spawn the first cactus farther away
cactus_y = 170

#animation variable
dinosaur_frame = 0 #which frame of the dino is displayed
dinosaur_anim_speed = 0.08  # Slower animation for a more relaxed pace
dinosaur_last_update = 0

# Jumping variables
is_jumping = False
jump_velocity = -5  # Reduced upward velocity for a flatter jump
gravity = 0.1       # Reduced gravity for a slower descent

#score variable
score = 0
font = pygame.font.Font('freesansbold.ttf', 30)

# Multiple cactus spawning logic
cactus_positions = []  # List to hold multiple cactus positions

# Function to spawn cacti
def spawn_cacti():
    global cactus_positions
    cactus_positions = []
    num_cacti = random.choices([1, 2, 3], weights=[70, 25, 5])[0]  # 70% chance for 1, 25% for 2, 5% for 3
    base_position = cactus_x  # Start position for the first cactus
    for i in range(num_cacti):
        offset = random.randint(15, 50)  # Small random spacing between cacti
        cactus_positions.append(base_position + i * offset)

# Spawn initial cacti
spawn_cacti()

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            if not is_jumping:
              is_jumping = True

    #scroll the background
    background_x -= background_speed
    if background_x <= -background_img.get_width():
      background_x = 0 

    #move the cactus
    for i in range(len(cactus_positions)):
        cactus_positions[i] -= cactus_speed
    if all(pos <= -cactus_img.get_width() for pos in cactus_positions):
        spawn_cacti()
        score += 1

    #animate the dinosaur
    current_time = pygame.time.get_ticks() #current time
    if current_time-dinosaur_last_update>dinosaur_anim_speed*1000:
      dinosaur_frame = (dinosaur_frame+1)%len(dinosaur_imgs)
      dinosaur_last_update = current_time

    #perform the jump
    if is_jumping:
      dinosaur_y += jump_velocity
      jump_velocity += gravity  # Use the adjusted gravity value

      if dinosaur_y >= 130:
          is_jumping = False
          dinosaur_y = 130
          jump_velocity = -5  # Reset jump velocity to the initial value

    #check for collision
    for pos in cactus_positions:
        cactus_rect = cactus_img.get_rect(topleft= (pos+25, cactus_y+25))
        dinosaur_rect = dinosaur_imgs[dinosaur_frame].get_rect(topleft= (dinosaur_x, dinosaur_y))
        if dinosaur_rect.colliderect(cactus_rect):
          running = False

    # Increase cactus speed as the score increases
    cactus_speed = 4 + (score // 10) * 0.1  # Gradual speed increase every 10 points

#display the sprites
    #display the background
    screen.blit(background_img, (background_x, 0))
    screen.blit(background_img, (background_x + background_img.get_width(),0))

    #display the dinosaur
    screen.blit(dinosaur_imgs[dinosaur_frame], (dinosaur_x, dinosaur_y))

    #display the cactus
    for pos in cactus_positions:
        screen.blit(cactus_img, (pos, cactus_y))

    #display the score
    score_text = font.render("score: "+ str(score), True, (0,0,0))
    screen.blit(score_text, (10,10))

    pygame.display.flip()