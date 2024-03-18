#Zijie Zhang, Sep.24/2023

import numpy as np
import socket, pickle
from reversi import reversi
from copy import deepcopy


def minmax(game, depth, alpha, beta, is_max_player):
    if depth == 0 or game.is_game_end():
        return game.score_game()
    
    # MAX TURN
    if is_max_player:
        max_score = float('-inf')
        valid_moves = game.get_all_valid_moves(-game.turn)
        for row, col in valid_moves:
            if game.board[row, col] == 0:

                new_game = reversi()
                new_game.turn = game.turn
                new_game.board = game.board
                new_game.put_stones(row, col, -game.turn)

                opponent_moves = new_game.get_all_valid_moves(game.turn)
                score = minmax(new_game, depth - 1, alpha, beta, opponent_moves == set())
                max_score = max(max_score, score)

                alpha = max(alpha, score)
                if beta <= alpha:
                    break

        return max_score

    # MIN TURN
    min_score = float('+inf')
    valid_moves = game.get_all_valid_moves(game.turn)
    for row, col in valid_moves:
        if game.board[row, col] == 0:

            new_game = reversi()
            new_game.turn = game.turn
            new_game.board = game.board
            new_game.put_stones(row, col, game.turn)

            opponent_moves = new_game.get_all_valid_moves(-game.turn)
            score = minmax(new_game, depth - 1, alpha, beta, opponent_moves != set())
            min_score = min(min_score, score)

            beta = min(beta, score)
            if beta <= alpha:
                break

    return min_score


def best_minmax_coordinators(game, turn):
    best_move = (-1, -1)
    max_score = float("-inf")
    MAX_DEPTH = 4
    
    valid_moves = game.get_all_valid_moves(turn)
    
    for row, col in valid_moves:
        if game.board[row, col] == 0:
            new_game = reversi()
            new_game.turn = game.turn
            new_game.board = game.board
            new_game.put_stones(row, col, turn)
            
            oppo_moves = new_game.get_all_valid_moves(-turn)
            current_score = minmax(new_game, MAX_DEPTH, float("-inf"), float("inf"), oppo_moves != set())
            
            if current_score > max_score:
                best_move = (row, col)
                max_score = current_score
            
    return best_move


def main():
    game_socket = socket.socket()
    game_socket.connect(('127.0.0.1', 33333))
    game = reversi()

    while True:

        #Receive play request from the server
        #turn : 1 --> you are playing as white | -1 --> you are playing as black
        #board : 8*8 numpy array
        data = game_socket.recv(4096)
        turn, board = pickle.loads(data)

        #Turn = 0 indicates game ended
        if turn == 0:
            game_socket.close()
            return
        
        #Debug info
        # print(turn)
        # print(board)
        
        
        # My minmax algorithm
        game.board = board
        x, y = best_minmax_coordinators(game, turn)
        
        #Send your move to the server. Send (x,y) = (-1,-1) to tell the server you have no hand to play
        game_socket.send(pickle.dumps([x,y]))
        
if __name__ == '__main__':
    main()