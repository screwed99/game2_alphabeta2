from math import inf
from copy import copy, deepcopy
import random
import pickle
import time

class GameState():
    
    def __init__(self, board, player_next, connect_number, number_of_moves, moves_list = []):
        self._board = board
        self._player_next = player_next
        self._connect_number = connect_number
        self._number_of_moves = number_of_moves
        self._moves_list = moves_list
        # self._last_move = last_move
        # self._previous_game_state = previous_game_state

    def _copy(self):
        board = deepcopy(self._board)
        player_next = deepcopy(self._player_next)
        connect_number = deepcopy(self._connect_number)
        number_of_moves = deepcopy(self._number_of_moves)
        moves_list = deepcopy(self._moves_list)
        # previous_game_state = deepcopy(self)
        return GameState(board, player_next, connect_number, number_of_moves, moves_list)
                
    def get_board(self):
        return self._board
    
    def get_player_next(self):
        return self._player_next

    def get_last_move(self):
        return self._moves_list[-1]
    
    def get_connect_number(self):
        return self._connect_number

    def get_number_of_moves(self):
        return self._number_of_moves
    
    def make_move(self, move, player_next = True):
               
        self._board[move[0]][move[1]] = self._player_next
        self._player_next = - self._player_next
        self._moves_list.append(move)
        self._number_of_moves = self._number_of_moves + 1

        # return game_state
        
    def unmake_move(self):
        move = self.get_last_move()
        self._board[move[0]][move[1]] = None
        self._player_next = - self._player_next
        self._number_of_moves = self._number_of_moves - 1
        self._moves_list = self._moves_list[: -1]
        
        # return game_state

    def get_next_moves(self):    
    
        global columns
        global rows
        global column_order
                
        moves = []
        any_moves = False

        for column in range(columns):
            if any_moves:
                break
            for row in range(rows):
                if self._board[row][column_order[column]] == None:
                    moves.append ((row, column_order[column]))
                    break
                
        return moves
   
    def game_end(self):

# This determines whether the game has ended after the last move and whether it is a win, lose
# or draw (if the board is full)

        if self.get_number_of_moves() == 0:
            return False, False        
        player = - self.get_player_next()
        board = self.get_board()
        connect_number = self.get_connect_number()
        last_move = self.get_last_move()

        global rows
        global columns
        
        game_end = False
        win = False
        
        vectors = [(0, 1), (1, 0), (1, 1), (1, -1)]
       
        if last_move == None:
            return game_end, win
                     
        for vector in vectors:
            consec = 1
            next_position = last_move
            while not win:
                next_position = (next_position[0] + vector[0], next_position[1] + vector[1])
                # print('Next position positive : ', next_position)
                if next_position[0] not in range(rows) or next_position[1] not in range(columns):
                    break                                                                                    
                if board[next_position[0]][next_position[1]] == player:
                    consec = consec + 1
                else:
                    break
                if consec == connect_number:
                        win = True
                # print('consec positive : ', consec, 'Vector : ', vector)
                                        
            next_position = last_move
            while not win:
                next_position = (next_position[0] - vector[0], next_position[1] - vector[1])
                # print('Next position negative : ', next_position)
                if next_position[0] not in range(rows) or next_position[1] not in range(columns):
                    break                                                                                    
                if board[next_position[0]][next_position[1]] == player:
                    consec = consec + 1
                else:
                    break
                if consec == connect_number:
                    win = True
                # print('consec negative : ', consec, 'Vector : ', vector)
            
        if win:
            game_end = True
 
        if None not in (item for sublist in self.get_board() for item in sublist):
            game_end = True
        
        return game_end, win

    def valid_move(self, move):
        if move in self.get_next_moves():
            return True
        else:
            return False
      
    def score(self):
        
        score = 0

        global rows
        global columns
              
        player_next = self.get_player_next()
        first_player = 1

# This gets the (occupied) heights of each column
        
        column_heights = []
        column_low_high = []
        
        for column in range(columns):
            for row in range(rows):
                if self._board[row][column] == None:
                    column_heights.append(row)
                    break
                elif row == rows - 1:
                    column_heights.append(rows)

        # print('Column heights : ', column_heights)
        
