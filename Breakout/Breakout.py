# Example file showing a circle moving on screen
import pygame
import random


# pygame setup
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("pixel_music.mp3")
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# basic variables 
ball_pos = pygame.Vector2(screen.get_width() / 2.5, screen.get_height() -200)
ball_speed = pygame.Vector2(200, 200)
player_size = pygame.Vector2(120, 30)
player_pos = pygame.Vector2((screen.get_width() / 2)-60, screen.get_height()-50)
block_pos = pygame.Vector2(screen.get_width() / 10, screen.get_height() / 10)
block_size = pygame.Vector2(128,50)
end_counter = 0

lose_image = pygame.image.load('Lose.png').convert_alpha() 
win_image = pygame.image.load('Win.png').convert_alpha() 

lose_rect = lose_image.get_rect()
lose_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

win_rect = win_image.get_rect()
win_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

# code that makes the ball bounce
def check_boundry_ball():
    if ball_pos.x < 0 or ball_pos.x > screen.get_width()-40:
        ball_speed.x *= -1
    
    if ball_pos.y < 0 or ball_pos.y > screen.get_height()-50:
        ball_speed.y *= -1

# Player Code
def player_code():
    # Keeps player in bounds
    if player_pos.x > 40:
        left_valid = True
    if player_pos.x < screen.get_width()-160:
        right_valid = True
        # False cases
    if player_pos.x <= 40:
        left_valid = False
    if player_pos.x >= screen.get_width()-160:
        right_valid = False

    # Player movment
    keys = pygame.key.get_pressed()
    if left_valid == True:
        if keys[pygame.K_a]:
            player_pos.x -= 800 * dt
    if right_valid == True:
        if keys[pygame.K_d]:
            player_pos.x += 800 * dt

#Ball player interaction
def check_ball_player_collision():
    #print(f"ball: {ball_pos.x}, {ball_pos.y}")
    #print(f"player: {player_pos.x},  {player_pos.y}")
#    if ball_pos.x+20 <= player_pos.x +120 and ball_pos.x+20 >= player_pos.x and ball_pos.y-20 >= player_pos.y-50:
#        ball_speed.y *= -1
    paddle_width = 120
    ball_radius = 20

    if (ball_pos.x + ball_radius <= player_pos.x + paddle_width and
        ball_pos.x + ball_radius >= player_pos.x and
        ball_pos.y - ball_radius >= player_pos.y - 50):

        # Reverse vertical direction
        ball_speed.y *= -1

        # Find paddle center
        paddle_center = player_pos.x + paddle_width / 2

        # Distance from center
        offset = (ball_pos.x - paddle_center)

        # Normalize (-1 to 1 range)
        normalized = offset / (paddle_width / 2)

        # Change X speed based on hit location
        max_x_speed = 600  # adjust for feel
        ball_speed.x = normalized * max_x_speed




#Game over
def delete_ball():
    if ball_pos.y >670:
        screen.fill("black")
        ball_speed.x *= 0
        ball_speed.y *= 0
        bricks.clear()
        screen.blit(lose_image, lose_rect)
        show_rect = False

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                print("CLICK")
    else:
        show_rect = True
    return show_rect
 
def brick():
    for brick in bricks:
        pygame.draw.rect(screen, (211,211,211), brick, 0, 10) 

def end():
    if end_counter == rows*cols:
        screen.fill("black")
        ball_speed.x *= 0
        ball_speed.y *= 0
        bricks.clear()
        screen.blit(win_image, win_rect)
        return False
    return True

rows = 5
cols = 8    

bricks = []  # list to store all brick rects

for row in range(rows):
    for col in range(cols):
        x = col * (block_size.x + 10) + 110
        y = row * (block_size.y + 10) + 110

        rect = pygame.Rect(x, y, block_size.x, block_size.y)
        bricks.append(rect)

    #screen.blit(win_image, win_rect)


#Main
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((28,24,31))

    #returns T/F
    
    
#player
    pygame.draw.rect(screen, (211,211,211), ((player_pos),(player_size.x, player_size.y)), 0, 10)

    
    show_ball = end()

    if show_ball:
        show_ball = delete_ball()

    if show_ball:
        ball_pos.y += ball_speed.y * dt
        ball_pos.x += ball_speed.x * dt
        
        check_boundry_ball()
        player_code()
        check_ball_player_collision()
        brick()
        ball_rect = pygame.draw.rect(screen, (211,211,211), ((ball_pos),(40,40)), 0, 100)


        for i in bricks:
            if ball_rect.colliderect(i):
                bricks.remove(i)
                ball_speed.y *= -1
                end_counter += 1
                break   
    else:
        player_code()
        brick()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()