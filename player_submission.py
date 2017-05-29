#!/usr/bin/env python
from isolation import Board, game_as_text


# This file is your main submission that will be graded against. Do not
# add any classes or functions to this file that are not part of the classes
# that we want.

# Submission Class 1
class OpenMoveEvalFn:

    def score(self, game, maximizing_player_turn=True):
        """Score the current game state
        
        Evaluation function that outputs a score equal to how many 
        moves are open for AI player on the board minus the moves open 
        for opponent player.
            
        Args
            param1 (Board): The board and game state.
            param2 (bool): True if maximizing player is active.

        Returns:
            float: The current state's score. Your agent's moves minus the opponent's moves.
            
        """

        aq1 = game.get_active_players_queen()[0]
        aq2 = game.get_active_players_queen()[1]
        iq1 = game.get_inactive_players_queen()[0]
        iq2 = game.get_inactive_players_queen()[1]
        ap = game.get_legal_moves()
        ip = game.get_opponent_moves()
        aq1Moves = list(ap[aq1])
        aq2Moves = list(ap[aq2])
        iq1Moves = list(ip[iq1])
        iq2Moves = list(ip[iq2])

        aqMoves = set(aq1Moves + aq2Moves)
        iqMoves = set(iq1Moves + iq2Moves)

        if(maximizing_player_turn):
            return len(aqMoves) - len(iqMoves)
        else:
            return len(iqMoves) - len(aqMoves)

# Submission Class 2
class CustomEvalFn:

    def __init__(self):
        pass

    def score(self, game, maximizing_player_turn=True):
        """Score the current game state
        
        Custom evaluation function that acts however you think it should. This 
        is not required but highly encouraged if you want to build the best 
        AI possible.
        
        Args
            game (Board): The board and game state.
            maximizing_player_turn (bool): True if maximizing player is active.

        Returns:
            float: The current state's score, based on your own heuristic.
            
        """
        # TODO: finish this function!
        raise NotImplementedError


