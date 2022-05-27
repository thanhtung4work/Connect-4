
import sys
import pygame
import math

ROWS = 6
COLUMNS = 9

SQUARE_UNIT = 80 #px
SCREEN_W = SQUARE_UNIT * COLUMNS
SCREEN_H = (SQUARE_UNIT) * (ROWS + 1)
SCREEN_SIZE = (SCREEN_W, SCREEN_H)
RADIUS = int(SQUARE_UNIT/ 2 - 5)

BLUE = (0, 180, 255)
RED = (255, 60, 0)
YELLOW = (255, 255, 120)
BLACK = (10, 10, 10)

def create_board():
  board = []
  for i in range(ROWS):
    row = []
    for j in range(COLUMNS):
      row.append("?")
    board.append(row)
  return board

def drop_ball(board, row, col, ball_color):
  board[row][col] = ball_color

def is_valid_location(board, col):
  return board[0][col] == "?"

def get_next_open_row(board, col):
  r = ROWS - 1
  while r >= 0:
    if board[r][col] == "?":
      return r
    r -= 1

def winning_move(board, ball_color):
  # check all the horizontal combination
  for c in range(COLUMNS - 3):
    for r in range(ROWS):
      if  (
            board[r][c] == ball_color and 
            board[r][c + 1] == ball_color and 
            board[r][c + 2] == ball_color and 
            board[r][c + 3] == ball_color
          ):
        return True
  
  # check all the vertical combination
  for r in range(ROWS - 3):
    for c in range(COLUMNS):
      if  (
            board[r][c] == ball_color and 
            board[r + 1][c] == ball_color and 
            board[r + 2][c] == ball_color and 
            board[r + 3][c] == ball_color
          ):
        return True
  
  # check all the diagonal combination (top -> down, left -> right) \\\\
  for r in range(ROWS - 3):
      for c in range(COLUMNS - 3):
        if  (
              board[r][c] == ball_color and 
              board[r + 1][c + 1] == ball_color and 
              board[r + 2][c + 2] == ball_color and 
              board[r + 3][c + 3] == ball_color
            ):
          return True
  
  # check all the diagonal combination (down -> top, left -> right) ////
  for r in range(ROWS - 3, ROWS):
      for c in range(COLUMNS - 3):
        if  (
              board[r][c] == ball_color and 
              board[r - 1][c + 1] == ball_color and 
              board[r - 2][c + 2] == ball_color and 
              board[r - 3][c + 3] == ball_color
            ):
          return True

def draw_board(board):
  for row in board:
    print(row)

def view_board_to_screen(screen, board):
  for c in range (COLUMNS):
    for r in range(ROWS):
      rect = (c*SQUARE_UNIT, r*SQUARE_UNIT + SQUARE_UNIT, SQUARE_UNIT, SQUARE_UNIT)
      pygame.draw.rect(screen, BLUE, rect)
      # circle has to be in the middle of the rect
      circle_pos = (int(c*SQUARE_UNIT + SQUARE_UNIT / 2), int(r*SQUARE_UNIT + SQUARE_UNIT + SQUARE_UNIT / 2))
      
      # determin the color
      if board[r][c] == '?':
        pygame.draw.circle(screen, BLACK, circle_pos, RADIUS)
      elif board[r][c] == 'X':
        pygame.draw.circle(screen, RED, circle_pos, RADIUS)
      elif board[r][c] == 'O':
        pygame.draw.circle(screen, YELLOW, circle_pos, RADIUS)
  
  pygame.display.update()

# MAIN DRIVER
board = create_board()
is_game_over = False
current_turn = 0
draw_board(board)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
view_board_to_screen(screen, board)
pygame.display.update()

while not is_game_over:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    # tracking the mouse to draw a ball following it
    if event.type == pygame.MOUSEMOTION:
      # draw a black rectangle to cover up old circle
      pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_W, SQUARE_UNIT))
      pos_x = event.pos[0]
      if current_turn == 0:
        circle_pos = (pos_x, int(SQUARE_UNIT/2))
        pygame.draw.circle(screen, RED, circle_pos, RADIUS)
      elif current_turn == 1:
        circle_pos = (pos_x, int(SQUARE_UNIT/2))
        pygame.draw.circle(screen, YELLOW, circle_pos, RADIUS)
    pygame.display.update()

    # player press a column
    if event.type == pygame.MOUSEBUTTONDOWN:
      # ask p1 input
      if current_turn == 0:
        pos_x = event.pos[0]
        selection = int(math.floor( pos_x / SQUARE_UNIT ))

        if is_valid_location(board, selection):
          row = get_next_open_row(board, selection)
          drop_ball(board, row, selection, "X")

          if winning_move(board, "X"):
            print("P1 wins!!!")
            is_game_over = True
  
      # ask p2 input
      elif current_turn == 1:
        pos_x = event.pos[0]
        selection = int(math.floor( pos_x / SQUARE_UNIT ))

        if is_valid_location(board, selection):
          row = get_next_open_row(board, selection)
          drop_ball(board, row, selection, "O")

          if winning_move(board, "O"):
            print("P2 wins!!!")
            is_game_over = True

      draw_board(board)
      view_board_to_screen(screen, board)
      current_turn += 1
      current_turn = current_turn % 2

      if(is_game_over == True):
        pygame.time.wait(3000)