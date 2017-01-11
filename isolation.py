from copy import deepcopy
from time import time, sleep
import resource
import io
#import StringIO

# Annoying hack for when script itself is a symlink
import sys,os
sys.path[0] = os.getcwd()

class Board:
    BLANK = 0
    NOT_MOVED = (-1, -1)
    __active_queen__= None
    __active_players_queen1__= None                        ## additional things for minimax and alpha beta so that oyu can predict
    __inactive_players_queen1__= None
    __active_players_queen2__= None                        ## additional things for minimax and alpha beta so that oyu can predict
    __inactive_players_queen2__= None
    
    
    def __init__(self, player_1, player_2, width=7, height=7):
        self.width=width
        self.height=height
        
        self.queen_11 = "queen11"
        self.queen_12 = "queen12"
        self.queen_21 = "queen21"
        self.queen_22 = "queen22"
        
        self.__board_state__ = [ [Board.BLANK for i in range(0, width)] for j in range(0, height)]
        self.__last_queen_move__ = {self.queen_11:Board.NOT_MOVED, self.queen_12:Board.NOT_MOVED, self.queen_21:Board.NOT_MOVED, self.queen_22:Board.NOT_MOVED} #change
        self.__queen_symbols__ = {Board.BLANK: Board.BLANK, self.queen_11:11, self.queen_12:12, self.queen_21:21, self.queen_22:22}     #change
        
        
        #self.__player_symbols__ = {Board.BLANK: Board.BLANK, player_1:1, player_2:2}
        self.move_count = 0
        
        self.__queen_11__ = self.queen_11
        self.__queen_12__ = self.queen_12
        self.__queen_21__ = self.queen_21
        self.__queen_22__ = self.queen_22
        #self.__active_queen__ = self.queen_2;
        #self.__inactive_queen__ =self.queen_1;
        
        
        self.__player_1__ = player_1
        self.__player_2__ = player_2
        
        
        self.__active_player__ = player_1
        self.__inactive_player__ = player_2 
        
        self.__active_players_queen1__= 11                    
        self.__active_players_queen2__= 12
        self.__inactive_players_queen1__= 21 
        self.__inactive_players_queen2__= 22 
        
        
    def get_queen_name(self, queen_num):
        if queen_num == 11:
            return self.queen_11
        elif queen_num ==12:
            return self.queen_12
        elif queen_num == 21:
            return self.queen_21
        elif queen_num ==22:
            return self.queen_22
        else :
            return None
            
    
    def get_state(self):
        return deepcopy(self.__board_state__)

    def set_active_queen_from_move(self, move):
        if move in self.get_legal_moves_of_queen1():
            self.set_active_queen(self.__active_players_queen1__)
        if move in self.get_legal_moves_of_queen2():
            self.set_active_queen(self.__active_players_queen2__)    
        
    def __apply_move__(self, move):
        row,col = move
        self.set_active_queen_from_move(move)
        self.__last_queen_move__[self.__active_queen__] = move     
        self.__board_state__[row][col] = self.__queen_symbols__[self.__active_queen__]   
        
        #swap the players
        
        tmp = self.__active_player__
        self.__active_player__ = self.__inactive_player__
        self.__inactive_player__ = tmp
        
        #swaping the queens
        
        tmp = self.__active_players_queen1__
        self.__active_players_queen1__ = self.__inactive_players_queen1__
        self.__inactive_players_queen1__ = tmp
        
        tmp = self.__active_players_queen2__
        self.__active_players_queen2__ = self.__inactive_players_queen2__
        self.__inactive_players_queen2__ = tmp
        
        self.move_count = self.move_count + 1
        
        

    def __apply_move_write__(self, move, __active_queen__):
        row,col = move
        self.__last_queen_move__[__active_queen__] = move     
        self.__board_state__[row][col] = self.__queen_symbols__[__active_queen__]   
        
        #swap the players
        
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
        #b.__inactive_queen__ = self.__inactive_queen__       ################incactive quen
        b.__active_players_queen1__ = self.__active_players_queen1__
        b.__active_players_queen2__ = self.__active_players_queen2__
        b.__board_state__ = self.get_state()
        return b
    
    def set_active_queen(self, queen):                       ###########################CHANGE INACTIVE
        if(queen==11):
            self.__active_queen__=self.queen_11
    #       self.__inactive_queen__=self.queen_21
        elif(queen==12):
            self.__active_queen__=self.queen_12
    #        self.__inactive_queen__=self.queen_22
        elif(queen==21):
            self.__active_queen__=self.queen_21
    #        self.__inactive_queen__=self.queen_11
        else:
            self.__active_queen__=self.queen_22
    #        self.__inactive_queen__=self.queen_12
            
    #def set_active_queen(self, queen):                       ###########################CHANGE INACTIVE
    #    self.__active_queen__=queen
            

    def forecast_move(self, move):      ###########################inactive part of forecast
        new_board = self.copy()
        new_board.__apply_move__(move)
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
    
    
    #def get_inactive_queen(self):                   ###########################CHANGE INACTIVE
    #    return self.__inactive_queen__

    def is_winner(self, player): # need ot check
        return not self.get_legal_moves() and player== self.__inactive_player__

    def is_opponent_winner(self, player): # need ot check
        return not self.get_legal_moves() and player== self.__active_player__

    def get_opponent_moves(self):                     ####################################trouble can make it better
        return self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__inactive_players_queen1__)]) + self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__inactive_players_queen2__)])

    def get_legal_moves(self):
        return self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__active_players_queen1__)]) + self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__active_players_queen2__)])
        
            
    def get_legal_moves_of_queen1(self):
        return self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__active_players_queen1__)])

    def get_legal_moves_of_queen2(self):
        return self.__get_moves__(self.__last_queen_move__[self.get_queen_name(self.__active_players_queen2__)])
    
    def __get_moves__(self, move):
        if move == Board.NOT_MOVED:
            return self.get_first_moves()

        r, c = move
        directions = [ (-1, -1), (-1, 0), (-1, 1),
                        (0, -1),          (0,  1),
                        (1, -1), (1,  0), (1,  1)]
        
        
        valid_moves = [(r+dr,c+dc) for dr, dc in directions
                if self.move_is_legal(r+dr, c+dc)]

        return valid_moves

    def get_first_moves(self):
        return [ (i,j) for i in range(0,self.height) for j in range(0,self.width) if self.__board_state__[i][j] == Board.BLANK]

    def move_is_legal(self, row, col):
        return 0 <= row < self.height and \
               0 <= col < self.width  and \
                self.__board_state__[row][col] == Board.BLANK

    def get_player_locations(self, player):                            ############check please!!!!
        return [ (i,j) for j in range(0, self.width) for i in range(0,self.height) if self.__board_state__[i][j] == self.__queen_symbols__[player]]


    def print_board(self):

        p11_r, p11_c = self.__last_queen_move__[self.__queen_11__]
        p12_r, p12_c = self.__last_queen_move__[self.__queen_12__]
        p21_r, p21_c = self.__last_queen_move__[self.__queen_21__]
        p22_r, p22_c = self.__last_queen_move__[self.__queen_22__]
        b = self.__board_state__

        out = ''

        for i in range(0, len(b)):
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

                out += ' | '
            out += '\n\r'

        return out

    #def __stub_inactive_player__(self, game_copy):
    #    old_inactive = self.__inactive_player__
    #    game_copy.__inactive_player__ = self.__player_symbols__[self.__inactive_player__]
    #    new_inactive = game_copy.__inactive_player__

    #    game_copy.__last_player_move__[new_inactive] = game_copy.__last_player_move__[old_inactive]
    #    game_copy.__player_symbols__[new_inactive] = game_copy.__player_symbols__[old_inactive]
    #    if game_copy.__player_1__ == old_inactive:
    #        game_copy.__player_1__ = new_inactive
    #    else:
    #        game_copy.__player_2__ = new_inactive

    #    game_copy.__last_player_move__.pop(old_inactive, None)
    #    game_copy.__player_symbols__.pop(old_inactive, None)

    #    return game_copy


    def play_isolation(self, time_limit = None):
        move_history = []
        queen_history =[]
        mi=1
        curr_time_millis = lambda : 1000 * resource.getrusage(resource.RUSAGE_SELF).ru_utime
        
       


        while True:

            #legal_player_moves =  self.get_legal_moves() # This is only provided as an added benefit
            # The copy is here to not penalize the students
            
            game_copy = self.copy()
            #game_copy = self.__stub_inactive_player__(game_copy)

            move_start = curr_time_millis()

            time_left = lambda : time_limit - (curr_time_millis() - move_start)
            curr_move = Board.NOT_MOVED
            try:
                
                legal_moves_of_queen1 =  self.get_legal_moves_of_queen1()
                legal_moves_of_queen2 =  self.get_legal_moves_of_queen2()
                legal_player_moves=legal_moves_of_queen1+legal_moves_of_queen2                
                curr_move = self.__active_player__.move(game_copy,legal_player_moves , time_left)
                
            except AttributeError as e:
                raise e
            except Exception as e:
                print("exception")
                print(e)
                pass
            
            
            #else:
            #    return self.__inactive_player__, move_history,queen_history, "choosen wrong players queen"
                

            if curr_move is None:
                curr_move = Board.NOT_MOVED
                
            elif curr_move in legal_moves_of_queen1:
                self.set_active_queen(self.__active_players_queen1__)
            elif curr_move in legal_moves_of_queen2:
                self.set_active_queen(self.__active_players_queen2__)
            else:
                self.__active_queen__="No queen"
                
                
            if self.__active_player__ == self.__player_1__:
                move_history.append([curr_move])
                queen_history.append([self.__active_queen__])
            else:
                move_history[-1].append(curr_move)
                queen_history[-1].append(self.__active_queen__)

            if time_limit and time_left() <= 0:
                return  self.__inactive_player__, move_history,queen_history, "timeout"
            if curr_move not in legal_player_moves:
                return self.__inactive_player__, move_history,queen_history, "illegal move"
            
            self.__apply_move__(curr_move)


