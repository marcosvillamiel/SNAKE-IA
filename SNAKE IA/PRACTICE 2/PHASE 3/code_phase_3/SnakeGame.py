"""
Snake Eater Game
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""
from snake_env import SnakeGameEnv
from q_learning import QLearning
import pygame
import sys


def state_to_index(state):
    """
    Convert the state tuple to a unique index for Q-table lookup.
    The state consists of 12 boolean values, which we'll convert to a unique integer.
    """
    index = 0
    for i, val in enumerate(state):
        if val:
            index += 1 << i
    return index


def main():
    # Window size
    FRAME_SIZE_X = 300
    FRAME_SIZE_Y = 300

    # Colors (R, G, B)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)

    difficulty = 100  # Adjust as needed
    render_game = True  # Show the game or not
    growing_body = True  # Makes the body of the snake grow
    training = True  # Defines if it should train or not

    # Initialize the game window, environment and q_learning algorithm
    pygame.init()
    env = SnakeGameEnv(FRAME_SIZE_X, FRAME_SIZE_Y, growing_body)

    # Number of possible states is 2^12 (since we have 12 binary features in state)
    number_states = 2 ** 12
    ql = QLearning(n_states=number_states, n_actions=4, alpha=0.1, gamma=0.9, epsilon=0.1)

    num_episodes = 100

    if render_game:
        game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))
        fps_controller = pygame.time.Clock()

    for episode in range(num_episodes):
        state = env.reset()
        state_idx = state_to_index(state)
        total_reward = 0
        game_over = False

        while not game_over:
            # Choose action using epsilon-greedy policy
            action = ql.choose_action(state_idx, [0, 1, 2, 3])

            # Execute action and get next state and reward
            next_state, reward, game_over = env.step(action)
            next_state_idx = state_to_index(next_state)
            total_reward += reward

            if training:
                # Update Q-table
                ql.update_q_table(state_idx, action, reward, next_state_idx, game_over)

            # Update current state
            state_idx = next_state_idx

            # Render
            if render_game:
                game_window.fill(BLACK)
                snake_body = env.get_body()
                food_pos = env.get_food()

                for pos in snake_body:
                    pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

                pygame.draw.rect(game_window, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()
                fps_controller.tick(difficulty)

        # Save Q-table periodically
        if episode % 100 == 0:
            ql.save_q_table()

        print(f"Episode {episode + 1}, Total reward: {total_reward}")

    ql.save_q_table()
    pygame.quit()


if __name__ == "__main__":
    main()