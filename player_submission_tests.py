#!/usr/bin/env python
import traceback
from player_submission import OpenMoveEvalFn, CustomEvalFn, CustomPlayer, CustomPlayerAB
from isolation import Board, game_as_text
from test_players import RandomPlayer, HumanPlayer, HumanPlayer2

def testUtility():
    try:
        sample_board = Board(RandomPlayer(), RandomPlayer())
        # setting up the board as though we've been playing
        sample_board.move_count = 4
        sample_board.__board_state__ = [
            [11, 0, 0, 0, 21, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 22, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 12, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        sample_board.__last_queen_move__ = {sample_board.queen_11: (0, 0), sample_board.queen_12: (4, 5),
                                            sample_board.queen_21: (0, 4), sample_board.queen_22: (2, 2)}
        test = sample_board.get_legal_moves()
        h = OpenMoveEvalFn()
        print 'OpenMoveEvalFn Test: This board has a score of %s.' % (h.score(sample_board))
        sample_board.print_board()
    except NotImplementedError:
        print 'OpenMoveEvalFn Test: Not implemented'
    except:
        print 'OpenMoveEvalFn Test: ERROR OCCURRED'
        print traceback.format_exc()

def testMiniMax():
    try:
        """Example test to make sure
        your minimax works, using the
        #computer_player_moves - opponent_moves evaluation function."""
        # create dummy 3x3 board

        p1 = RandomPlayer()
        p2 = CustomPlayerAB(search_depth=3)
        #p2 = HumanPlayer()
        b = Board(p1, p2, 5, 5)
        b.__board_state__ = [
            [0, 21, 0, 0, 0],
            [0, 0, 11, 0, 0],
            [0, 0, 12, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 22, 0, 0, 0]
        ]
        b.__last_queen_move__["queen11"] = (1, 2)
        b.__last_queen_move__["queen21"] = (0, 1)
        b.__last_queen_move__["queen12"] = (2, 2)
        b.__last_queen_move__["queen22"] = (4, 1)

        b.move_count = 4

        output_b = b.copy()
        winner, move_history, queen_history, termination = b.play_isolation(1000,True)
        print 'Minimax Test: Runs Successfully'
        # Uncomment to see example game
        print game_as_text(winner, move_history, queen_history, b.output_history, termination, output_b)
    except NotImplementedError:
        print 'Minimax Test: Not Implemented'
    except:
        print 'Minimax Test: ERROR OCCURRED'
        print traceback.format_exc()

def testCustomPlayRandom():
    """Example test you can run
    to make sure your AI does better
    than random."""
    try:
        r = CustomPlayer(search_depth=3)
        h = RandomPlayer()
        game = Board(r, h, 7, 7)
        output_b = game.copy()
        winner, move_history, queen_history, termination = game.play_isolation(1000,True)
        game.print_board()
        print game_as_text(winner, move_history, queen_history, game.output_history, termination, output_b)
    except NotImplementedError:
        print 'CustomPlayer Test: Not Implemented'
    except:
        print 'CustomPlayer Test: ERROR OCCURRED'
        print traceback.format_exc()

def testCustomABPlayRandom():
    """Example test you can run
    to make sure your AI does better
    than random."""
    try:
        r = CustomPlayerAB(search_depth=10)
        h = RandomPlayer()
        game = Board(r, h, 7, 7)
        output_b = game.copy()
        winner, move_history, queen_history, termination = game.play_isolation(1000,True)
        game.print_board()
        print game_as_text(winner, move_history, queen_history, game.output_history, termination, output_b)
    except NotImplementedError:
        print 'CustomPlayer Test: Not Implemented'
    except:
        print 'CustomPlayer Test: ERROR OCCURRED'
        print traceback.format_exc()

def testCustomPlayCustomAB():
    """Example test you can run
    to make sure your AI does better
    than random."""
    try:
        r = CustomPlayer(search_depth=3)
        h = CustomPlayerAB(search_depth=10)
        game = Board(r, h, 7, 7)
        output_b = game.copy()
        winner, move_history, queen_history, termination = game.play_isolation(1000,True)
        game.print_board()
        print game_as_text(winner, move_history, queen_history, game.output_history, termination, output_b)
    except NotImplementedError:
        print 'CustomPlayer Test: Not Implemented'
    except:
        print 'CustomPlayer Test: ERROR OCCURRED'
        print traceback.format_exc()

def testCustomABPlayHuman2():
    """Example test you can run
    to make sure your AI does better
    than random."""
    try:
        r = CustomPlayerAB(search_depth=10)
        h = HumanPlayer2()
        game = Board(r, h, 7, 7)
        output_b = game.copy()
        winner, move_history, queen_history, termination = game.play_isolation(30000,True)
        game.print_board()
        print game_as_text(winner, move_history, queen_history, game.output_history, termination, output_b)
    except NotImplementedError:
        print 'CustomPlayer Test: Not Implemented'
    except:
        print 'CustomPlayer Test: ERROR OCCURRED'
        print traceback.format_exc()

def main():
    # testUtility()
    # testMiniMax()
    # testCustomPlayRandom()
    # testCustomABPlayRandom()
    # testCustomPlayCustomAB()
    testCustomABPlayHuman2()

if __name__ == "__main__":
    main()
