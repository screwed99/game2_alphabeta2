from math import inf
from copy import copy, deepcopy
import random

class GameState():
    def __init__(self, board, player_next, previous_game_state = None):
        self._board = board
        self._player_next = player_next
        self._previous_game_state = previous_game_state

    def _copy(self):
        board = deepcopy(self._board)
        player_next = self._player_next
        previous_game_state = deepcopy(self)
        return GameState(board, player_next, previous_game_state)

                
    def get_board(self):
        return self._board
    
    def get_player_next(self):
        return self._player_next

    def make_move(self, move):
        new_game_state = self._copy()
        new_game_state._board[move[0]][move[1]] = new_game_state._player_next
        new_game_state._player_next = - new_game_state._player_next
        return new_game_state
        
    def unmake_move(self):
        new_game_state = self._previous_game_state
        return new_game_state
        
    def get_next_moves(self, moves_sort = False, game_end = False):
        moves = []
        any_moves = False
        for i in range(len(self._board)):
            if any_moves:
                break
            for j in range(len(self._board[i])):
                if self._board[i][j] == None:
        #            moves.append ((i, j))
                    moves.insert(0, (i, j))
                    if game_end:
                        any_moves = True
                        break
                    
        random.shuffle(moves)
        
        if moves_sort:
            moves_and_scores = []
            i = 0
            for move in moves:
                new_game_state = self.make_move(move)
                moves_and_scores.append([move])
                moves_and_scores[i].append(new_game_state.score())
                i = i + 1
            print ('Moves and scores before sort : ', moves_and_scores)
            moves_and_scores.sort(key = lambda x: x[1])
            print ('Moves and scores after sort : ', moves_and_scores)
            moves = []
            for move_and_score in moves_and_scores:
                moves.append(move_and_score[0])
                
        # print('moves are ', moves)
        return moves

    


    def game_end(self):
        if self.get_next_moves(game_end = True) == []:
            return True
        else:
            return False

    def valid_move(self, move):
        if move in self.get_next_moves():
            return True
        else:
            return False
   
        
    def score(self):
        score = 0
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] == self._player_next:
                    score = score + (i + 1)*(j + 1)
                else:
                    if self._board[i][j] == - self._player_next:
                        score = score - (i + 1)*(j + 1)

        global score_count
        score_count = score_count + 1

        ## print('score = ', score)
        return score

def minimax(game_state, look_forward,  player_next_first, alpha, beta, sort_depth):
 
    # print('look forward = ', look_forward)
    move_and_score = ((-1, -1), 0)
    
    if look_forward == 0 or game_state.game_end():
        move_score = game_state.score()
        if game_state.get_player_next() != player_next_first: 
            move_score = - move_score
               
        ## print('move score = ', move_score, 'Game End : ', game_state.game_end())
        return (-1, -1), move_score

    if sort_depth <= look_forward:
        sort = True
    else:
        sort = False
        
    
    best_move = (-1, -1)
    if game_state.get_player_next() == player_next_first: 
        for move in game_state.get_next_moves(moves_sort = sort):
            ## print ('max board prior to move  ', game_state.get_board())
            new_game_state = game_state.make_move(move)
            # print ('max board after move  ', new_game_state.get_board())
            move_and_score = minimax(new_game_state, look_forward - 1, player_next_first, alpha, beta, sort_depth)
            # print ('Max score : ', move_and_score[1], 'alpha = ', alpha)            
            if move_and_score[1] > alpha:
                alpha = move_and_score[1]
                best_move = move
                # print('Best move max : ', move)
            # print('max alpha = ', alpha, 'max beta = ', beta)
            if beta <= alpha:
                print ('Break max')
                break
            
        return best_move, alpha

    else:
        for move in game_state.get_next_moves(moves_sort = sort):
            ## print ('min board prior to move  ', game_state.get_board())
            new_game_state = game_state.make_move(move)
            # print ('min board after move  ', new_game_state.get_board())
            move_and_score = minimax(new_game_state, look_forward - 1, player_next_first, alpha, beta, sort_depth)  
            # print ('Min score : ', move_and_score[1], 'beta = ', beta)            
            if move_and_score[1] < beta:
                beta = move_and_score[1]
                best_move = move
                # print('Best move min : ', move)
            print('min alpha = ', alpha, 'min beta = ', beta)
            if beta <= alpha:
                print ('Break min')
                break
            
        return best_move, beta
    
