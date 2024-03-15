#Zijie Zhang, Sep.24/2023

import numpy as np

class reversi:
    def __init__(self) -> None:
        self.board = np.zeros([8,8])

        self.board[3,4] = -1
        self.board[3,3] = 1
        self.board[4,3] = -1
        self.board[4,4] = 1
        self.white_count = 2
        self.black_count = 2
        self.directions = [
            [1,1],
            [1,0],
            [1,-1],
            [0,1],
            [0,-1],
            [-1,1],
            [-1,0],
            [-1,-1]
        ]

        self.time = 0
        self.turn = 1

    def step(self, x, y, piece = 1, commit = True) -> int:

        #Piece already exists
        if self.board[x,y] != 0:
            return -1
        
        #Out of bound
        elif x < 0 or x > 7 or y < 0 or y > 7:
            return -2
        
        else:
            fliped = 0
            for direction in self.directions:
                dx, dy = direction
                cursor_x, cursor_y = x + dx, y + dy
                flip_list = []
                while 0 <= cursor_x <=7 and 0 <= cursor_y <=7:
                    if self.board[cursor_x, cursor_y] == 0:
                        break
                    elif self.board[cursor_x, cursor_y] == piece:
                        if len(flip_list) == 0:
                            break
                        else:
                            for cord in flip_list:
                                if commit:
                                    self.board[*cord] = piece
                                fliped += 1
                            break
                    else:
                        flip_list.append([cursor_x, cursor_y])
                        cursor_x, cursor_y = cursor_x + dx, cursor_y + dy

            #Illegal Move
            if fliped == 0:
                return -3
            else:
                if commit:
                    self.board[x,y] = piece
                    if piece == 1:
                        self.white_count += 1
                    else:
                        self.black_count += 1
                    self.white_count += fliped * piece
                    self.black_count -= fliped * piece
                return fliped
            
            
            
    def score_game(self):
        # coin parity
        coin_parity = 100 * (self.black_count - self.white_count) / (self.black_count + self.white_count)
        
        # Mobility
        black_mobility = len(self.get_all_valid_moves(-self.turn))
        white_mobility = len(self.get_all_valid_moves(self.turn))
        
        if black_mobility + white_mobility == 0:
            actual_mobility = 0
        else:
            actual_mobility = 100 * (black_mobility - white_mobility) / (black_mobility + white_mobility)

        # corner capture
        corners = (self.board[0, 0], self.board[0,7], self.board[7, 0], self.board[7, 7])
        black_corners = sum(100 for corner in corners if corner == -self.turn)
        white_corners = sum(-100 for corner in corners if corner == self.turn)
        
        if black_corners + white_corners == 0:
            corner_value = 0
        else:
            corner_value = 100 * (black_corners - white_corners) / (black_corners + white_corners)

        return coin_parity + actual_mobility + corner_value
        
    
    
    @staticmethod
    def isCoordValid(x, y):
        return (x >= 0 and y >= 0) and (x < 8 and y < 8)         
    
    
    
    def is_game_end(self):
        check_black_moves = self.get_all_valid_moves(-self.turn)
        check_white_moves = self.get_all_valid_moves(self.turn)
        
        if check_black_moves or check_white_moves:
            return False

        return True
    
    
    
    def get_moves(self, row, col):
        my_turn = self.board[row, col]
        opponent_turn = my_turn * -1
        
        all_valid_moves = []

        for d_row, d_col in self.directions:
            rr = row + d_row
            cc = col + d_col
            
            if reversi.isCoordValid(rr, cc) is False or self.board[rr, cc] != opponent_turn:
                continue
            
            rr += d_row
            cc += d_col
            
            while (reversi.isCoordValid(rr, cc) is True and self.board[rr, cc] == opponent_turn):
                rr += d_row
                cc += d_col
                
            if (reversi.isCoordValid(rr, cc) is True and self.board[rr, cc] == 0):
                all_valid_moves.append((rr, cc))
                
        return all_valid_moves
    
    
    
    def get_all_valid_moves(self, turn):
        valid_moves = set()
        
        for row in range(8):
            for col in range(8):
                if self.board[row, col] == turn:
                    valid_moves.update(self.get_moves(row, col))
                    
        return valid_moves
    
    
    
    def flip_stones(self, turn, start_coord, end_coord, direction):
        opponent_color = turn * -1
        row_dir, col_dir = direction

        start_row, start_col = start_coord
        start_row += row_dir
        start_col += col_dir 

        end_row, end_col = end_coord

        while (self.board[start_col, end_col] == opponent_color) and (start_row != end_row or start_col != end_col):
            self.board[start_col, end_col] = turn
            start_row += row_dir
            start_col += col_dir

    
    
    def put_stones(self, row, col, turn):
        self.board[row, col] = turn
        opponent_color = turn * -1
        
        for d_row, d_col in self.directions:
            rr = row + d_row
            cc = col + d_col
     
            if reversi.isCoordValid(rr, cc) is False or self.board[rr, cc] != opponent_color:
                continue
            
            rr += d_row
            cc += d_col
            
            while (reversi.isCoordValid(rr, cc) is True and self.board[rr, cc] == opponent_color):
                rr += d_row
                cc += d_col
                
            if (reversi.isCoordValid(rr, cc) is True and self.board[rr, cc] == turn):
                self.flip_stones(turn, (row, col), (rr, cc), (d_row, d_col)) 
                
        # update stone counts
        self.black_count = -self.board[self.board < 0].sum()
        self.white_count = self.board[self.board > 0].sum()