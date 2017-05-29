# Assignment 1 - Isolation

## Setup

Clone this repository:
`git clone https://github.gatech.edu/omscs6601/assignment_1.git`

The submission scripts depend on the presence of 3 python packages - `requests`, `future`, and `nelson`. Install them using the command below:

`pip install -r requirements.txt`

Read [setup.md](./setup.md) for more information on how to effectively manage your git repository and troubleshooting information.

## Overview

This assignment will cover some of the concepts discussed in the Adversarial Search lectures. You will be implementing game playing agents for a variant of the game Isolation called Team Isolation.

### The Game

 The rules of Team Isolation are simple. In our version, two players take turn placing their own game pieces on different squares of a 7-by-7 grid. Each player has 2 game pieces which they can move on the board. At the beginning of the game, the players, in turn, place each of their two pieces on any unoccupied square. The players must use their first two turns to place their two pieces. From that point on, the pieces move like a Queen in chess (any number of squares vertically, horizontally, or diagonally but not past an occupied or blocked square). Each time a player moves their piece, there is a twist. There is a chance, based on non-uniform probability that increases with distance moved, the piece will fail to reach the intended square. Essentially, the farther away you move, the greater chance you will land on an adjacent valid square to the intended target. All 1 square moves are certain but all other moves have a fixed maximum chance of failure based on distance. The square that was previously occupying is blocked and cannot be moved for remainder of the game.  The queens can’t move through each other or through the blocked portion of the board. The first player who is unable to move loses.

### The Files

While you'll only have to edit and submit `player_submission.py`, there are a number of notable files:

1. `isolation.py`: Includes the `Board` class and a function for printing out a game as text.
2. `player_submission.py`: Where you'll implement required methods for your agents.
3. `player_submission_tests.py`: Sample tests to validate your agents locally.
3. `test_players.py`: Example agents used to play isolation locally.
4. `submit.py`: A script to submit your work.

### The Assignment

Your task is to create an AI that can play and win a game of Team Isolation. Your AI will be tested against several pre-baked AIs as well as your peers’ AI systems. You will implement your AI in Python 2.7, using our provided code as a starting point.

In this repository, we provide:

- A class for representing the game state
- A function for printing the game board
- A function for generating legal game states
- A class for running unit tests
- A random AI (baseline test)

Your goal is to implement the following parts of the AI in the class CustomPlayer:

1. Evaluation functions (`OpenMoveEvalFn()` and `CustomEvalFn()`)
2. The minimax algorithm (`minimax()`)
3. Alpha-beta pruning (`alphabeta()`)

Your agent will have a limited amount of time to act each turn (5 seconds). We will call these functions directly so **don’t modify** the <u>function names</u> or the <u>parameters</u>.

In addition to checking time each turn, you will be penalized if your agent takes more than a few minutes at construction time. For example, if you attempt to load the entire set of possible board states from memory. In total, your submission will be allowed to run for a maximum of <u>75 minutes</u> before being interrupted.

These are the bare minimum requirements for your AI, and the rest is up to you. You will be scored according to how well your AI performs against some baseline AIs that we provide (see “Grading”). If you want to improve over the base performance, here are a few suggestions:

- Storing the evaluation scores for past moves.
- Modifying your evaluation function to account for “killer moves”.
- Ordering nodes to maximize pruning.

### Grading

The grade you receive for the assignment will be determined as follows:

| Points    | Condition                                |
| --------- | ---------------------------------------- |
| 10 points | You write an evaluation function that scores based on the maximum number of moves that the AI can make minus maximum number of moves opponent can make, and your evaluation function performs correctly on some sample boards we provide. |
| 30 points | Your AI defeats a random player >= 60% of the time. |
| 30 points | Your AI defeats an agent using OpenMoveEvalFn that is depth limited to level 3  >= 60% of the time. Due to the high branching factor of Team Isolation, we reserve the ability to have our test player move randomly in the beginning of the game. |
| 20 points | Your AI defeats an agent using OpenMoveEvalFn that uses iterative deepening and alpha-beta pruning >= 60% of the time. |
| 5 points  | Your AI defeats an agent using expectiminimax >= 60% of the time. |
| 5 points  | Your AI defeats an agent using expectiminimax >= 90% of the time. |

Submission policy: 1 submission per hour and last submission score.

### Botfight! (Extra Credit)

In addition to the basic assignment, you will have the option to compete against your peers for the glory of being the Summer 2017 AI-Game-Playing champ. We’ll set up a system to pit your AI against others, and we’ll be giving out prizes for the top players. May the odds be ever in your favor.

If you wish to compete in the tournament, simply include a plaintext file with a description of your agent, titled ‘AI.txt’, and your CustomPlayer instance will be enlisted.

