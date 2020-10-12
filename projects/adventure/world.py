from room import Room
import random
import math
from termcolor import colored


class World:
    def __init__(self):
        self.starting_room = None
        self.rooms = {}
        self.room_grid = []
        self.grid_size = 0

    def load_graph(self, room_graph):
        num_rooms = len(room_graph)
        rooms = [None] * num_rooms
        grid_size = 1
        for i in range(0, num_rooms):
            x = room_graph[i][0][0]
            grid_size = max(
                grid_size, room_graph[i][0][0], room_graph[i][0][1])
            self.rooms[i] = Room(
                f"Room {i}", f"({room_graph[i][0][0]},{room_graph[i][0][1]})", i, room_graph[i][0][0], room_graph[i][0][1])
        self.room_grid = []
        grid_size += 1
        self.grid_size = grid_size
        for i in range(0, grid_size):
            self.room_grid.append([None] * grid_size)
        for room_id in room_graph:
            room = self.rooms[room_id]
            self.room_grid[room.x][room.y] = room
            if 'n' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms(
                    'n', self.rooms[room_graph[room_id][1]['n']])
            if 's' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms(
                    's', self.rooms[room_graph[room_id][1]['s']])
            if 'e' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms(
                    'e', self.rooms[room_graph[room_id][1]['e']])
            if 'w' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms(
                    'w', self.rooms[room_graph[room_id][1]['w']])
        self.starting_room = self.rooms[0]

    def print_map(self, player_room, visited_rooms, starting_room, tot_cols=26, tot_rows=28):
        rotated_room_grid = []
        for i in range(0, len(self.room_grid)):
            rotated_room_grid.append([None] * len(self.room_grid))
        for i in range(len(self.room_grid)):
            for j in range(len(self.room_grid[0])):
                rotated_room_grid[len(self.room_grid[0]) -
                                  j - 1][i] = self.room_grid[i][j]
        # print("######")
        # row_len = len(self.room_grid) * 7
        row_len = tot_cols * 7
        col_header = f"... WORLD MAP (Grid Size: {self.grid_size})..."
        pref = [" "] * ((row_len - len(col_header)) // 2)
        post = [" "] * (row_len - len(col_header) - len(pref))
        print(f"      {''.join(pref) + col_header + ''.join(post)} ")
        s = ""
        for i in range(tot_cols):
            s += "  " + f"{i}".zfill(3) + "  "
        print(f"      {s} ")
        print(f"      {'#'*len(s)}#")

        str = ""
        for r, row in enumerate(rotated_room_grid):
            all_null = True
            for room in row:
                if room is not None:
                    all_null = False
                    break
            if all_null:
                continue

            # PRINT NORTH CONNECTION ROW
            top_line = "     #"
            mid_line = "[" + f"{self.grid_size - r - 1}".zfill(2) + "] #"
            bot_line = "     #"
            for i in range(tot_cols):
                room = row[i]
                if room is not None:
                    # PRINT ROOM ROW
                    if room.n_to is not None:
                        top_line += " ╔═╩═╗ "
                    else:
                        top_line += " ╔═══╗ "

                    if room.w_to is not None:
                        mid_line += "═╣"
                    else:
                        mid_line += " ║"

                    if room.id == player_room.id:
                        mid_line += colored(" P ", 'blue')
                    elif room.id == starting_room.id:
                        mid_line += colored(" X ", 'red')
                    elif room.id in visited_rooms:
                        mid_line += colored(f"{room.id}".zfill(3), 'green')
                    else:
                        mid_line += f"{room.id}".zfill(3)
                    if room.e_to is not None:
                        mid_line += "╠═"
                    else:
                        mid_line += "║ "

                    if room.s_to is not None:
                        bot_line += " ╚═╦═╝ "
                    else:
                        bot_line += " ╚═══╝ "

                else:
                    top_line += "   │   "
                    mid_line += "───┼───"
                    bot_line += "   │   "

                # top_line += "#\n"
                # mid_line += "#\n"
                # bot_line += "#\n"

            str += f"{top_line}#\n{mid_line}#\n{bot_line}#\n"

        print(str)
        print("#####")


'''

 ┌──┴──┐
─┤     ├─┼─
 └──┬──┘
    │


 ╔═╩═╗
═╣   ╠═╬═
 ╚═╦═╝
   ║

'''