# This gets the positions that are next to (horozontally, vertically or diagonally) from an
# occupied position. It outputs the columm, lowest row and highest row.
    
        for column in range(columns):
            if columns == 1:
                max_height = column_heights[0]
                break
            if column_heights[column] != rows:
                if column == 0:
                    max_height = max(column_heights[column], column_heights[column + 1])
                elif column == columns - 1:
                    max_height = max(column_heights[column], column_heights[column - 1])
                else:
                    max_height = max(column_heights[column - 1], column_heights[column], column_heights[column + 1])
    
                if max_height != 0:
                    if max_height == rows:
                        max_row = max_height - 1
                    else:
                        max_row = max_height    
                    column_low_high.append((column, column_heights[column], max_row))
    
        # self.print_board()             
        # print('Column low high : ', column_low_high)

# This identfies all the threats (i.e. positions that would result in a win if occupied by a
# player.) It returns the position and player for whom the threat exists and whether it is
# 'good' threat or not.
        
        threat_positions = []
        immediate_threats_not_player_next = 0

        for column, low, high in (column_low_high):
            column_threats = [] 
            for row in range(low, high + 1):
                # threat_position = (row, column)
                # print('Position to check for threats : ', row, column)
                # column_threats = self.get_threats((row, column))
                for threat in self.get_threats((row, column)):
                    column_threats.append(threat)
                    
        # self.print_board()
        #     print('Column Threats : ', column, column_threats)

        # first_player = 1
        # print('Even board : ', board_even)
        # self.print_board()
        # threat_number = 0
            previous_good_threat = False
            previous_threat_row_player_next = -1 
            previous_threat_row_not_player_next = -1
        #   last_threat = 0
        
            for threat_position in column_threats:

                # threat_column = threat_position[0][1]
                good_threat = threat_position[2]
                threat_row = threat_position[0][0]
                threat_player = threat_position[1]
                # print('Threat position : ', threat_position)
                if threat_row == column_heights[column]:
                    if threat_player == player_next:
                        # print('Immediate win next move')
                        return 99999
                    else:
                        immediate_threats_not_player_next = immediate_threats_not_player_next + 1
                        previous_threat_row_not_player_next = threat_row
                        if immediate_threats_not_player_next < 2:
                            score = score - 10
                            
                # print('Threat position : ', threat_position)
                else:
                    if threat_player == player_next:
                        if threat_row == previous_threat_row_player_next + 1:
                            if previous_threat_row_not_player_next >= 0:
                                score = score + 200
                            else:
                                score = score + 1000
                        elif threat_row == previous_threat_row_not_player_next + 1:
                            score = score + 5
                            previous_threat_row_player_next = threat_row
                            break
                        previous_threat_row_player_next = threat_row
                        
                    else:
                        if threat_row == previous_threat_row_not_player_next + 1:
                            if previous_threat_row_player_next >= 0:
                                score = score - 200
                            else:
                                score = score -1000
                        elif threat_row == previous_threat_row_player_next + 1:
                            score = score - 5
                            previous_threat_row_not_player_next = threat_row
                            break
                        previous_threat_row_not_player_next = threat_row
                                                 
                    if good_threat:
                        if not previous_good_threat:
                            previous_good_threat = True
                            if threat_player == player_next:
                                score = score + 100
                            else:
                                score = score - 100
                        else:
                            score = score + 20
                    else:
                        if not previous_good_threat:
                            if threat_player == player_next:
                                score = score + 20
                            else:
                                score = score - 20

                       # print('Score : ', score)
                            
            # print('Threat position : ', threat_position)
            # print('Threat row : ', threat_row)
                                
        global score_count
        score_count = score_count + 1
        
        if immediate_threats_not_player_next >= 2:
          # print('Immediate win in two moves')
            return -99999
                        
        # global score_find
        # if score == score_find:
        #    self.print_board()
        
        return score

    def get_threats(self, position):

