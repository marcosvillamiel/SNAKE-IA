"""
Snake Eater
Made with PyGame
Last modification in January 2024 by José Carlos Pulido
Machine Learning Classes - University Carlos III of Madrid
"""

import pygame, sys, time, random, os.path
pygame.mixer.quit()

from wekaH import Weka

# DIFFICULTY settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTY = 120
# Window size
FRAME_SIZE_X = 480
FRAME_SIZE_Y = 480

# Colors (R, G, B)
BLACK = pygame.Color(51, 51, 51)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(204, 51, 0)
GREEN = pygame.Color(204, 255, 153)
BLUE = pygame.Color(0, 51, 102)

# GAME STATE CLASS
class GameState:
    def __init__(self, FRAME_SIZE):
        self.snake_pos = [100, 50]
        self.snake_pos_next = [100, 50]


        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = [random.randrange(1, (FRAME_SIZE[0]//10)) * 10, random.randrange(1, (FRAME_SIZE[1]//10)) * 10]
        self.food_spawn = True
        self.direction = 'DOWN'
        self.previous_direction = None
        self.change_to = self.direction
        self.food_side_y = None
        self.food_side_x = None
        self.right_safe = True
        self.left_safe = False
        self.up_safe = True
        self.down_safe = True
        self.score = 0
        self.next_score = 0
        self.move_history = []

# Game Over
def game_over(game):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, WHITE)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/4)
    game_window.fill(BLUE)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(game, 0, WHITE, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Score
def show_score(game, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(game.score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (FRAME_SIZE_X/8, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

# Move the snake
def move_keyboard(game, event):
    change_to = game.direction
    if event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_UP or event.key == ord('w')) and game.direction != 'DOWN':
            change_to = 'UP'
        if (event.key == pygame.K_DOWN or event.key == ord('s')) and game.direction != 'UP':
            change_to = 'DOWN'
        if (event.key == pygame.K_LEFT or event.key == ord('a')) and game.direction != 'RIGHT':
            change_to = 'LEFT'
        if (event.key == pygame.K_RIGHT or event.key == ord('d')) and game.direction != 'LEFT':
            change_to = 'RIGHT'
    return change_to


# TODO: IMPLEMENT HERE THE NEW INTELLIGENT METHOD


# Check if the position is safe

def is_safe(pos):
    x, y = 0, 1
    return (pos not in game.snake_body and
            0 <= pos[x] < FRAME_SIZE_X and
            0 <= pos[y] < FRAME_SIZE_Y)


def possible_moves():
    moves = {
        'LEFT': (-10, 0),
        'RIGHT': (10, 0),
        'UP': (0, -10),
        'DOWN': (0, 10)
    }

    # Calculate the new position for each possible move
    possible_moves = []
    for direction, (dx, dy) in moves.items():
        dir = direction
        new_pos = [game.snake_pos[x] + dx, game.snake_pos[y] + dy]
        # If the new position is safe, add it to the possible_moves dictionary.
        if is_safe(new_pos):
            possible_moves.append(dir)
    return possible_moves


# Calculate distance between two positions
def manhattan_distance(pos1, pos2):
    x, y = 0, 1
    return abs(pos1[x] - pos2[x]) + abs(pos1[y] - pos2[y])

def body_indirection(pos,body, direction):
    if direction == 'RIGHT':
        for i in body:
            if i[1] == pos[1] and pos[0] < i[0]:
                    return 'True'
    elif direction == 'LEFT':
        for i in body:
            if i[1] == pos[1] and pos[0] > i[0]:
                    return 'True'
    elif direction == 'UP':
        for i in body:
            if i[0] == pos[0] and pos[1] > i[1]:
                    return 'True'
    elif direction == 'DOWN':
        for i in body:
            if i[0] == pos[0] and pos[1] < i[1]:
                return 'True'
    return 'False'

def is_unique(lista):
    if len(lista) == 4:
        if len(lista) == len(set(lista)):
            return 'True'
        else:
            return 'False'
    else:
        return 'False'


def move_tutorial_1(game):
    x, y = 0, 1
    change_to = game.direction

    # Possible moves
    moves = {
        'LEFT': (-10, 0),
        'RIGHT': (10, 0),
        'UP': (0, -10),
        'DOWN': (0, 10)
    }

    # Calculate the new position for each possible move
    possible_moves = {}
    for direction, (dx, dy) in moves.items():
        new_pos = [game.snake_pos[x] + dx, game.snake_pos[y] + dy]
        # If the new position is safe, add it to the possible_moves dictionary.
        if is_safe(new_pos):
            possible_moves[direction] = new_pos

    # If there are no safe moves, choose a move that avoids the crash
    if not possible_moves:
        for direction, (dx, dy) in moves.items():
            new_pos = [game.snake_pos[x] + dx, game.snake_pos[y] + dy]
            if 0 <= new_pos[x] < FRAME_SIZE_X and 0 <= new_pos[y] < FRAME_SIZE_Y:
                change_to = direction
                break
        return change_to

    # Choose the move that minimizes the distance to the food
    best_direction = None
    min_distance = float('inf')
    for direction, pos in possible_moves.items():
        distance = manhattan_distance(pos, game.food_pos)
        if distance < min_distance:
            min_distance = distance
            best_direction = direction

    if len(game.move_history) == 0:
        game.move_history.append(best_direction)

    if best_direction != game.move_history[-1]:
        game.move_history.append(best_direction)

    if len(game.move_history) > 4:
        game.move_history.pop(0)

    # If there is not a move that gets closer to the food, choose a safe move
    if best_direction is None:
        best_direction = list(possible_moves.keys())[0]

    return best_direction


def print_state(game):
    print("--------GAME STATE--------")
    print("FrameSize:", FRAME_SIZE_X, FRAME_SIZE_Y)
    print("Direction:", game.direction)
    print("PreDirection:", game.previous_direction)
    print("Snake X:", game.snake_pos[0], ", Snake Y:", game.snake_pos[1])
    print("Snake Body:", game.snake_body)
    print("Food X:", game.food_pos[0], ", Food Y:", game.food_pos[1])
    print("Score:", game.score)
    print("Move History", game.move_history)



# TODO: IMPLEMENT HERE THE NEW INTELLIGENT METHOD
def init_arff(arff_filename):
    ''' Initialize the arff file with the header '''
    if os.path.exists(arff_filename):
        with open(arff_filename, "w") as file:
            file.write("@relation snake_game\n\n")
            file.write("@attribute snake_pos_x NUMERIC\n")
            file.write("@attribute snake_pos_y NUMERIC\n")
            file.write("@attribute snake_pos_x_next NUMERIC\n")
            file.write("@attribute snake_pos_y_next NUMERIC\n")
            file.write("@attribute food_pos_x NUMERIC\n")
            file.write("@attribute food_pos_y NUMERIC\n")
            file.write("@attribute food_side_y {UP, DOWN, EQUAL}\n")
            file.write("@attribute food_side_x {RIGHT, LEFT, EQUAL}\n")
            file.write("@attribute manhattan_distance NUMERIC\n")
            file.write("@attribute next_manhattan_distance NUMERIC\n")
            file.write("@attribute large_snake NUMERIC\n")
            file.write("@attribute right_safe {True, False}\n")
            file.write("@attribute left_safe {True, False}\n")
            file.write("@attribute up_safe {True, False}\n")
            file.write("@attribute down_safe {True, False}\n")
            file.write("@attribute score NUMERIC\n")
            file.write("@attribute next_score NUMERIC\n")
            file.write("@attribute cycle {True, False}\n")
            file.write("@attribute body_indirection {True, False}\n")
            file.write("@attribute previous_direction {UP, DOWN, LEFT, "
                       "RIGHT}\n")
            file.write("@attribute direction {UP, DOWN, LEFT, RIGHT}\n\n")
            file.write("@data\n")


def print_line_data(arff_filename):
    x, y = 0, 1
    with open(arff_filename, "a") as file:
        file.write(str(game.snake_pos[x])+","
                   + str(game.snake_pos[y])+","
                   + str(game.snake_pos_next[x]) + ","
                   + str(game.snake_pos_next[y]) + ","
                   + str(game.food_pos[x])+","
                   + str(game.food_pos[y])+","
                   + str(game.food_side_y)+","
                   + str(game.food_side_x)+","
                   + str(manhattan_distance(game.snake_pos, game.food_pos))+","
                   + str(manhattan_distance(game.snake_pos_next, game.food_pos))
                   + ","
                   + str(len(game.snake_body)) + ","
                   + str(game.right_safe)+","
                   + str(game.left_safe)+","
                   + str(game.up_safe) + ","
                   + str(game.down_safe) + ","
                   + str(game.score)+","
                   + str(game.next_score) + ","
                   + is_unique(game.move_history) + ","
                   + body_indirection(game.snake_pos,game.snake_body,
                                      game.direction) + ","
                   + str(game.previous_direction) + ','
                   + str(game.direction)+"\n")

# Checks for errors encounteRED
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater - Machine Learning (UC3M)')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Main logic
game = GameState((FRAME_SIZE_X,FRAME_SIZE_Y))
game.file = "all_data_snake_Practice1.arff"
init_arff(game.file)
x, y = 0, 1

weka = Weka()
weka.start_jvm()

while True:

    game.previous_direction = game.direction
    # UNCOMMENT WHEN METHOD IS IMPLEMENTED
    # game.direction = move_tutorial_1(game)








    #print_line_data(game.file)

    # Moving the snake
    if game.direction == 'UP':
        game.snake_pos[1] -= 10
    if game.direction == 'DOWN':
        game.snake_pos[1] += 10
    if game.direction == 'LEFT':
        game.snake_pos[0] -= 10
    if game.direction == 'RIGHT':
        game.snake_pos[0] += 10

    if 'LEFT' in possible_moves():
        game.left_safe = True
    else:
        game.left_safe = False
    if 'RIGHT' in possible_moves():
        game.right_safe = True
    else:
        game.right_safe = False
    if 'UP' in possible_moves():
        game.up_safe = True
    else:
        game.up_safe = False
    if 'DOWN' in possible_moves():
        game.down_safe = True
    else:
        game.down_safe = False

    if game.snake_pos[y] > game.food_pos[y]:
        game.food_side_y = "UP"
    elif game.snake_pos[y] < game.food_pos[y]:
        game.food_side_y = "DOWN"
    else:
        game.food_side_y = "EQUAL"

    if game.snake_pos[x] < game.food_pos[x]:
        game.food_side_x = "RIGHT"
    elif game.snake_pos[x] > game.food_pos[x]:
        game.food_side_x = "LEFT"
    else:
        game.food_side_x = "EQUAL"


    # Snake body growing mechanism
    game.snake_body.insert(0, list(game.snake_pos))
    if game.snake_pos[0] == game.food_pos[0] and game.snake_pos[1] == game.food_pos[1]:
        game.score += 100
        game.food_spawn = False
    else:
        game.snake_body.pop()
        game.score -= 1

    # Spawning food on the screen
    if not game.food_spawn:
        game.food_pos = [random.randrange(1, (FRAME_SIZE_X//10)) * 10, random.randrange(1, (FRAME_SIZE_Y//10)) * 10]
    game.food_spawn = True


    # GFX
    game_window.fill(BLUE)
    for pos in game.snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, RED, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if game.snake_pos[0] < 0 or game.snake_pos[0] > FRAME_SIZE_X-10:
        game_over(game)
    if game.snake_pos[1] < 0 or game.snake_pos[1] > FRAME_SIZE_Y-10:
        game_over(game)
    # Touching the snake body
    for block in game.snake_body[1:]:
        if game.snake_pos[0] == block[0] and game.snake_pos[1] == block[1]:
            game_over(game)

    show_score(game, 1, WHITE, 'consolas', 15)
    # Refresh game screen

    aux = [
        game.food_side_y,  # Posición X de la comida
        game.food_side_x,  # Posición Y de la comida
        str(game.right_safe),  # Seguridad hacia la derecha (True/False)
        str(game.left_safe),  # Seguridad hacia la izquierda (True/False)
        str(game.up_safe),  # Seguridad hacia arriba (True/False)
        str(game.down_safe),  # Seguridad hacia abajo (True/False)
        str(body_indirection(game.snake_pos,game.snake_body,
                                      game.direction)),
    ]

    print("[DEBUG] Features para el modelo:", aux)

    game.direction = str(weka.predict("./modelocatLTM.model", aux,
                                  "./training_keyboard_1_cat.arff"))

    print("[DEBUG] Predicted direction:", game.direction)



#    for event in pygame.event.get():
 #       if event.type == pygame.QUIT:
  #          pygame.quit()
   #         sys.exit()
   #     if event.type == pygame.KEYDOWN:
    #        # Esc -> Create event to quit the game
     #       if event.key == pygame.K_ESCAPE:
      #          pygame.event.post(pygame.event.Event(pygame.QUIT))
        # CALLING MOVE METHOD
       # game.direction = move_keyboard(game, event)

    if game.direction == 'UP':
        game.snake_pos_next[1] = game.snake_pos[1]-10
    if game.direction == 'DOWN':
        game.snake_pos_next[1] = game.snake_pos[1]+10
    if game.direction == 'LEFT':
        game.snake_pos_next[0] = game.snake_pos[0]-10
    if game.direction == 'RIGHT':
        game.snake_pos_next[0] = game.snake_pos[0]+10


    if (game.snake_pos_next[0] == game.food_pos[0] and game.snake_pos_next[1]
            ==game.food_pos[1]):
        game.next_score = game.score + 100
    else:
        game.next_score = game.score - 1

    if (game.snake_pos_next[0] <= 0 or game.snake_pos_next[0] >=
            FRAME_SIZE_X-10):
        game.next_score = 0
    if game.snake_pos[1] <= 0 or game.snake_pos[1] >= FRAME_SIZE_Y-10:
        game.next_score = 0

    for block in game.snake_body[1:]:
        if (game.snake_pos_next[0] == block[0] and game.snake_pos_next[1] ==
                block[1]):
            game.next_score = 0


    pygame.display.update()
    # Refresh rate
    fps_controller.tick(DIFFICULTY)
    # PRINTING STATE
    print_state(game)
    print_line_data(game.file)
