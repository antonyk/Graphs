from room import Room
from player import Player
from world import World

import random
import collections
from util import Stack, Queue
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def get_optimal_path(player, max_rooms):
    directions = player.current_room.get_exits()
    travel_path = []
    for direction in directions:
        # new_path = explore(Player(player.current_room.get_room_in_direction(direction)))
        new_path = explore(Player(player.current_room), max_rooms, direction)
        # new_path = explore(player, max_rooms, direction)
        if len(new_path) < len(travel_path) or len(travel_path) == 0:
            travel_path = new_path

    

    return travel_path

def explore(player, max_rooms, initial_directions=None):
    travel_path = []
    pending = collections.deque() # Stack() # 
    traversed = {}
    cur_pending = set()

    # init
    cur = player.current_room
    exits = cur.get_exits()
    entry = {}
    # if initial_direction and initial_direction in exits:
    #     neighbor = cur.get_room_in_direction(initial_direction)
    #     if neighbor.id in traversed:
    #         entry[initial_direction] = neighbor.id
    #     else:
    #         entry[initial_direction] = '?'
    #         # return instructions
    #         pending.append((neighbor.id, get_opposite_direction(initial_direction)))
    #         # forward instructions
    #         pending.append((cur.id, initial_direction))
    #     exits.remove(initial_direction)

    if initial_directions:
        exits = []
        for item in initial_directions:
            exits.append(item)

    for direction in exits:
        neighbor = cur.get_room_in_direction(direction)
        if neighbor.id in traversed:
            entry[direction] = neighbor.id
        else:
            entry[direction] = '?'
            forward = (cur.id, direction)
            if forward not in cur_pending:
                # return instructions
                backtrack = (neighbor.id, get_opposite_direction(direction))
                pending.append(backtrack)
                cur_pending.add(backtrack)
                # forward instructions
                pending.append((cur.id, direction))
                cur_pending.add(forward)

    traversed[cur.id] = entry
    # print(entry)
    print("Starting room: ", end='')
    print(traversed)
    print("Initial stack: ", end='')
    print(pending)
    print(" ")

    while len(traversed) < max_rooms: # len(pending) > 0:
        if len(pending) > 0:
            travel_entry = pending.pop()
            # print("Popped: " + str(travel_entry) + " -> Remaining: " + str(pending))
            travel_dir = travel_entry[1]
            player.travel(travel_dir)
            # print(travel_dir)
            travel_path.append(travel_dir)
            cur = player.current_room
            exits = cur.get_exits()
            entry = {}
            for direction in exits:
                neighbor = cur.get_room_in_direction(direction)
                if neighbor.id in traversed:
                    entry[direction] = neighbor.id
                else:
                    entry[direction] = '?'
                    forward = (cur.id, direction)
                    if forward not in cur_pending:
                        # return instructions
                        backtrack = (neighbor.id, get_opposite_direction(direction))
                        pending.append(backtrack)
                        cur_pending.add(backtrack)
                        # forward instructions
                        pending.append((cur.id, direction))
                        cur_pending.add(forward)

                    # pending.append((neighbor.id, get_opposite_direction(direction)))
                    # pending.append((cur.id, direction))
                    # print("New stack: " + str(pending))

            from_room_id = travel_entry[0]
            traversed[from_room_id][travel_dir] = cur.id
            traversed[cur.id] = entry
            # print(entry)
            # print("Traversed so far: ", traversed)
            # print(traversed)
            # print(pending)
            # print(" ")

        else:
            print("NO more travel paths... do something else")

    return travel_path


def get_opposite_direction(direction):
    if direction == "n":
        return "s"
    elif direction == "e":
        return "w"
    elif direction == "s":
        return "n"
    elif direction == "w":
        return "e"
    else:
        raise "Invalid Direction"

iniital_setup = {
    0: ["w", "n", "e", "s"],
    1: ["w", "n", "s", "e"],
    2: ["w", "s", "n", "e"],
    3: ["w", "s", "e", "n"],
    4: ["w", "s", "e", "n"],
    5: ["w", "s", "e", "n"],
    6: ["w", "s", "e", "n"],
    7: ["w", "s", "e", "n"]
}

initial_directions = ["w", "e", "s", "n"]

traversal_path = explore(player, len(room_graph), initial_directions)
# print(traversal_path)

player.current_room = world.starting_room


#######
# UNCOMMENT TO WALK BASED ON PATH
#######
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room.id)
# world.print_map(player.current_room, visited_rooms, world.starting_room)
# cur_path = []
# for move in traversal_path:
#     cmds = input("-> ").lower().split(" ")
#     player.travel(move)
#     cur_path.append(move)
#     visited_rooms.add(player.current_room.id)
#     world.print_map(player.current_room, visited_rooms, world.starting_room)
#     print(cur_path)


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