# This determinse whether a position is a threat (i.e. potentially winning move) for either
# or both players
        
        threats_player = []
        board = self.get_board()
        connect_number = self.get_connect_number()
        
        global rows
        global columns
       
        vectors = [(0, 1), (1, 0), (1, 1), (1, -1)]
        players = (1, -1)

        for player in players:
            threat = False
            for vector in vectors:
                consec = 1
                next_position = position
                # threat = False
                while not threat:
                    next_position = (next_position[0] + vector[0], next_position[1] + vector[1])
                    if next_position[0] not in range(rows) or next_position[1] not in range(columns):
                        break                                                                                    
                    if board[next_position[0]][next_position[1]] == player:
                        consec = consec + 1
                    else:
                        break
                    if consec == connect_number:
                            threat = True
                            good_threat = self.check_threat(position, player)
                            threats_player.append((position, player, good_threat))
                                                     
                next_position = position
                while not threat:
                    next_position = (next_position[0] - vector[0], next_position[1] - vector[1])
                    if next_position[0] not in range(rows) or next_position[1] not in range(columns):
                        break                                                                                    
                    if board[next_position[0]][next_position[1]] == player:
                        consec = consec + 1
                    else:
                        break
                    if consec == connect_number:
                        threat = True
                        good_threat = self.check_threat(position, player)
                        threats_player.append((position, player, good_threat))
                if threat:
                    break
                
        # self.print_board()
        # print('Position for threats: ', position)
        # print('Player threats : ', threats_player)

        return threats_player
    
    def get_threats_new(self, position):

# This determinse whether a position is a threat (i.e. potentially winning move) for either
# or both players
        
        threats_player = []
        player_next = self.get_player_next()
        
        new_game_state = self.make_move(position)
        game_end_win = new_game_state.game_end()
        if game_end_win[0] and game_end_win[1]:
            good_threat = self.check_threat(position, player_next)
            threats_player.append((position, player_next, good_threat))
         
        new_game_state = self.make_move(position, player_next = False)
        game_end_win = new_game_state.game_end()
        if game_end_win[0] and game_end_win[1]:
            good_threat = self.check_threat(position, -player_next)
            threats_player.append((position, -player_next, good_threat))

        return threats_player

    def check_threat(self, position, threat_player):

# This determines whether a threat is 'good threat' or not depending on the threat position,
# the player and if the board is odd or even.

        global rows
        global columns
        global board_even
                  
        first_player = 1
        threat_row = position[0]
        good_threat = False
                             
        if board_even:
            if not threat_row % 2:
                if threat_player == first_player:
                    good_threat = True
            else:
                if threat_player != first_player:
                    good_threat = True
        else:
            if threat_row % 2:
                if threat_player == first_player:
                    good_threat = True
            else:
                if threat_player != first_player:
                    good_threat = True
                    
        return good_threat
                                         
    def print_board(self):

        global rows
        global columns
              
        for row in range(rows):
            print_row = []
            for column in range(columns):
                if self._board[rows - row - 1][column] == 1:
                    print_row.append('W')
                elif self._board[rows - row - 1][column] == -1:
                    print_row.append('B')
                else:
                    print_row.append(' ')
            print(print_row)
            
        if self._player_next == 1:
            print('Player is White Connect Number : ', self._connect_number, ' Number of moves : ', self._number_of_moves)
        else:
            print('Player is Black Connect Number : ', self._connect_number, ' Number of moves : ', self._number_of_moves)

def sort_moves(game_state, moves):

    moves_and_scores = []
                             
    for move in moves:
        
        game_state.make_move(move)
        game_end_win = game_state.game_end()
        if game_end_win[0]:
            if game_end_win[1]:
                moves_and_scores.append([move, -inf])
            else:
                moves_and_scores.append([move, 0])
        else:
            # moves_and_scores.append([move, new_game_state.score()])
            moves_and_scores.append([move, game_state.score()])
            
        game_state.unmake_move()          
        # moves_and_scores.append([move, new_game_state.score()])
           
        # print ('Moves and scores before sort : ', moves_and_scores)
    moves_and_scores.sort(key = lambda x: x[1])
    # print ('Moves and scores after sort : ', moves_and_scores)
    sorted_moves = [move_and_score[0] for move_and_score in moves_and_scores]
    # print('Moves and scores are : ', moves_and_scores)

    return sorted_moves

          
