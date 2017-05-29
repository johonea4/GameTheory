from copy import deepcopy
from time import time, sleep
import platform
# import io
import random
import StringIO
import sys
import os

if platform.system() != 'Windows':
    import resource

sys.path[0] = os.getcwd()


class Board:
    BLANK = 0
    NOT_MOVED = (-1, -1)
    __active_queen__ = None
    __active_players_queen1__ = None
    __inactive_players_queen1__ = None
    __active_players_queen2__ = None
    __inactive_players_queen2__ = None

    def __init__(self, player_1, player_2, width=7, height=7):
        self.mistake_count = 0
        self.width = width
        self.height = height

        self.queen_11 = "queen11"
        self.queen_12 = "queen12"
        self.queen_21 = "queen21"
        self.queen_22 = "queen22"

        self.__board_state__ = [[Board.BLANK for i in range(0, width)] for j in range(0, height)]
        self.__last_queen_move__ = {self.queen_11: Board.NOT_MOVED, self.queen_12: Board.NOT_MOVED,
                                    self.queen_21: Board.NOT_MOVED, self.queen_22: Board.NOT_MOVED}
        self.__queen_symbols__ = {Board.BLANK: Board.BLANK, self.queen_11: 11, self.queen_12: 12, self.queen_21: 21,
                                  self.queen_22: 22}

        self.move_count = 0

        self.__queen_11__ = self.queen_11
        self.__queen_12__ = self.queen_12
        self.__queen_21__ = self.queen_21
        self.__queen_22__ = self.queen_22

        self.__player_1__ = player_1
        self.__player_2__ = player_2

        self.__active_player__ = player_1
        self.__inactive_player__ = player_2

        self.__active_players_queen1__ = 11
        self.__active_players_queen2__ = 12
        self.__inactive_players_queen1__ = 21
        self.__inactive_players_queen2__ = 22

    def get_queen_name(self, queen_num):
        if queen_num == 11:
            return self.queen_11
        elif queen_num == 12:
            return self.queen_12
        elif queen_num == 21:
            return self.queen_21
        elif queen_num == 22:
            return self.queen_22
        else:
            return None

    def get_state(self):
        return deepcopy(self.__board_state__)

    def __apply_move__(self, move, uncertainty=True):
        cur_row, cur_col = self.__last_queen_move__[self.__active_queen__]
        row, col = move
        if uncertainty:
            distance = max(abs(cur_row - row), abs(cur_col - col))
            if distance < 2:
                mistake_prob = 0
            elif distance >= 5:
                mistake_prob = 0.9
            else:
                mistake_prob = (0.4, 0.6, 0.8)[distance - 2]

            if random.random() < mistake_prob:
                directions = [(-1, -1), (-1, 0), (-1, 1),
                              (0, -1), (0, 1),
                              (1, -1), (1, 0), (1, 1)]
                mistakes = [(row + dr, col + dc) for dr, dc in directions
                            if self.move_is_legal(row + dr, col + dc)]
                if mistakes:
                    self.mistake_count += 1
                    move = random.choice(mistakes)
                    row, col = move
        self.__last_queen_move__[self.__active_queen__] = move
        self.__board_state__[row][col] = self.__queen_symbols__[self.__active_queen__]
        # swap the players

        tmp = self.__active_player__
        self.__active_player__ = self.__inactive_player__
        self.__inactive_player__ = tmp

        # swaping the queens

        tmp = self.__active_players_queen1__
        self.__active_players_queen1__ = self.__inactive_players_queen1__
        self.__inactive_players_queen1__ = tmp

        tmp = self.__active_players_queen2__
        self.__active_players_queen2__ = self.__inactive_players_queen2__
        self.__inactive_players_queen2__ = tmp

        self.move_count = self.move_count + 1
        return move

    def __apply_move_write__(self, move, __active_queen__):
        row, col = move
        self.__last_queen_move__[__active_queen__] = move
        self.__board_state__[row][col] = self.__queen_symbols__[__active_queen__]

        # swap the players

        tmp = self.__active_player__
        self.__active_player__ = self.__inactive_player__
        self.__inactive_player__ = tmp
        self.move_count = self.move_count + 1

    def copy(self):
        b = Board(self.__player_1__, self.__player_2__, width=self.width, height=self.height)
        for key, value in self.__last_queen_move__.items():
            b.__last_queen_move__[key] = value
        for key, value in self.__queen_symbols__.items():
            b.__queen_symbols__[key] = value
        b.move_count = self.move_count
        b.__active_player__ = self.__active_player__
        b.__inactive_player__ = self.__inactive_player__
        b.__active_queen__ = self.__active_queen__
        b.__active_players_queen1__ = self.__active_players_queen1__
        b.__active_players_queen2__ = self.__active_players_queen2__
        b.__inactive_players_queen1__ = self.__inactive_players_queen1__
        b.__inactive_players_queen2__ = self.__inactive_players_queen2__
        b.__board_state__ = self.get_state()
        return b

    def set_active_queen(self, queen):
        if queen == 11:
            self.__active_queen__ = self.queen_11
        elif queen == 12:
            self.__active_queen__ = self.queen_12
        elif queen == 21:
            self.__active_queen__ = self.queen_21
        else:
            self.__active_queen__ = self.queen_22

    def forecast_move(self, move, queen):
        new_board = self.copy()
        new_board.set_active_queen(queen)
        new_board.__apply_move__(move, uncertainty=False)
        return new_board

    def get_active_player(self):
        return self.__active_player__

    def get_inactive_player(self):
        return self.__inactive_player__

    def get_active_players_queen(self):
        return self.__active_players_queen1__, self.__active_players_queen2__

    def get_inactive_players_queen(self):
        return self.__inactive_players_queen1__, self.__inactive_players_queen2__

    def get_active_queen(self):
        return self.__active_queen__

    def get_opponent_moves(self):
        """Returns the possible moves of both queens and the possible results of those moves, 
        The format that's returned is the following:
        {
        queen:  {
                        (move_x, move_y): 
                            [((pos_x, pos_y), likelihood),
                                ....]
                    }
        }
        where (move_x, move_y) is the intended target, (pos_x, pos_y) is a space that move might result in, and
        likelihood is the chance that result happens.

        An example of iterating through this nested dictionary is included below:

        move_dict = self.get_opponent_moves()
        for move in move_dict:
            move_x, move_y = move
            for (pos_x, pos_y), likelihood in move_dict[move]:
                # do something

        All 4 queens must be placed on the board in the first 4 moves
        """

        # changed to include edge cases!
        move_by_q1 = self.__last_queen_move__[self.get_queen_name(self.__inactive_players_queen1__)]
        move_by_q2 = self.__last_queen_move__[self.get_queen_name(self.__inactive_players_queen2__)]

        if move_by_q1 == Board.NOT_MOVED and move_by_q2 == Board.NOT_MOVED:
            return {self.__inactive_players_queen1__: self.__get_moves__(move_by_q1),
                    self.__inactive_players_queen2__: self.__get_moves__(move_by_q2)}

        elif move_by_q1 == Board.NOT_MOVED and move_by_q2 != Board.NOT_MOVED:
            return {self.__inactive_players_queen1__: self.__get_moves__(move_by_q1),
                    self.__inactive_players_queen2__: {}}

        elif move_by_q1 != Board.NOT_MOVED and move_by_q2 == Board.NOT_MOVED:
            return {self.__inactive_players_queen1__: {},
                    self.__inactive_players_queen2__: self.__get_moves__(move_by_q2)}

        else:
            return {self.__inactive_players_queen1__: self.__get_moves__(move_by_q1),
                    self.__inactive_players_queen2__: self.__get_moves__(move_by_q2)}

    def get_legal_moves(self):
        """Returns the possible moves of both queens and the possible results of those moves, 
        The format that's returned is the following:
        {
        queen:  {
                        (move_x, move_y): 
                            [((pos_x, pos_y), likelihood),
                                ....]
                    }
        }
        where (move_x, move_y) is the intended target, (pos_x, pos_y) is a space that move might result in, and
        likelihood is the chance that result happens.
        An example of iterating through this nested dictionary is included below:
        move_dict = game.get_legal_moves()
        for queen in move_dict:
            for move in move_dict[queen]:
                move_x, move_y = move
                print move_x, move_y
                for (pos_x, pos_y), likelihood in move_dict[queen][move]:
                    print pos_x, pos_y, likelihood
                    # do something
        All 4 queens must be placed on the board in the first 4 moves
        """
        move_by_q1 = self.__last_queen_move__[self.get_queen_name(self.__active_players_queen1__)]
        move_by_q2 = self.__last_queen_move__[self.get_queen_name(self.__active_players_queen2__)]

        if move_by_q1 == Board.NOT_MOVED and move_by_q2 == Board.NOT_MOVED:
            return {self.__active_players_queen1__: self.__get_moves__(move_by_q1),
                    self.__active_players_queen2__: self.__get_moves__(move_by_q2)}

        elif move_by_q1 == Board.NOT_MOVED and move_by_q2 != Board.NOT_MOVED:
            return {self.__active_players_queen1__: self.__get_moves__(move_by_q1), self.__active_players_queen2__: {}}

        elif move_by_q1 != Board.NOT_MOVED and move_by_q2 == Board.NOT_MOVED:
            return {self.__active_players_queen1__: {}, self.__active_players_queen2__: self.__get_moves__(move_by_q2)}

        else:
            return {self.__active_players_queen1__: self.__get_moves__(move_by_q1),
                    self.__active_players_queen2__: self.__get_moves__(move_by_q2)}

    def get_legal_moves_of_queen1(self):
        return self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__active_players_queen1__)])

    def get_legal_moves_of_queen2(self):
        return self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__active_players_queen2__)])

    def __get_moves__(self, move):
        # Changed this function. Now the piece will move like QUEEN not like KING.

        if move == self.NOT_MOVED or self.move_count < 2:
            first_moves = self.get_first_moves()
            return {move: [(move, 1.0)] for move in first_moves}
        start_r, start_c = move

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        fringe = [((start_r + dr, start_c + dc), (dr, dc)) for dr, dc in directions
                  if self.move_is_legal(start_r + dr, start_c + dc)]

        valid_moves = []

        while fringe:
            move, delta = fringe.pop()

            r, c = move
            dr, dc = delta

            if self.move_is_legal(r, c):
                new_move = ((r + dr, c + dc), (dr, dc))
                fringe.append(new_move)
                valid_moves.append(move)
        move_possibilities = {}
        for r, c in valid_moves:
            distance = max(abs(r - start_r), abs(c - start_c))
            if distance < 2:
                move_possibilities[(r, c)] = [((r, c), 1.0)]
            else:
                mistakes = [(r + dr, c + dc) for dr, dc in directions
                            if self.move_is_legal(r + dr, c + dc)]
                n_choices = len(mistakes)
                if distance >= 5:
                    mistake_prob = 0.9
                else:
                    mistake_prob = (0.4, 0.6, 0.8)[distance - 2]
                outcomes = [((r2, c2), mistake_prob / n_choices) for r2, c2 in mistakes]
                outcomes.append(((r, c), 1 - mistake_prob))
                move_possibilities[(r, c)] = outcomes[:]

        return move_possibilities

    def get_first_moves(self):
        return [(i, j) for i in range(0, self.height) for j in range(0, self.width) if
                self.__board_state__[i][j] == Board.BLANK]

    def move_is_legal(self, row, col):
        return 0 <= row < self.height and \
               0 <= col < self.width and \
               self.__board_state__[row][col] == Board.BLANK

    def get_player_locations(self, queen):
        return [(i, j) for j in range(0, self.width) for i in range(0, self.height) if
                self.__board_state__[i][j] == self.__queen_symbols__[queen]]

    def print_board(self):

        p11_r, p11_c = self.__last_queen_move__[self.__queen_11__]
        p12_r, p12_c = self.__last_queen_move__[self.__queen_12__]
        p21_r, p21_c = self.__last_queen_move__[self.__queen_21__]
        p22_r, p22_c = self.__last_queen_move__[self.__queen_22__]
        b = self.__board_state__

        out = u'   \u250f'
        for j in range(0, len(b[0]) - 1):
            out += ' ' + str(j) + u'  \u2533'
        out += str(len(b[0]) - 1).rjust(2) + u'  \u2513'
        out += '\n\r'
        for i in range(0, len(b)):
            out += str(i).center(3) + u'\u250b '
            for j in range(0, len(b[i])):
                if not b[i][j]:
                    out += '  '

                elif i == p11_r and j == p11_c:
                    out += '11'
                elif i == p12_r and j == p12_c:
                    out += '12'
                elif i == p21_r and j == p21_c:
                    out += '21'
                elif i == p22_r and j == p22_c:
                    out += '22'
                else:
                    out += '--'

                out += u' \u250b '
            out += '\n\r'
        out += u'   \u2517' + u' \u2505\u2009\u2505 \u253b' * (len(b[0]) - 1) + u' \u2505\u2009\u2505 \u251b'
        return out

    def play_isolation(self, time_limit=5000, print_moves=False):
        # changed the time_limit
        self.output_history = []
        move_history = []
        queen_history = []
        mi = 1

        if platform.system() == 'Windows':
            def curr_time_millis():
                return int(round(time() * 1000))
        else:
            def curr_time_millis():
                return 1000 * resource.getrusage(resource.RUSAGE_SELF).ru_utime
        while True:
            game_copy = self.copy()
            move_start = curr_time_millis()

            def time_left(): return time_limit - (curr_time_millis() - move_start)
            curr_move = Board.NOT_MOVED

            legal_player_moves = self.get_legal_moves()
            curr_move, queen = self.__active_player__.move(game_copy, legal_player_moves,
                                                           time_left)  # queen added in return
            if queen == None:
                return self.__inactive_player__, move_history, queen_history, "illegal move"
            self.set_active_queen(queen)

            if curr_move is None:
                curr_move = Board.NOT_MOVED

            if self.__active_player__ == self.__player_1__:
                move_history.append([curr_move])
                queen_history.append([self.__active_queen__])
            else:
                move_history[-1].append(curr_move)
                queen_history[-1].append(self.__active_queen__)

            if time_limit and time_left() <= 0:
                if print_moves:
                    print 'Winner: ' + str(self.__inactive_player__)
                return self.__inactive_player__, move_history, queen_history, "timeout"

            legal_moves_of_queen1 = self.get_legal_moves_of_queen1()
            legal_moves_of_queen2 = self.get_legal_moves_of_queen2()

            if self.__active_players_queen1__ == queen and curr_move not in legal_moves_of_queen1:
                if print_moves:
                    print 'Winner: ' + str(self.__inactive_player__)
                return self.__inactive_player__, move_history, queen_history, "illegal move"

            if self.__active_players_queen2__ == queen and curr_move not in legal_moves_of_queen2:
                if print_moves:
                    print 'Winner: ' + str(self.__inactive_player__)
                return self.__inactive_player__, move_history, queen_history, "illegal move"

            if curr_move not in legal_moves_of_queen1 and curr_move not in legal_moves_of_queen2:
                if print_moves:
                    print 'Winner: ' + str(self.__inactive_player__)
                return self.__inactive_player__, move_history, queen_history, "illegal move"

            last_attempt = curr_move
            if self.move_count > 3:
                last_move = self.__apply_move__(curr_move)
            else:
                last_move = self.__apply_move__(curr_move, uncertainty=False)
            if self.__active_player__ == self.__player_1__:
                move_history[-1][1] = last_move
            else:
                move_history[-1][0] = last_move

            if self.__inactive_player__ == self.__player_1__:
                output = "player1's "
            else:
                output = "player2's "
            output += queen_history[-1][-1]
            if last_move != last_attempt:
                output += ' attempted (%d,%d),' % last_attempt
            output += ' moved to (%d,%d)' % last_move
            self.output_history.append(output)
            if print_moves:
                print output
                print self.print_board()


