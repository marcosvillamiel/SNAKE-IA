# 🐍 Autonomous Snake Agent — Machine Learning

Machine Learning project focused on developing an **autonomous Snake agent** using data collected from the game environment.

The project explores several stages of an ML pipeline: **data collection, classification, automatic decision-making, and regression-based prediction**. Different machine learning algorithms were evaluated and iteratively refined based on both their predictive performance and their behaviour when integrated into the game.

---

## 📌 Project Overview

The objective was to use information extracted from the Snake game to build models capable of making decisions and predicting future outcomes.

The project was divided into four main phases:

1. **Instance Collection** — collecting and preparing game data.
2. **Classification** — predicting the next movement of the Snake.
3. **Automatic Agent** — integrating trained models into the game to control the Snake automatically.
4. **Prediction** — predicting the score of the next game step using regression models.

The project was developed using **Python, Weka, and the provided Snake simulator**.

---

# 1. Data Collection

The first phase focused on generating a dataset from games played manually using the keyboard.

The resulting dataset contained:

* **2,514 instances**
* **21 attributes**

The collected features described different aspects of the game state, including:

* Snake head position
* Food position
* Distance to food
* Snake length
* Safe directions
* Current and previous movement direction
* Whether the Snake was following a cycle
* Whether its body was between the head and the food
* Current score

Future-state attributes were also calculated, including the predicted next position, next Manhattan distance, and next score.

### Example features

```text
snake_pos_x
snake_pos_y
food_pos_x
food_pos_y
manhattan_distance
large_snake
right_safe
left_safe
up_safe
down_safe
direction
previous_direction
body_indirection
```

The dataset was generated from the interaction between the player and the game environment and was later used for both classification and regression tasks.

---

# 2. Movement Classification

The second phase focused on predicting the **next movement direction of the Snake**.

### Algorithms evaluated

Three classification algorithms were compared:

* **ID3**
* **J48**
* **LMT (Logistic Model Trees)**

The models were evaluated through several iterations involving:

* Feature selection
* Dimensionality reduction
* Different training/test datasets
* Data collected from multiple games
* Removal of attributes that introduced unnecessary complexity or overfitting

### Iteration 1

The first models were trained using the initial set of selected features.

| Model | Training Accuracy | Test Accuracy |
| ----- | ----------------: | ------------: |
| ID3   |            97.71% |    **97.26%** |
| J48   |            95.43% |        95.02% |
| LMT   |            93.04% |        91.79% |

ID3 achieved the highest accuracy in this first iteration.

### Iteration 2

Feature selection was applied to reduce the dimensionality of the dataset.

Several features with lower correlation to the target variable were removed, including:

```text
cycle
manhattan_distance
snake_pos_y
body_indirection
snake_pos_x
large_snake
```

The models were retrained using the reduced feature set.

### Iteration 3

To improve generalisation, data from **five different games** was used for training, while a separate game was used as the test set.

The resulting test accuracies were:

| Model | Test Accuracy |
| ----- | ------------: |
| ID3   |    **96.28%** |
| J48   |        95.98% |
| LMT   |        95.30% |

The results showed that training with data collected from multiple games produced a more robust model.

---

# 3. Building an Autonomous Agent

The classification models were then integrated into the Snake simulator to create an **automatic agent**.

The Weka models were imported into the Snake game, allowing the agent to classify the current state and select the next movement at each game tick.

```text
Game State
     ↓
Feature Extraction
     ↓
ML Model
     ↓
Predicted Direction
     ↓
Snake Movement
     ↓
New Game State
```

### Model limitations

During integration, an important difference became apparent between **offline model accuracy and actual agent performance**.

Although ID3 achieved the best classification accuracy in the previous phase, it could not be directly used with the available Weka integration.

J48 and LMT models were therefore evaluated in the game.

Further experiments showed that models using mainly **categorical variables** produced better behaviour when integrated into the environment.

The final categorical model used:

```text
food_side_x
food_side_y
right_safe
left_safe
up_safe
down_safe
body_indirection
```

The `previous_direction` feature was removed because it was found to negatively affect the agent's decisions.

### Agent behaviour

The resulting LMT-based agent achieved an approximate score of **5,000**.

Rather than always following the shortest path to the food, the agent developed a more conservative strategy:

1. Move towards the borders.
2. Follow the border until aligned with the food.
3. Adjust its movement towards the food.
4. Prioritise avoiding collisions with the walls.

This strategy was not optimal in terms of path length, but it allowed the agent to avoid many premature failures.

### Performance comparison

| Agent           | Approx. Score |
| --------------- | ------------: |
| Move Tutorial   |        ~5,000 |
| Automatic Agent |        ~5,000 |
| Keyboard        |        ~7,000 |

The automatic agent therefore achieved performance comparable to the provided automated baseline, while remaining below manual gameplay performance.

---

# 4. Score Prediction

The final phase treated the problem as a **regression task**.

The objective was to predict:

```text
next_score
```

based on information from the current game state and the next movement.

Nominal attributes were removed because the selected regression algorithms operated on numerical variables.

### Regression models

The following algorithms were evaluated:

* **M5P**
* **Random Forest**
* **Decision Stump**

### Initial results

| Model          | Correlation (r) |        MAE |         MSE |
| -------------- | --------------: | ---------: | ----------: |
| M5P            |          0.9974 |    10.5831 |     35.8491 |
| Random Forest  |      **0.9997** | **7.2121** | **12.3939** |
| Decision Stump |          0.8587 |    216.407 |     255.651 |

Random Forest produced the strongest predictive performance in the initial experiment.

### Feature Selection

A second iteration applied attribute selection to reduce the number of features.

For Random Forest, the selected attributes included:

```text
score
large_snake
food_pos_x
food_pos_y
snake_pos_y
snake_pos_y_next
snake_pos_x_next
snake_pos_x
body_indirection
```

After feature selection:

| Model         | Correlation (r) |       MAE |        MSE |
| ------------- | --------------: | --------: | ---------: |
| M5P           |          0.9957 | **4.747** |    15.6281 |
| Random Forest |      **0.9986** |    6.6641 | **8.8754** |

Random Forest maintained the highest correlation and lowest MSE, while M5P achieved a lower MAE and provided a more interpretable model.

---

# 🧠 Key Lessons

One of the main lessons from the project was that **model accuracy alone does not determine how well an autonomous agent performs**.

A model can achieve high accuracy on a test dataset while behaving differently when integrated into a dynamic environment.

The project also highlighted the importance of:

* Data quality and data collection
* Feature engineering
* Feature selection
* Model comparison
* Generalisation across different games
* Evaluating models inside the actual environment
* Balancing predictive performance with model interpretability

The iterative development of the autonomous agent showed how theoretical ML results can differ from practical system behaviour.

---

# 🛠️ Technologies

* **Python**
* **Weka**
* **Machine Learning**
* **Classification**
* **Regression**
* **Decision Trees**
* **Logistic Model Trees**
* **Random Forest**
* **Feature Selection**
* **Data Preprocessing**


# 👨‍💻 Authors

**Marcos Villamiel**
**Pablo Fernández**

Universidad Carlos III de Madrid

---

## 📄 Academic Context

This project was developed as part of the **Data Science and Engineering** degree at Universidad Carlos III de Madrid.

The work integrates several Machine Learning concepts covered throughout the course, from data collection and preprocessing to classification, regression, model evaluation, and the integration of ML models into an autonomous system.