def minimax(game_state, look_forward,  player_next_first, alpha, beta, sort_depth):

    global start_look_forward
    global score_find
    global score_found
    global worse_score_found
       
    # print('look forward = ', look_forward)
    move_and_score = ((-1, -1), 0)
    game_end_win = game_state.game_end()
    if look_forward == 0 or game_end_win[0]:
        if game_end_win[0]:
            if game_end_win[1]:
                move_score = -inf
            else:
                move_score = 0
        else:
            move_score = game_state.score()
            # game_state.print_board()
            # print('Board score : ', move_score) 
        if game_state.get_player_next() != player_next_first: 
            move_score = - move_score

        # if  move_score == score_find and not score_found:
            # print('Score : ', move_and_score[1], 'Score Find : ', score_find, 'Score found : ', score_found)
        #     score_found = True
        #     game_state.print_board()
            
        # if  move_score > score_find and not worse_score_found:
        #     worse_score_found = True
        #     print('Worse score found')
               
        ## print('move score = ', move_score, 'Game End : ', game_state.game_end())
        return (-1, -1), move_score
    
    moves = game_state.get_next_moves()

    # if sort_depth > 0 and (game_state.get_number_of_moves() > 10 or look_forward < start_look_forward):
    if sort_depth > 0:
        moves = sort_moves(game_state, moves) 
          
    best_move = (-1, -1)
    if game_state.get_player_next() == player_next_first: 
        
        for move in moves:

            # if look_forward == start_look_forward:
            #     print('First Move : ', move)
            #     score_found = False
            #     worse_score_found = False
                           
            # print ('max board prior to move')
            # game_state.print_board()
           
            game_state.make_move(move)
            # print ('max board after move')
            # game_state.print_board()
            move_and_score = minimax(game_state, look_forward - 1, player_next_first, alpha, beta, sort_depth - 1)
            # print ('Max score : ', move_and_score[1], 'alpha = ', alpha)
            
            game_state.unmake_move()
            
            if move_and_score[1] > alpha:
                alpha = move_and_score[1]
                best_move = move
                # print('Best move max : ', move)
            # print('max alpha = ', alpha, 'max beta = ', beta)
            if beta <= alpha:
                # print ('Break max')
                break
                    
        return best_move, alpha

    else:
        
        for move in moves:
            
            # print ('min board prior to move')
            # game_state.print_board()
           
            game_state.make_move(move)
            # print ('min board after move')
            # game_state.print_board()
            move_and_score = minimax(game_state, look_forward - 1, player_next_first, alpha, beta, sort_depth - 1)  
            # print ('Min score : ', move_and_score[1], 'beta = ', beta)
            
            game_state.unmake_move()
            
            if move_and_score[1] < beta:
                beta = move_and_score[1]
                best_move = move
                # print('Best move min : ', move)
            # print('min alpha = ', alpha, 'min beta = ', beta)
            if beta <= alpha:
                # print ('Break min')
                break
                    
        return best_move, beta
    
def get_computer_move(game_state):

    global score_count
    global total_score_count
    global cyborg
    global cyborg_look_forward
    global cyborg_sort_depth
    global start_look_forward
    
    score_count = 0
    start_time = time.time()
    
    player_next_first = game_state.get_player_next()

    if cyborg:
        look_forward = cyborg_look_forward
        sort_depth = cyborg_sort_depth
    else:
        look_forward = get_look_forward()
        sort_depth = get_sort_depth()
        
    start_look_forward = look_forward
    best_move_and_score = minimax(game_state, look_forward, player_next_first, -inf, inf, sort_depth)
    next_move_and_score = best_move_and_score
    best_score = best_move_and_score[1]

    print('Best move and score : ', best_move_and_score)