class CustomPlayer:
    # TODO: finish this class!
    """Player that chooses a move using 
    your evaluation function and 
    a depth-limited minimax algorithm 
    with alpha-beta pruning.
    You must finish and test this player
    to make sure it properly uses minimax
    and alpha-beta to return a good move
    in less than 5 seconds."""

    def __init__(self, search_depth=3, eval_fn=OpenMoveEvalFn()):
        """Initializes your player.
        
        if you find yourself with a superior eval function, update the default 
        value of `eval_fn` to `CustomEvalFn()`
        
        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Utility function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, legal_moves, time_left):
        """Called to determine one move by your agent
        
        Args:
            game (Board): The board and game state.
            legal_moves (dict): Dictionary of legal moves and their outcomes
            time_left (function): Used to determine time left before timeout
            
        Returns:
            (tuple, int): best_move, best_queen
        """
        best_move, best_queen, utility = self.alphabeta(game, time_left, depth=self.search_depth)
        # change minimax to alphabeta after completing alphabeta part of assignment
        if best_move == None:
            print '***********Got NULL Move!'
        return best_move, best_queen

    def utility(self, game):
        """Can be updated if desired"""
        return self.eval_fn.score(game)

    def getMoveList(self, queenDict):
        moveDict = dict()
        for queen in queenDict:
            for move in queenDict[queen]:
                moveDict[move] = queen
        return moveDict

    def isTerminal(self, game, maximizing_player):
        """ Determines is the current game state
            is done with. In this, either player1
            or Player 2 will have 0 moves left
        """
        aq1 = game.get_active_players_queen()[0]
        aq2 = game.get_active_players_queen()[1]
        # iq1 = game.get_inactive_players_queen()[0]
        # iq2 = game.get_inactive_players_queen()[1]
        ap = game.get_legal_moves()
        # ip = game.get_opponent_moves()

        apMoves = len(ap[aq1]) + len(ap[aq2])
        # ipMoves = len(ip[iq1]) + len(ip[iq2])

        if maximizing_player:
            return apMoves == 0
        # if apMoves==0 or ipMoves==0:
        #     return True
        # return False

    def minimax(self, game, time_left, depth=float("inf"), maximizing_player=True):
        """Implementation of the minimax algorithm
        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple, int, int): best_move, best_queen, best_val
        """
        best_move = None
        best_queen = None
        best_val = None
        if depth <= 0 or time_left()<=100 or self.isTerminal(game,maximizing_player):            
            best_val = self.eval_fn.score(game,maximizing_player)
            return best_move,best_queen,best_val
        
        if maximizing_player:
            best_val = float("-inf")
            moveDict = self.getMoveList(game.get_legal_moves())
            for move in moveDict:
                tmpMove, tmpQueen, tmpVal = self.minimax(game.forecast_move(move,moveDict[move]),time_left,depth-1,False)
                if tmpVal > best_val:
                    best_val = tmpVal
                    best_queen = moveDict[move]
                    best_move = move
                if time_left() <= 50: 
                    break
            return best_move,best_queen,best_val
        else:
            best_val = float("+inf")
            moveDict = self.getMoveList(game.get_legal_moves())
            for move in moveDict:
                tmpMove, tmpQueen, tmpVal = self.minimax(game.forecast_move(move,moveDict[move]),time_left,depth-1,True)
                if tmpVal < best_val:
                    best_val = tmpVal
                    best_queen = moveDict[move]
                    best_move = move
                if time_left() <= 50: 
                    break
            return best_move,best_queen,best_val


    def alphabeta(self, game, time_left, depth=float("inf"), alpha=float("-inf"), beta=float("inf"),
                  maximizing_player=True):
        """Implementation of the alphabeta algorithm
        
        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple, int, int): best_move, best_queen, best_val
        """
        best_move = None
        best_queen = None
        best_val = None
        if depth <= 0 or time_left()<=100 or self.isTerminal(game,maximizing_player):            
            best_val = self.eval_fn.score(game,maximizing_player)
            return best_move,best_queen,best_val
        if maximizing_player:
            best_val = alpha
            moveDict = self.getMoveList(game.get_legal_moves())
            for move in moveDict: 
                tmpMove, tmpQueen, tmpVal = self.alphabeta(game.forecast_move(move,moveDict[move]),time_left,depth-1,alpha,beta,False)
                if tmpVal > best_val:
                    best_val = tmpVal
                    best_queen = moveDict[move]
                    best_move = move
                alpha = max(best_val,alpha)
                if beta <= alpha:
                    break
                if time_left() <= 50: 
                    break
            return best_move,best_queen,best_val
        else:
            best_val = beta
            moveDict = self.getMoveList(game.get_legal_moves())
            for move in moveDict: 
                tmpMove, tmpQueen, tmpVal = self.alphabeta(game.forecast_move(move,moveDict[move]),time_left,depth-1,alpha,beta,True)
                if tmpVal < best_val:
                    best_val = tmpVal
                    best_queen = moveDict[move]
                    best_move = move
                beta = min(best_val,beta)
                if beta >= alpha:
                    break
                if time_left() <= 50: 
                    break
            return best_move,best_queen,best_val


class CustomPlayerAB(CustomPlayer):
    def __init__(self, search_depth=3, eval_fn=OpenMoveEvalFn()):
        """Initializes your player.
        
        if you find yourself with a superior eval function, update the default 
        value of `eval_fn` to `CustomEvalFn()`
        
        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Utility function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, legal_moves, time_left):
        """Called to determine one move by your agent
        
        Args:
            game (Board): The board and game state.
            legal_moves (dict): Dictionary of legal moves and their outcomes
            time_left (function): Used to determine time left before timeout
            
        Returns:
            (tuple, int): best_move, best_queen
        """
        best_move, best_queen, utility = self.alphabeta(game, time_left, depth=self.search_depth)
        # change minimax to alphabeta after completing alphabeta part of assignment
        if best_move == None:
            print '***********Got NULL Move!'
        return best_move, best_queen
