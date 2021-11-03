import numpy as np
from queue import PriorityQueue
from constants import world_size

WALL = 'wall'
EMPTY = 'empty'

#start_cor_y = 240
#start_cor_x = 150

#end_cor_y = 120
#end_cor_x = 145



class Cell:
    def __init__(self, row, col):
        self.col = col
        self.row = row
        self.state = EMPTY
        self.neighbours = []
        self.total_size = world_size
        self.total_rows = world_size

    # returns the x and y coordinate of the cell.
    def get_pos(self):
        return self.row, self.col

    # returns true if the cell contains a wall.
    def is_wall(self):
        return self.state == WALL

    # sets the cell to contain a wall
    def make_wall(self):
        self.state = WALL

    # this function goes through the whole grid of cell objects and
    # finds out if their direct neighbour cells contain walls. Adds the non-wall neighbours to a list.
    def find_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_size -1 and not grid[self.row+1][self.col].is_wall():  # down neighbour
            self.neighbours.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_wall():  # up neighbour
            self.neighbours.append(grid[self.row-1][self.col])

        if self.col < self.total_rows -1 and not grid[self.row][self.col + 1].is_wall():  # right neighbour
            self.neighbours.append(grid[self.row][self.col + 1 ])

        if self.col > 0 and not grid[self.row][self.col-1].is_wall():  # left neighbour
            self.neighbours.append(grid[self.row][self.col-1])


        # additional 4 directions
        if (self.row < self.total_size -1 and self.col > 0) and not grid[self.row+1][self.col-1].is_wall():  # down left neighbour
            self.neighbours.append(grid[self.row+1][self.col-1])

        if (self.row < self.total_size-1 and self.col < self.total_rows-1) and not grid[self.row+1][self.col+1].is_wall():  # down right neighbour
            self.neighbours.append(grid[self.row+1][self.col+1])

        if (self.row > 0 and self.col > 0) and not grid[self.row-1][self.col - 1].is_wall():  # upper left neighbour
            self.neighbours.append(grid[self.row-1][self.col-1])

        if (self.row > 0 and self.col < self.total_rows-1) and not grid[self.row-1][self.col+1].is_wall():  # upper right neighbour
            self.neighbours.append(grid[self.row-1][self.col+1])

        pass


# this function creates a grid of cell objects
def make_grid(world_size):

    grid = []

    for i in range(world_size):
        grid.append([])
        for j in range(world_size):
            cell = Cell(i, j)
            grid[i].append(cell)

    return grid


# this function looks for walls on the world map and places them in the correct cells on the cell grid.
def find_walls(grid, world_map, world_size):

    for i in range(world_size):
        for j in range(world_size):
            if world_map[i][j] == 20:
                cell = grid[i][j]
                cell.make_wall()

                #test of anti wall-hugging
                for extra in range(1,10):

                    if i-extra > 0 and j-extra > 0:
                        cell = grid[i-extra][j-extra]
                        cell.make_wall()

                    if i-extra > 0:
                        cell = grid[i-extra][j]
                        cell.make_wall()

                    if i-extra > 0 and j+extra < world_size:
                        cell = grid[i-extra][j+extra]
                        cell.make_wall()

                    # middle row
                    if j + extra < world_size:

                        cell = grid[i][j+extra]
                        cell.make_wall()

                    if j-extra > 0:
                        cell = grid[i][j-extra]
                        cell.make_wall()

                    #bottom row
                    if i+extra < world_size and j-extra > 0:
                        cell = grid[i+extra][j-extra]
                        cell.make_wall()

                    if i + extra < world_size:
                        cell = grid[i + extra][j]
                        cell.make_wall()

                    if i + extra < world_size and j+extra < world_size:
                        cell = grid[i + extra][j + extra]
                        cell.make_wall()



    return


# this function calculetes the heuristic score,
# which is the direct distance between the current cell and the goal.
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# this function recreates the shortest path from the end cell to the start cell and puts it in a list.
def reconstruct_path(came_from, current):

    path = []
    path.append(current.get_pos())
    while current in came_from:
        current = came_from[current]
        path.append(current.get_pos())

    return path


# this is the pathfinding algorithm itself
def pathfinding(grid, start, end_goal):

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    # here we set the initial g- and f-score to be infinate,
    # any value that we actually calculate will be lower and replace the infinite one.
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end_goal.get_pos())

    open_set_hash = {start}

    while not open_set.empty():

        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end_goal:

            path = reconstruct_path(came_from, end_goal)
            return path

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1  # neighbour at least 1 hop away

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current  # 1h21m
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end_goal.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)

    return False

#def find_path(grid,world_map,world_size, start_cor, end_cor):
def find_path(grid, world_map, world_size, start_cor_y, start_cor_x, end_cor_y, end_cor_x):

    start_cor_y = start_cor_y.astype(np.int32)
    start_cor_x = start_cor_x.astype(np.int32)


    end_cor_y = end_cor_y
    end_cor_x = end_cor_x

    #print (end_cor_y,end_cor_x)
    find_walls(grid, world_map, world_size)

    cell = grid[start_cor_y][start_cor_x]
    start = cell

    cell = grid[end_cor_y][end_cor_x]
    end_goal = cell

    for row in grid:
        for cell in row:
            cell.find_neighbours(grid)

    p = pathfinding(grid, start, end_goal)

    #print(p)
    p.reverse()
    #print(p)
    return p