def game_as_text(winner, move_history,queen_history, termination="", board=Board(1,2)):
    print(winner)
    ans = io.StringIO()
    k=0
    for i, move1 in enumerate(move_history):
        p1_move = move1[0]
        ans.write(queen_history[k][0]+"  player1 "+"%d." % i + " (%d,%d)\r\n" % p1_move)
        if p1_move != Board.NOT_MOVED:
            board.__apply_move_write__(p1_move, queen_history[k][0])
        ans.write(board.print_board())

        if len(move1) > 1:
            p2_move = move1[1]
            ans.write(queen_history[k][1]+" player2 "+"%d. ..." % i + " (%d,%d)\r\n" % p2_move)
            if p2_move != Board.NOT_MOVED:
                board.__apply_move_write__(p2_move , queen_history[k][1])
            ans.write(board.print_board())
        k=k+1
    ans.write(termination + "\r\n")
    ans.write("Winner: " + str(winner) + "\r\n")

    return ans.getvalue()

if __name__ == '__main__':

    print("Starting game:")


    from test_players import RandomPlayer
    from test_players import HumanPlayer

    board = Board(RandomPlayer(), HumanPlayer())
    winner, move_history,queen_history, termination = board.play_isolation()
    print (game_as_text(winner, move_history,queen_history, termination))