# If there is a forced win or loss this finds the optimum move. In the case of forced win it
# will return a move that will win in the smallest number of moves. If a forced loss it will
# play a move that makes the opponent play an optimum move to win in the least possible
# number of moves.
    
    if best_score == inf:
        if not look_forward % 2:
            look_forward = look_forward - 1
        while best_score == inf:
            look_forward = look_forward - 2
            # print('Win look forward : ', look_forward)
            best_move_and_score =  next_move_and_score
            if look_forward <= 0:
                break
            next_move_and_score = minimax(game_state, look_forward, player_next_first, -inf, inf, 0)
            # best_move_and_score =  next_move_and_score
            best_score = next_move_and_score[1]
                    
        print('Forced win after ', look_forward + 2, ' moves')
        
    elif best_score == -inf:
        
        best_move_and_score = (game_state.get_next_moves()[0], -inf)
        if look_forward % 2:
            look_forward = look_forward - 1
        
        while best_score == -inf:
            look_forward = look_forward - 2
            # print('Lose look forward : ', look_forward)
            
            if look_forward <= 0:
                break
            next_move_and_score = minimax(game_state, look_forward, player_next_first, -inf, inf, 0)
            # best_move_and_score =  next_move_and_score
            best_score = next_move_and_score[1]
            # print('Best lose score : ', best_score)

        if best_score == -inf:
            best_move_and_score = (game_state.get_next_moves()[0], -inf)
        else:
            best_move_and_score =  next_move_and_score
        
        print('Forced loss after ', look_forward + 2, ' moves')
        # best_move_and_score = (game_state.get_next_moves()[0], -inf)
        
    print('Time for move : ', round(time.time()- start_time, 1), ' seconds', 'Score count : ', score_count)
    total_score_count = total_score_count + score_count
      
    return best_move_and_score

def choose_board_size():
    not_valid = True
    while not_valid:
        try:
            rows = int(input("Enter number of rows : "))
            if rows > 0:
                not_valid = False
            else:
                print('Invalid input. Try again')  
        except:
            print('Invalid input. Try again')
    not_valid = True
    while not_valid:
        try:
            columns = int(input("Enter number of columns : "))
            if columns > 0:
                not_valid = False
            else:
                print('Invalid input. Try again')  
        except:
            print('Invalid input. Try again')
        
    return (rows, columns)

def create_board(board_size):
    board = [[None] * int(board_size[1]) for _ in range(int(board_size[0]))]
    return board

def get_look_forward():
    while True:
        try:
            look_forward = int(input("Enter look forward : "))
            if look_forward >= 0:
                return look_forward
            else:
                print('Look ahead cannot be negative: Try again')  
        except:
            print('Invalid input. Try again')         

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
    while True:
        try:
            sort_depth = int(input("Enter number of levels to sort moves : "))
            return sort_depth
        except:
            print('Invalid input. Try again')
          
def human_to_play():
        
    human = input("Human to play? (Y/N) : ")
    if human == 'Y' or human == 'y':
        return True
    else:
        return False

def get_human_move(game_state):

    global rows
    global columns
       
    board = game_state.get_board()
    
    while True:
        try:
            column = int(input("Enter column : ")) - 1
            if column < 0 or column >= columns:
                print('Column outside range. Try again')
            else:
                for row in range(rows):
                    if board[row][column] == None:
                        return row, column
                print('Column full. Try again')                                
        except:
            print('Invalid input. Try again')
                             
def get_hint():
    
    hint = input("Get hint? (Y/N) : ")
    if hint == 'Y' or hint == 'y':
        return True
    else:
        return False

def get_connect_number():
    
    while True:
        try:
            connect_number = int(input("Enter connect number : "))
            if connect_number <= 0:
                print('Connect number must be  positive: Try again')
            else:
                return connect_number
        except:
            print('Invalid input. Try again')

def save_game(game_state):
    
    save = input("Save Game:? (Y/N) : ")
    while save == 'Y' or save == 'y':
        filename = input('Enter file name to save to : ')
        try:
            with open(filename, 'wb') as f:
                pickle.dump(game_state, f)
                break
        except Exception as ex:
            print('Error during saving game : ', ex)
            save = input("Try again:? (Y/N) : ")
         
