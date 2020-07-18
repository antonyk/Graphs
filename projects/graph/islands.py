'''
Connected components
'''
from util import Stack, Queue  # These may come in handy

islands = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]


islands2 = [[1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
           [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
           [0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
           [0, 0, 1, 1, 0, 1, 0, 1, 1, 0],
           [0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
           [0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
           [1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
           [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
           [0, 0, 1, 1, 0, 1, 0, 0, 1, 0]]

'''
islands = [[F, T, F, F, F],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]
'''

def island_counter(islands):
  # create a visited matrix
  island_count = 0
  row_count = len(islands)
  col_count = len(islands[0])

  visited = []
  for _ in range(row_count):
    visited.append([False] * col_count)

  # walk through each cell of the matrix
  for row, _ in enumerate(islands):
    for col, _ in enumerate(islands[row]):
      if not visited[row][col]:
        if islands[row][col] == 1:
          # traverse and mark each as visited
          dft(row, col, islands, visited)

          # increment counter
          island_count += 1

  return island_count


def dft(row, col, islands, visited):
  pending = Stack()

  pending.push((row, col))

  while len(pending) > 0:
    r, c = pending.pop()

    if not visited[r][c]:
      visited[r][c] = True

      for neighbor in get_neighbors(row, col, islands):
        pending.push(neighbor)


def get_neighbors(row, col, islands):
  # row, col = cell
  neighbors = []
  row_count = len(islands)
  col_count = len(islands[0])

  # check north
  if row > 0 and islands[row-1][col] == 1:
    neighbors.append((row-1, col))

  # check east
  if col < col_count - 1 and islands[row][col+1] == 1:
    neighbors.append((row, col+1))

  # check south
  if row < row_count - 1 and islands[row+1][col] == 1:
    neighbors.append((row+1, col))

  # check west  
  if col > 0 and islands[row][col-1] == 1:
    neighbors.append((row, col-1))


  return neighbors

    # if it's not been visited
      #if we hit a 1 on the islands

print(island_counter(islands)) # returns 4
print(island_counter(islands2))

