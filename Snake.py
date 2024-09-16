import pygame
import random
import sys
import os

# Get the path to the resource, whether running as a bundled exe or from the source code
def resource_path(relative_path):
    try:
        # PyInstaller stores files in a temporary folder when bundled
        base_path = sys._MEIPASS
    except AttributeError:
        # When running from source, the base path is the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Function to set or reset the game's default state
def set_game():
    global snake_position, snake, direction, change_to, score, x_apple, y_apple, record
    snake_position = [100, 50]
    snake = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    change_to = direction
    score = 0
    record = get_record()
    x_apple = random.randint(0, (x_window // 10) - 1) * 10
    y_apple = random.randint(0, (y_window // 10) - 2) * 10
    pygame.mixer.music.play(-1)  # Restart the background music

#Getting the record from the text file
def get_record():
    record_file_path = resource_path('recordBook.txt')
    with open(record_file_path, 'r') as file_reader:
            file_reader.seek(9)
            runing = 5
            record_string = ""
            while runing > 0:
                char = file_reader.read(1)
                if char != " ":
                    record_string += char
                runing -= 1
            record = int(record_string)
    return record

# Initialising pygame (+ sounds and font)
pygame.init()
pygame.mixer.init()
pygame.font.init()

# defining colors
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(255,255,255)
pink = pygame.Color(255,70,150)

#Initilise all the variables referring to the sounds of the game
apple_pickup_sound_path = resource_path('sounds/apple_pickup_sound.wav')
apple_pickup_sound = pygame.mixer.Sound(apple_pickup_sound_path)

game_over_sound_path = resource_path('sounds/game_over_sound.wav')
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

paused_resume_sound_path = resource_path('sounds/paused_resume_sound.wav')
paused_resume_sound = pygame.mixer.Sound(paused_resume_sound_path)

game_music_path = resource_path('sounds/game_music.wav')
pygame.mixer.music.load(game_music_path)

#Initializing game window size
x_window = 300
y_window = 200

# FPS (frames per second) controller
fps = pygame.time.Clock()
snake_speed = 15

#Call the function to set default game's state
set_game()

#Function to print the score and the record
def show_score(game_window, score):
    # Initialize the font
    pygame.font.init()
    fontt = pygame.font.Font('freesansbold.ttf', 15)
    
    
    # Render the text
    text = fontt.render(f'{score} pts', True, blue)
    text2 = fontt.render(f'Record: {record} pts', True, blue)
    
    # Get the rectangle for positioning
    textRect = text.get_rect()
    textRect.center = (20,10)

    textRect2 = text2.get_rect()
    textRect2.center = (150,10)
    
    # Blit the text onto the window
    game_window.blit(text, textRect)
    game_window.blit(text2, textRect2)
    
    # Update the display to show the text
    pygame.display.update()

#Function to pause the game
def game_paused(game_window):
    pygame.mixer.music.stop()
    paused_resume_sound.play()
    # Initialize the font
    pygame.font.init()
    fontt = pygame.font.Font('freesansbold.ttf', 32)
    font2 = pygame.font.Font('freesansbold.ttf', 12)
    
    
    # Render the text
    text = fontt.render(f'Paused', True, pink)
    text2 = font2.render(f'press r to resume or e to exit', True, white)
    
    # Get the rectangle for positioning
    textRect = text.get_rect()
    textRect.center = (x_window // 2, y_window // 2)

    textRect2 = text2.get_rect()
    textRect2.center = (150, 190)
    
    # Blit the text onto the window
    game_window.blit(text, textRect)
    game_window.blit(text2, textRect2)
    
    # Update the display to show the text
    pygame.display.update()
    is_paused = True
    while is_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'r' to resume
                    pygame.time.wait(300)# Wait for the player to be ready
                    paused_resume_sound.play()
                    pygame.mixer.music.play(-1)
                    is_paused = False
                if event.key == pygame.K_e:  # Press 'e' to exit
                    pygame.quit()
                    sys.exit()

#Function stop the game and print the game over message
def game_over(game_window, score, record):

    pygame.mixer.music.stop()
    game_over_sound.play()
    # Initialize the font
    font1 = pygame.font.Font('freesansbold.ttf', 32)
    font2 = pygame.font.Font('freesansbold.ttf', 19)
    font3 = pygame.font.Font('freesansbold.ttf', 12)
    
    # Render the text
    text1 = font1.render("You died", True, red)
    text2 = font2.render(f'you scored {score} pts', True, white)
    text3 = font2.render(f'Record {record} pts', True, white)
    text4 = font3.render(f'press r to restart or e to exit', True, white)
    # Get the rectangle for positioning
    textRect1 = text1.get_rect()
    textRect1.center = (x_window // 2, y_window // 2)
    textRect2 = text2.get_rect()
    textRect2.center = (x_window // 2 - 4, y_window // 2 + 30)
    textRect3 = text3.get_rect()
    textRect3.center = (x_window // 2 - 5, y_window // 2 + 50)
    textRect4 = text4.get_rect()
    textRect4.center = (150, 190)
    
    # Blit the text onto the window
    game_window.blit(text1, textRect1)
    game_window.blit(text2, textRect2)
    game_window.blit(text3, textRect3)
    game_window.blit(text4, textRect4)
    
    # Update the display to show the text
    pygame.display.update()
    record_file_path = resource_path('recordBook.txt')
    if score > record:
        with open(record_file_path, 'w') as file:
            score_str = "Record : "+str(score)
            file.write(score_str)

    # Wait for a short time to let the user see the message
    run = True
    while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press 'r' to restart
                        set_game()
                        run = False
                    if event.key == pygame.K_e:  # Press 'e' to exit
                        pygame.quit()
                        sys.exit()
   
#Creating game window
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((x_window, y_window))

#Game loop
while True :

    #Handeling events
    for event in pygame.event.get():

        # Check if a key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                change_to = "LEFT"
            if event.key == pygame.K_d:
                change_to = "RIGHT"
            if event.key == pygame.K_z:
                change_to = "UP"
            if event.key == pygame.K_s:
                change_to = "DOWN"
            if event.key == pygame.K_ESCAPE:
                game_paused(game_window)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Making sure that the snake can't go 
    #into the opposite direction and modify
    #the direction if it's ok 
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10


    #Updating the snake (adding a rect in the direction the snake is going)
    snake.insert(0, list(snake_position))
    
    #If the apple is where the head of the snake is update score, 
    #generate new x y for the apple and don't pop the last rect of the snake else 
    #just pop to make the snake going in the current direction)
    if snake_position[0] == x_apple and snake_position[1] == y_apple:
        apple_pickup_sound.play()
        x_apple = random.randint(0, (x_window // 10) - 1) * 10
        y_apple = random.randint(0, (y_window // 10) - 2) * 10
        score += 1
    else:
        snake.pop()

    #If snake go over the limit of the window -> game over
    if snake_position[0] >= x_window or snake_position[1] >= y_window or snake_position[0] < 0 or snake_position[1] < 0:
        game_over(game_window, score, record)
    #If the snake touche himself -> game over
    if snake_position in snake[1:]:
            game_over(game_window, score, record)   


    # Clear the window before drawing
    game_window.fill(black)

    #Drawing the snake
    for cell in snake:
       pygame.draw.rect(game_window, green, pygame.Rect(cell[0], cell[1], 10, 10))

    #Darwing the apple
    pygame.draw.rect(game_window, red, pygame.Rect(x_apple, y_apple, 10, 10))

    #Show the score at each update
    show_score(game_window, score)

    #Update the game window
    pygame.display.update()

    #Set the fps on the game (fps direvtly affect the snake speed)
    fps.tick(snake_speed)
   