If you compete in the AI tournament and your agent finishes in the top 10%, you will receive a bonus:

- Best Overall:  5 bonus points.
- Top 5%: 2 bonus points.
- Top 10%: 1 bonus point.

## How to Submit Your Code

A friendly reminder: please ensure that your submission is in `player_submission.py`. The script described in the following section automatically sends that file to the servers for processing.

To submit your code and have it evaluated for a grade, use `python submit.py`. We are going to limit you to 1 submissions in one hour (Subject to change depending on load on servers) and the last submission before the deadline will be used to determine your grade.

To enter yourself into the playoffs against your classmates, run `python submit.py --enable-face-off`. Ensure that you have created the required AI.txt to enter the tournament.

## Your Classes (`player_submission.py`)

As discussed above, the follow classes must be populated in `player_submission.py`:

1. `OpenMoveEvalFn`
2. `CustomEvalFn`
3. `CustomPlayer`

Aside from those 3 classes, any added code (such as additional tests) **MUST** be included in **`player_submissions_tests.py`** or another separate file. We need to be certain that code outside of these classes does not get accidentally executed.

### Evaluation Functions

These functions will inform the value judgements your AI will make when choosing moves. There are 2 classes:

- `OpenMoveEvalFn` - Scores the maximum number of available moves open for computer player minus the maximum number of moves open for opponent player. All baseline tests will use this function. **This is mandatory**
- `CustomEvalFn` - You are encouraged to create your own evaluation function here.

**DO** submit the code within this class (and only the code within this class).

#### Tips

1. You may write additional code within each class. However, we will only be invoking the `score()` function. You may not change the signature of this function.
2. When writing additional code to test, try to do so in separate cells. It allows for independent test execution and you can be sure that *all* the code within the EvalFn cells belong only to the EvalFn classes

```python
class OpenMoveEvalFn():
    """Evaluation function that outputs a
    score equal to how many moves are open
    for AI player on the board
    minus the moves open for opponent player."""
    def score(self, game, maximizing_player_turn=True):
        # TODO: finish this function!
        return eval_func

class CustomEvalFn():
    """Custom evaluation function that acts
    however you think it should. This is not
    required but highly encouraged if you
    want to build the best AI possible."""
    def score(self, game, maximizing_player_turn=True):
        # TODO: finish this function!
        return eval_func
```

### `CustomPlayer`

This is the meat of the assignment. A few notes about the class:

- You are not permitted to change the function signatures of any of the provided methods.
- You are permitted to change the default values within the function signatures provided. In fact, when you have your custom evaluation function, you are encouraged to change the default values for `__init__` to use the new eval function.
- You are free change the contents of each of the provided methods. When you are ready with `alphabeta()`, for example, you are encouraged to update `move()` to use that function instead.
- You are free to add more methods to the class.
- You may not create additional external functions and classes that are referenced from within this class.

**DO** submit the code within this class (and only the code within this class).

```python
class CustomPlayer():
    # TODO: finish this class!
    """Player that chooses a move using
    your evaluation function and
    a depth-limited minimax algorithm
    with alpha-beta pruning.
    You must finish and test this player
    to make sure it properly uses minimax
    and alpha-beta to return a good move
    in less than 5 seconds."""
    def __init__(self,  search_depth=3, eval_fn=OpenMoveEvalFn()):
        # if you find yourself with a superior eval function, update the
        # default value of `eval_fn` to `CustomEvalFn()`
        self.eval_fn = eval_fn
        self.search_depth = search_depth


    def move(self, game, legal_moves, time_left):
        best_move,best_queen, utility = self.minimax(game,time_left, depth=self.search_depth)
        #change minimax to alphabeta after completing alphabeta part of assignment
        return best_move, best_queen


    def utility(self, game):
        """TODO: Update this function to calculate the utility of a game state"""
        return self.eval_fn.score(game)


    def minimax(self, game, time_left, depth=float("inf"), maximizing_player=True):
        # TODO: finish this function!
        return best_move,best_queen, best_val

    def alphabeta(self, game, time_left, depth=float("inf"), alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        # TODO: finish this function!
        return best_move, best_queen, val
```

### Built-in Tests

In `player_submission_tests.py` several built-in tests can be found in the **`main()`** function. We've included these to help you test your player and evaluation function as well as to give you an idea of how the classes are used. Feel free to play around with the code and add more tests.

## Helper Player classes (`test_players.py`)

We include 2 player types for you to test against locally:

- `RandomPlayer` - chooses a legal move randomly from among the available legal moves
- `HumanPlayer` - allows *YOU* to play against the AI

**DO NOT** submit. You are however free to change these classes as you see fit. Know that any changes you make will be solely for the benefit of your own tests.

