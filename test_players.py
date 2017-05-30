from random import randint


class RandomPlayer():
    """Player that chooses a move randomly."""    

    def move(self, game, legal_moves, time_left):
        if not legal_moves: return (-1,-1)        
        num=randint(game.__active_players_queen1__,game.__active_players_queen2__)
        if not len(legal_moves[num]):
            num = game.__active_players_queen1__ if num == game.__active_players_queen2__ else game.__active_players_queen2__
            if not len(legal_moves[num]):
                return (-1,-1), num
        
        moves = legal_moves[num].keys()[randint(0,len(legal_moves[num])-1)]
        return moves, num
    


class HumanPlayer():
    """Player that chooses a move according to
    user's input."""
    def move(self, game, legal_moves, time_left):
        i=0
        choice = {}
        if not len(legal_moves[game.__active_players_queen1__]) and not len(legal_moves[game.__active_players_queen2__]):
            return None, None
        for queen in legal_moves:
            for move in sorted(legal_moves[queen].keys()):
                    choice.update({i:(queen,move)})
                    if (i + 1) % 6 == 0:
                        print '\t'.join(['[%d] q%d: (%d,%d)' % (i,queen,move[0],move[1])])
                    else:
                        print '\t'.join(['[%d] q%d: (%d,%d)' % (i, queen, move[0], move[1])]),
                    i += 1
        
        valid_choice = False
        while not valid_choice:
            try:
                index = int(input('Select move index:'))
                valid_choice = 0 <= index < i

                if not valid_choice:
                    print('Illegal move! Try again.')
            
            except ValueError:
                print('Invalid index! Try again.')
        
        return choice[index][1],choice[index][0]

class HumanPlayer2():
    """Player that chooses a move according to
    user's input."""
    def move(self, game, legal_moves, time_left):
        i=0
        choice = {}
        if not len(legal_moves[game.__active_players_queen1__]) and not len(legal_moves[game.__active_players_queen2__]):
            return None, None
        for queen in legal_moves:
                for move in legal_moves[queen].keys():
                    choice.update({i:(queen,move)})
                    # print('\t'.join(['[%d] q%d: (%d,%d)'%(i,queen,move[0],move[1])] ))
                    i=i+1
        
        # find which queens still have valid moves
        valid_queens = []
        if len(legal_moves[game.__active_players_queen1__]):
            valid_queens.append(game.__active_players_queen1__)

        if len(legal_moves[game.__active_players_queen2__]):
            valid_queens.append(game.__active_players_queen2__)

        # pick the queen to move
        valid_queen = False
        while not valid_queen:
            try:
                queen = int(input('Choose queen to move. Choose from ' + str(valid_queens) + ':'))
                valid_queen = queen in valid_queens
            except (NameError, SyntaxError) as e:
                print('Invalid input! Try again.')

        valid_position = False
        while not valid_position:
            try:
                # Choose the position
                position = tuple(int(x.strip()) for x in raw_input('input tuple (y,x) : ').split(','))
                for tup in choice:
                    option = choice[tup]
                    if option[0] is queen and option[1] == position:
                        valid_position = True
                        break

                if not valid_position:
                    print('Illegal move! Try again.')
            
            except ValueError:
                print('Invalid index! Try again.')
        
        return position, queen