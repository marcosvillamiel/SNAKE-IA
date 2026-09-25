# Snake AI — Q-Learning

A Reinforcement Learning project in which a **Q-Learning agent learns to play the Snake game through trial and error**.

The project focuses on implementing a tabular Q-Learning approach, designing a compact state representation, defining a reward function, balancing exploration and exploitation, and evaluating the agent across different board configurations.

## Overview

The agent interacts with the Snake environment repeatedly:

```text
State
  ↓
Action
  ↓
Environment
  ↓
Reward + Next State
  ↓
Q-Table Update
  ↓
New State
```

Through repeated episodes, the agent gradually updates its Q-table and learns which actions are more valuable in different game situations.

## State Representation

The game state is represented using **12 binary features** describing the snake's current situation:

* `food_left`
* `food_right`
* `food_up`
* `food_down`
* `danger_left`
* `danger_right`
* `danger_up`
* `danger_down`
* `dir_left`
* `dir_right`
* `dir_up`
* `dir_down`

The state representation was designed to use a small number of discrete features and remain independent of the board size.

Since each feature is binary, the theoretical state space contains:

$$
2^{12} = 4096
$$

possible states.

The snake's entire body is not explicitly represented. Instead, the `danger_*` features capture whether moving in a given direction would result in a collision with a wall or the snake's own body.

## Q-Table

The agent uses a **Q-table** to store the expected value of each possible action for every state.

Conceptually:

```text
Q(state, action)
```

The Q-value represents the expected long-term return of taking a particular action from a given state.

After each interaction with the environment, the corresponding Q-value is updated using the Q-Learning update rule:

$$
Q(s,a) \leftarrow (1-\alpha)Q(s,a)
+\alpha\left[r+\gamma\max_{a'}Q(s',a')\right]
$$

Where:

* **α** — learning rate
* **γ** — discount factor
* **r** — reward received after taking the action
* **s'** — next state
* **max Q(s', a')** — highest estimated value among the possible actions in the next state

For terminal states, the update uses the immediate reward without considering future rewards.

## Reward Function

The reward function was designed to encourage the agent to reach the food while avoiding collisions.

| Situation             | Reward |
| --------------------- | -----: |
| Food eaten            |  `+10` |
| Moves closer to food  |   `+1` |
| Moves away from food  |   `-1` |
| No progress           | `-0.1` |
| Game over / collision | `-100` |

The distance between the snake and the food is evaluated using **Manhattan distance** to determine whether the snake has moved closer to or further from the target.

## Exploration vs. Exploitation

The agent uses an **ε-greedy policy** to balance exploration and exploitation.

With probability `ε`, the agent explores by selecting an action randomly. Otherwise, it chooses the action with the highest Q-value for the current state.

The training starts with a relatively high exploration rate and progressively reduces it using an epsilon decay strategy:

```text
ε_initial = 0.7
ε_decay   = 0.995
```

This allows the agent to explore different behaviours during early training and increasingly rely on its learned Q-values as training progresses.

## Training

The Q-table is maintained across episodes, allowing the agent to retain previously learned information and progressively improve its behaviour.

The training process includes:

1. Obtaining the current state.
2. Selecting an action using the ε-greedy policy.
3. Executing the action in the Snake environment.
4. Calculating the resulting reward.
5. Obtaining the next state.
6. Updating the Q-table.
7. Repeating the process over multiple episodes.

The main Q-Learning parameters used in the project were:

```text
Learning rate (α) = 0.1
Discount factor (γ) = 0.9
Initial epsilon (ε) = 0.7
Epsilon decay = 0.995
```

## Evaluation

The trained agent was evaluated using different board configurations to analyse how the learned policy performed under different environments.

The project considered boards with different dimensions, including:

* `150 × 300`
* `200 × 200`
* `300 × 300`

The Q-table was kept across episodes so that learning could continue throughout training rather than restarting from an empty table for every game.

## Technologies

* **Python**
* **NumPy**
* **Reinforcement Learning**
* **Q-Learning**
* **Tabular Reinforcement Learning**



## Key Takeaways

This project provided practical experience with:

* Designing a compact state representation for a Reinforcement Learning problem.
* Implementing a **Q-table and Q-Learning algorithm**.
* Designing a reward function to guide agent behaviour.
* Balancing **exploration and exploitation** using an ε-greedy strategy.
* Selecting and tuning Reinforcement Learning hyperparameters.
* Evaluating an agent across different environment configurations.
* Understanding how state representation affects the size and feasibility of a tabular RL solution.