def game_as_text(winner, move_history, queen_history, output_history, termination="", board=Board(1, 2)):
    print(winner)
    # ans = io.StringIO()
    ans = StringIO.StringIO()
    k = 0
    for i, move1 in enumerate(move_history):
        p1_move = move1[0]
        if len(output_history) > i * 2:
            ans.write(output_history[i * 2] + '\r\n')
        else:
            ans.write('player1 lost: ' + termination + '\r\n')
            ans.write("Winner: " + str(winner) + "\r\n")
            ans.write(board.__active_player__ == board.__player_1__)
            return ans.getvalue()
        if p1_move != Board.NOT_MOVED:
            board.__apply_move_write__(p1_move, queen_history[k][0])
        ans.write(board.print_board())

        if len(move1) > 1:
            p2_move = move1[1]
            if len(output_history) > i * 2 + 1:
                ans.write(output_history[i * 2 + 1] + '\r\n')
            else:
                ans.write('player2 lost: ' + termination + '\r\n')
                ans.write("Winner: " + str(winner) + "\r\n")
                return ans.getvalue()
            if p2_move != Board.NOT_MOVED:
                board.__apply_move_write__(p2_move, queen_history[k][1])
            ans.write(board.print_board())
        k = k + 1


def main():
    print("Starting game:")

    from test_players import RandomPlayer
    from test_players import HumanPlayer

    board = Board(RandomPlayer(), HumanPlayer())
    board_copy = board.copy()
    winner, move_history, queen_history, termination = board.play_isolation(time_limit=30000, print_moves=True)
    print game_as_text(winner, move_history, queen_history, board.output_history, termination, board_copy)

if __name__ == '__main__':
    main()
