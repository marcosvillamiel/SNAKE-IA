"""
Snake Eater Environment
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""
import numpy as np
import random

class SnakeGameEnv:
    def __init__(self, frame_size_x=150, frame_size_y=150, growing_body=True):
        # Initializes the environment with default values
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.growing_body = growing_body
        self.reset()

    def reset(self):
        # Resets the environment with default values
        self.snake_pos = [50, 50]
        self.snake_body = [[50, 50], [60, 50], [70, 50]]
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10, random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.score = 0
        self.game_over = False
        return self.get_state()

    def step(self, action):
        # Implements the logic to change the snake's direction based on action
        # Update the snake's head position based on the direction
        # Check for collision with food, walls, or self
        # Update the score and reset food as necessary
        # Determine if the game is over
        self.update_snake_position(action)
        reward = self.calculate_reward()
        self.update_food_position()
        state = self.get_state()
        self.game_over = self.check_game_over()
        return state, reward, self.game_over

    def get_state(self):
        head_x, head_y = self.snake_pos
        food_x, food_y = self.food_pos

        food_left = food_x < head_x
        food_right = food_x > head_x
        food_up = food_y < head_y
        food_down = food_y > head_y

        danger_left = (head_x - 10 < 0) or ([head_x - 10, head_y] in self.snake_body[1:])
        danger_right = (head_x + 10 >= self.frame_size_x) or ([head_x + 10, head_y] in self.snake_body[1:])
        danger_up = (head_y - 10 < 0) or ([head_x, head_y - 10] in self.snake_body[1:])
        danger_down = (head_y + 10 >= self.frame_size_y) or ([head_x, head_y + 10] in self.snake_body[1:])

        dir_left = self.direction == 'LEFT'
        dir_right = self.direction == 'RIGHT'
        dir_up = self.direction == 'UP'
        dir_down = self.direction == 'DOWN'

        state = (
            food_left, food_right, food_up, food_down,
            danger_left, danger_right, danger_up, danger_down,
            dir_left, dir_right, dir_up, dir_down
        )
        return state

    def get_body(self):
    	return self.snake_body

    def get_food(self):
    	return self.food_pos

    def calculate_reward(self):
        # Calculate and return the reward. Remember that you can provide positive or negative reward.
        if self.check_game_over():
            return -100  # Big penalty for dying

        head_x, head_y = self.snake_pos
        food_x, food_y = self.food_pos

        if head_x == food_x and head_y == food_y:
            return 10  # Reward for eating food

        # Calculate Manhattan distance to food
        prev_distance = abs(self.snake_body[1][0] - food_x) + abs(self.snake_body[1][1] - food_y)
        current_distance = abs(head_x - food_x) + abs(head_y - food_y)

        if current_distance < prev_distance:
            return 1  # Reward for moving closer to food
        elif current_distance > prev_distance:
            return -1  # Penalty for moving away from food

        return -0.1  # Small penalty for no progress
        
    def check_game_over(self):
        # Return True if the game is over, else False
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            return True
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True
                
        return False

    def update_snake_position(self, action):
        # Updates the snake's position based on the action
        # Map action to direction
        change_to = ''
        direction = self.direction
        if action == 0:
            change_to = 'UP'
        elif action == 1:
            change_to = 'DOWN'
        elif action == 2:
            change_to = 'LEFT'
        elif action == 3:
            change_to = 'RIGHT'
    
        # Move the snake
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
    
        if direction == 'UP':
            self.snake_pos[1] -= 10
        elif direction == 'DOWN':
            self.snake_pos[1] += 10
        elif direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif direction == 'RIGHT':
            self.snake_pos[0] += 10
            
        self.direction = direction
        
        
        self.snake_body.insert(0, list(self.snake_pos))
        
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 10
            self.food_spawn = False
            # If the snake is not growing
            if not self.growing_body:
                self.snake_body.pop()
        else:
            self.snake_body.pop()
    
    def update_food_position(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_x//10)) * 10]
        self.food_spawn = True
        
        