def restore_game():
    
    restore = input("Restore Game:? (Y/N) : ")
    while restore == 'Y' or restore == 'y':
        filename = input('Enter file name to restore : ')
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except Exception as ex:
            print('Error during restoring game : ', ex)
            restore = input("Try again:? (Y/N) : ")

def get_cyborg():
    
    cyborg = input("Cyborg? (Y/N) : ")
    if cyborg == 'Y' or cyborg == 'y':
        return True
    else:
        return False

def get_score_find():
    
    global score_find
   
    while True:
        try:
            score_find = int(input("Enter score to find : "))
            return score_find
        except:
            print('Invalid input. Try again')          
def main():
    
    game_state = restore_game()
    if game_state == None:
        board = []
        board_size = choose_board_size()
        board = create_board(board_size)
        connect_number = get_connect_number()
        player_next = 1
        number_of_moves = 0
        game_state = GameState(board, player_next, connect_number, number_of_moves)

    game_start_time = time.time()
    global cyborg
    global cyborg_look_forward
    global cyborg_sort_depth
    
    global rows
    global columns
    board = game_state.get_board()
    rows = len(board)
    columns = len(board[0])

    global column_order
    column_order = [None]*columns
    iterate = 1
    column_order[0] = int((columns - 1)/2)
    for i in range(1, columns):
        column_order[i] = column_order[i-1] + iterate
        if iterate > 0:
            iterate = -1-iterate
        else:
            iterate = 1-iterate

    # column_order = [1, 0, 2, 3, 4, 5, 6]
    
    global board_even
    board_count = rows * columns
    if board_count % 2:
        board_even = False
    else:
        board_even = True
   
    cyborg = False
        
    global score_count
    global score_find
    global total_score_count
    total_score_count = 0
    game_state.print_board()
   
    another_move = True
    while another_move:
        if not cyborg:
            cyborg = get_cyborg()
            if cyborg:
                cyborg_look_forward = get_look_forward()
                cyborg_sort_depth = get_sort_depth()
                score_find = 9876
        if cyborg:
            best_move_and_score = get_computer_move(game_state)
            # print ('best move and score: ', best_move_and_score, 'Score count : ', score_count)
            best_move = best_move_and_score[0]
            game_state.make_move(best_move)
        else:    
            if  human_to_play():
                while get_hint():
                    # score_find = 9876
                    # score_find = get_score_find()
                    best_move_and_score = get_computer_move(game_state)
                    best_move = best_move_and_score[0]
                    # print('Suggested move row : ', best_move[0] + 1, 'column : ', best_move[1] + 1)
                    print('Suggested move column : ', best_move[1] + 1)
            
                move = get_human_move(game_state)
                # game_state = game_state.make_move(move)
                game_state.make_move(move)
            else:
                # score_find = 9876
                # score_find = get_score_find()
            
                best_move_and_score = get_computer_move(game_state)
                # print ('best move and score: ', best_move_and_score, 'Score count : ', score_count)
                best_move = best_move_and_score[0]
                # game_state = game_state.make_move(best_move)
                game_state.make_move(best_move)
                 
        game_state.print_board()
        
        if not cyborg:
            while undo_move():
                game_state.unmake_move()
                game_state.print_board()
                #if game_state.get_last_move() == None:
                if game_state.get_number_of_moves() == 0:
                    break
                
        game_end_win = game_state.game_end()
        
        if game_end_win[0]:
            print('End of Game')
            if game_end_win[1]:
                if game_state.get_player_next() == 1:
                    print('Winner is Black')
                else:
                    print('Winner is White')
            else: 
                print('Game is Drawn')
            print('Time for game : ', round(time.time()- game_start_time, 1), ' seconds')
            print('Total score count : ', total_score_count)
            break

        if not cyborg:
            save_game(game_state)
            another_move = move_more()

     
if __name__ == '__main__':
    main()