def get_computer_move(game_state):
    player_next_first = game_state.get_player_next()
    look_forward = choose_look_ahead()
    sort_depth = get_sort_depth()
    score_count = 0
    best_move_and_score = minimax(game_state, look_forward, player_next_first, -inf, inf, sort_depth)
    return best_move_and_score


def choose_board_size():
    rows = int(input("Enter number of rows : "))
    columns = int(input("Enter number of columns : "))
    return (rows, columns)

def create_board(board_size):
    board = [[None] * int(board_size[1]) for _ in range(int(board_size[0]))]
    return board

def choose_look_ahead():
    look_ahead = int(input("Enter look ahead : "))
    return look_ahead

def move_more():
    more_moves = input("Another Move? (Y/N) : ")
    if more_moves == 'Y' or more_moves == 'y':
        return True
    else:
        return False

def undo_move():
    undo_last_move = input("Undo last move? (Y/N) : ")
    if undo_last_move == 'Y' or undo_last_move == 'y':
        return True
    else:
        return False

def get_sort_depth():
    sort_depth = int(input("Enter sort depth : "))
    return sort_depth

def human_to_play():
    human = input("Human to play? (Y/N) : ")
    if human == 'Y' or human == 'y':
        return True
    else:
        return False

def get_human_move(game_state):
    valid = False
    while not valid:
        row = int(input("Enter row : ")) - 1
        column = int(input("Enter column : ")) - 1
        if  game_state.valid_move((row, column)):
            valid = True
        else:
            print('Invalid move. Try again')
            valid = False
    return row, column

def get_hint():
    hint = input("Get hint? (Y/N) : ")
    if hint == 'Y' or hint == 'y':
        return True
    else:
        return False


def main():
    board = []
    board_size = choose_board_size()
    print('board size : ', board_size)
    board = create_board(board_size)
    print('board : ', board)
    
    player_next = 1
    number_of_moves = 0
    
    global score_count
    
    game_state = GameState(board, player_next)
   
    another_move = True

    while another_move:

        if  human_to_play():
            while get_hint():
                score_count = 0
                best_move_and_score = get_computer_move(game_state)
                best_move = best_move_and_score[0]
                print('Suggested move row : ', best_move[0] + 1, 'column : ', best_move[1] + 1)
            
            move = get_human_move(game_state)
            
            game_state = game_state.make_move(move)
            number_of_moves = number_of_moves + 1 
            print('board = ', game_state.get_board(), 'next player = ', game_state.get_player_next())

        else:
        
            # player_next_first = game_state.get_player_next()
            # look_forward = choose_look_ahead()
            # sort_depth = get_sort_depth()
            score_count = 0
            # best_move_and_score = minimax(game_state, look_forward, player_next_first, -inf, inf, sort_depth)
            best_move_and_score = get_computer_move(game_state)
            print ('best move and score: ', best_move_and_score, 'Score count : ', score_count)
            # print('board = ', game_state.get_board(), 'next player = ', game_state.get_player_next())
            best_move = best_move_and_score[0]
            game_state = game_state.make_move(best_move)
            number_of_moves = number_of_moves + 1 
            print('board = ', game_state.get_board(), 'next player = ', game_state.get_player_next())
        
        while undo_move():
            game_state = game_state.unmake_move()
            number_of_moves = number_of_moves - 1
            print('board = ', game_state.get_board(), 'next player = ', game_state.get_player_next())
            if number_of_moves == 0:
                break
            
        # print ('Game end : ', game_state.game_end())
        if game_state.game_end():
            print('End of Game')
            score_count = 0
            end_score = game_state.score()
            if game_state.get_player_next() == 1:
                if end_score > 0:
                    print('Winner is Player 1 with net score of', end_score)
                elif end_score < 0:
                    print('Winner is Player 2 with net score of', -end_score)
                else:
                    print('Game is a draw')
            else:
                if end_score > 0:
                    print('Winner is Player 2 with net score of', end_score)
                elif end_score < 0:
                    print('Winner is Player 1 with net score of', -end_score)
                else:
                    print('Game is a draw')
            break   

        another_move = move_more()
   
    

if __name__ == '__main__':
    main()
