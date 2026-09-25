# 🐍 Snake AI — Machine Learning & Reinforcement Learning

A series of Machine Learning and Reinforcement Learning experiments developed around the **Snake game environment** as part of the Data Science and Engineering degree at Universidad Carlos III de Madrid.

The project explores how an autonomous agent can learn to make decisions using different approaches, progressing from **supervised Machine Learning and data-driven decision making to Reinforcement Learning**.

---

## 🎯 Project Overview

The project is divided into two practices, each approaching the Snake problem from a different perspective.

### Practice I — Machine Learning & Autonomous Agent

The first practice focuses on building an autonomous Snake agent using data collected from gameplay.

The workflow includes:

```text
Data Collection
      ↓
Feature Engineering
      ↓
Classification
      ↓
Model Evaluation
      ↓
Autonomous Agent
      ↓
Regression & Score Prediction
```

Several Machine Learning models were evaluated, including:

* ID3
* J48
* Logistic Model Trees (LMT)
* M5P
* Random Forest
* Decision Stump

The classification models were used to predict the Snake's next movement, while regression models were used to predict the next score.

A key part of the practice was integrating the trained models into the game environment and evaluating their behaviour as an autonomous agent.

---

### Practice II — Reinforcement Learning

The second practice approaches the same problem using **Reinforcement Learning**.

A Q-Learning agent was developed to learn how to play Snake through repeated interaction with the environment.

The agent follows the classical Reinforcement Learning loop:

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

The agent gradually improves its behaviour by updating a Q-table based on the rewards obtained during gameplay.

The state representation uses **12 binary features** describing:

* Relative food position
* Immediate collision risks
* Current movement direction

This results in a theoretical state space of:

$$
2^{12} = 4096
$$

possible states.

The project uses an **ε-greedy policy** to balance exploration and exploitation.

---

# 🧠 Approaches

The two practices provide complementary approaches to autonomous decision-making.

|                         | Practice I                 | Practice II                       |
| ----------------------- | -------------------------- | --------------------------------- |
| Approach                | Supervised ML              | Reinforcement Learning            |
| Main task               | Predict next movement      | Learn actions through interaction |
| Learning signal         | Labelled gameplay data     | Rewards                           |
| Main technique          | Classification             | Q-Learning                        |
| Decision mechanism      | Trained ML model           | Q-table                           |
| Exploration             | Not explicitly modelled    | ε-greedy                          |
| Environment interaction | Model integrated into game | Agent learns through gameplay     |

This progression provides a practical comparison between **learning from previously collected data** and **learning directly through interaction with an environment**.

---

# 📊 Practice I — Machine Learning

The first practice started by collecting gameplay data.

The resulting dataset contained:

* **2,514 instances**
* **21 attributes**

The collected information described different aspects of the Snake's state, including its position, food position, distances, movement direction, safe directions, body position and score.

### Classification

The objective was to predict the Snake's next movement.

Three algorithms were evaluated:

* ID3
* J48
* LMT

Feature selection and different training datasets were used to improve generalisation.

Data from multiple games was eventually used to train the models, with separate gameplay data used for evaluation.

### Autonomous Agent

The trained models were integrated into the Snake environment so that the model could automatically select the next movement.

An important observation from this stage was that **offline classification accuracy did not necessarily translate directly into better behaviour inside the game**.

The autonomous agent therefore had to be evaluated not only through model metrics but also through its behaviour in the environment.

### Regression

The practice also explored predicting the next game score.

The regression models evaluated were:

* M5P
* Random Forest
* Decision Stump

Feature selection was also applied to investigate how the input variables affected prediction performance.

---

# 🤖 Practice II — Q-Learning

The second practice implemented a tabular Reinforcement Learning approach.

## State Representation

The agent represents the environment using 12 binary features:

```text
food_left
food_right
food_up
food_down

danger_left
danger_right
danger_up
danger_down

dir_left
dir_right
dir_up
dir_down
```

The representation captures the relevant local information needed by the agent while keeping the state space manageable.

The Snake's complete body is not explicitly encoded. Instead, collision risks are represented through the directional `danger_*` variables.

## Q-Table

The Q-table stores a value for each:

```text
(state, action)
```

combination.

The Q-values are updated after each interaction with the environment using:

$$
Q(s,a) \leftarrow (1-\alpha)Q(s,a)
+\alpha[r+\gamma\max_{a'}Q(s',a')]
$$

The main training parameters were:

```text
α = 0.1
γ = 0.9
ε = 0.7
ε decay = 0.995
```

## Reward Function

The reward function encourages the agent to reach the food while avoiding collisions.

| Situation             | Reward |
| --------------------- | -----: |
| Food eaten            |    +10 |
| Moves closer to food  |     +1 |
| Moves away from food  |     -1 |
| No progress           |   -0.1 |
| Collision / game over |   -100 |

The distance to the food is evaluated using Manhattan distance.

---

# 🔬 Key Learning Outcomes

Across both practices, the project provided practical experience with:

* Data collection and preprocessing
* Feature engineering
* Feature selection
* Classification
* Regression
* Model evaluation
* Autonomous decision-making
* Reinforcement Learning
* Q-Learning
* Q-table implementation
* Exploration vs. exploitation
* Reward design
* Hyperparameter tuning
* Integrating ML models into an interactive environment

One of the main observations across the project was the difference between **predictive performance and behaviour in a dynamic environment**.

The first practice learns from previously collected examples, while the second allows the agent to improve its policy through direct interaction and rewards.

---

# 🛠️ Technologies

* **Python**
* **NumPy**
* **Weka**
* **Machine Learning**
* **Reinforcement Learning**
* **Q-Learning**
* **Decision Trees**
* **Logistic Model Trees**
* **Random Forest**
* **Regression**
* **Feature Selection**


```

Each practice contains its own implementation, results and detailed documentation, while this README provides an overview of the complete project.

---

# 🎓 Academic Context

Developed as part of the **Data Science and Engineering** degree at **Universidad Carlos III de Madrid (UC3M)**.

The project explores different Machine Learning approaches to autonomous decision-making using the Snake game as a controlled environment.
