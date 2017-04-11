import numpy
import random
import math
from collections import namedtuple

Tile = namedtuple("Tile", "x y value")

class Game:

  def __init__(self):
    self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    self.score = 0

    self.insert_tile_random()
    self.insert_tile_random()

  def highest_square(self):
    return sorted(sum(self.board, []), reverse=True)[0]

  def game_over(self):
    return len(self.empty_cells()) == 0 and self.has_matches() == False

  def has_matches(self):
    for x in range(4):
      for y in range(1,3):
        value = self.board[x][y]
        if self.board[x][y - 1] == value or self.board[x][y + 1] == value:
           return True
    for x in range(1,3):
      for y in range(4):
        value = self.board[x][y]
        if self.board[x - 1][y] == value or self.board[x + 1][y] == value:
          return True
    return False


  def print_board(self):
    print(numpy.array(self.board).T)

  def each_cell(self, cb):
    for x in range(4):
      for y in range(4):
        cb(Tile(x, y, self.board[x][y]))

  def empty_cells(self):
    cells = []
    self.each_cell(lambda tile: cells.append(tile))
    cells = [cell for cell in cells if cell.value == 0]
    return cells

  def non_empty_cells(self):
    cells = []
    self.each_cell(lambda tile: cells.append(tile))
    cells = [cell for cell in cells if cell.value != 0]
    return cells

  def insert_tile_random(self):
    empty_cells = self.empty_cells()
    num_empty_cells = len(empty_cells)
    if num_empty_cells == 0:
      return
    index = math.floor(random.random() * num_empty_cells)
    cell = empty_cells[int(index)]
    self.board[cell.x][cell.y] = 2 if random.random() < 0.9 else 4

  def remove_all_empty(self):
    cells = self.non_empty_cells()
    new_board = []

    for x in range(4):
      new_board.append([cell for cell in self.board[x] if cell != 0])

    return new_board

  def fill_board(self, board, append):
    for x in range(4):
      num_items = len(board[x])
      for y in range(4 - num_items):
        board[x].append(0) if append else board[x].insert(0, 0)

    return board
  
  def set_new_board(self, board):
    is_board_same = self.board == board
    self.board = board

    if is_board_same == False:
      self.insert_tile_random()

  def up(self):
    empty_board = self.remove_all_empty()
    for x in range(4):
      num_items = len(empty_board[x])
      y = 0
      while y < num_items - 1 and empty_board[x][y]:
        if empty_board[x][y] == empty_board[x][y + 1]:
          empty_board[x][y] = empty_board[x][y] * 2
          self.score += empty_board[x][y]
          del empty_board[x][y + 1]
          num_items = len(empty_board[x])
        y += 1
    
    board = self.fill_board(empty_board, True)
    self.set_new_board(board)

  def down(self):
    empty_board = self.remove_all_empty()
    for x in range(4):
      num_items = len(empty_board[x])
      y = num_items - 1
      while y > 0 and empty_board[x][y]:
        if empty_board[x][y] == empty_board[x][y - 1]:
          empty_board[x][y] = empty_board[x][y] * 2
          self.score += empty_board[x][y]
          del empty_board[x][y - 1]
          num_items = len(empty_board[x])
        y -= 1

    board = self.fill_board(empty_board, False)
    self.set_new_board(board)

  def right(self):
    current_board = self.board
    self.board = numpy.array(self.board).T
    empty_board = self.remove_all_empty()
    
    empty_board = self.remove_all_empty()
    for x in range(4):
      num_items = len(empty_board[x])
      y = num_items - 1
      while y > 0 and empty_board[x][y]:
        if empty_board[x][y] == empty_board[x][y - 1]:
          empty_board[x][y] = empty_board[x][y] * 2
          self.score += empty_board[x][y]
          del empty_board[x][y - 1]
          num_items = len(empty_board[x])
        y -= 1

    board = self.fill_board(empty_board, False)
    self.board = current_board
    self.set_new_board(numpy.array(board).T.tolist())

  def left(self):
    current_board = self.board
    self.board = numpy.array(self.board).T
    empty_board = self.remove_all_empty()
    for x in range(4):
      num_items = len(empty_board[x])
      y = 0
      while y < num_items - 1 and empty_board[x][y]:
        if empty_board[x][y] == empty_board[x][y + 1]:
          empty_board[x][y] = empty_board[x][y] * 2
          self.score += empty_board[x][y]
          del empty_board[x][y + 1]
          num_items = len(empty_board[x])
        y += 1
    
    board = self.fill_board(empty_board, True)
    self.board = current_board
    self.set_new_board(numpy.array(board).T.tolist())