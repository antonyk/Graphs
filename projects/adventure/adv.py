from room import Room
from player import Player
from world import World

import random
import math
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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def get_optimal_path(starting_room, max_rooms):
    directions = starting_room.get_exits()
    travel_path = []
    for direction in directions:
        # new_path = explore(Player(player.current_room.get_room_in_direction(direction)))
        new_path = explore(Player(starting_room), max_rooms, direction)
        if len(new_path) < len(travel_path) or len(travel_path) == 0:
            travel_path = new_path

    return travel_path


def randomize_directions(directions):
    # result = list(directions)
    if len(directions) > 1:
        first = random.randint(0, len(directions)-1)
        second = random.randint(0, len(directions)-1)
        # while first == second:
        #     second = random.randint(0,len(directions)-1)

        directions[first], directions[second] = directions[second], directions[first]

    return directions


def explore(player, max_rooms, initial_directions=None):
    travel_path = []
    pending = collections.deque()  # Stack() #
    traversed = {}
    cur_pending = set()

    # init
    cur = player.current_room
    exits = randomize_directions(cur.get_exits())
    # exits = cur.get_exits()
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

    # if initial_directions:
    #     exits = []
    #     for item in initial_directions:
    #         exits.append(item)

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
    # print("Starting room: ", end='')
    # print(traversed)
    # print("Initial stack: ", end='')
    # print(pending)
    # print(" ")

    while len(traversed) < max_rooms:  # len(pending) > 0:
        if len(pending) > 0:
            travel_entry = pending.pop()
            # print("Popped: " + str(travel_entry) + " -> Remaining: " + str(pending))
            travel_dir = travel_entry[1]
            player.travel(travel_dir)
            # print(travel_dir)
            travel_path.append(travel_dir)
            cur = player.current_room
            # exits = cur.get_exits()
            exits = randomize_directions(cur.get_exits())
            # print(exits == cur.get_exits())
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
                        backtrack = (
                            neighbor.id, get_opposite_direction(direction))
                        pending.append(backtrack)
                        cur_pending.add(backtrack)
                        # forward instructions
                        pending.append((cur.id, direction))
                        cur_pending.add(forward)

            from_room_id = travel_entry[0]
            traversed[from_room_id][travel_dir] = cur.id
            traversed[cur.id] = entry

        else:
            print("NO more travel paths... do something else")

    return travel_path


def explore2(player, max_rooms):
    path = []
    explored_rooms = set()
    while len(explored_rooms) < max_rooms:
        weight = math.inf
        new_path = []
        for direction in player.current_room.get_exits():
            result = find_path_to_nearest_leaf(
                player.current_room, explored_rooms)
            if result[1] < weight:  # and random.randint(0,1) == 1:
                weight = result[1]
                new_path = result[0]

        # new_path = find_path_to_nearest_leaf(player.current_room, explored_rooms)
        # print(new_path)
        # move whole path
        for direction in new_path:
            player.travel(direction)
            explored_rooms.add(player.current_room.id)
        path.extend(new_path)

        # move one room at a time and recalculate
        # if len(new_path) > 0:
        #     direction = new_path[0]
        #     player.travel(direction)
        #     explored_rooms.add(player.current_room.id)
        #     path.append(direction)

    return path


# find the nearest unexplored leaf
# node is an unexplored leaf if:
# -> it is not in the explored_rooms set
# -> its neighbors have all been visited
def find_path_to_nearest_leaf(starting_room, explored_rooms):
    pending = collections.deque()  # use as a Queue
    visited = set()
    path = []

    cur = starting_room
    visited.add(cur.id)
    exits = cur.get_exits()
    is_leaf = True
    weight = 1
    for direction in exits:
        room = cur.get_room_in_direction(direction)
        if room.id not in visited:
            new_path = list(path)
            new_path.append(direction)
            pending.append((room, new_path, 1))
            is_leaf = False

    if is_leaf and cur.id not in explored_rooms:
        # this is the unexplored leaf;
        # return path to it
        return (path, weight)

    while len(pending) > 0:
        element = pending.popleft()
        cur = element[0]
        visited.add(cur.id)
        exits = cur.get_exits()
        is_leaf = True
        weight = element[2]
        for direction in exits:
            room = cur.get_room_in_direction(direction)
            if room.id not in visited:
                neighbors = len(unvisited_neighbors(room, explored_rooms))
                new_path = list(element[1])
                new_path.append(direction)
                pending.append((room, new_path, weight +
                                neighbors * neighbors / 2))
                is_leaf = False

        if is_leaf and cur.id not in explored_rooms:
            # this is the unexplored leaf;
            # return path to it
            return (element[1], weight)

    raise "Cannot Find Unexplored Leaf"


def unvisited_neighbors(from_room, explored_rooms):
    count = 0
    exits = from_room.get_exits()
    rooms = []
    for direction in exits:
        room = from_room.get_room_in_direction(direction)
        if room.id not in explored_rooms:
            rooms.append(room)

    return rooms


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

# init player
player.current_room = world.starting_room

dft_traversal_path = explore(Player(player.current_room), len(room_graph))
for i in range(1):
    new_path = explore(Player(player.current_room), len(room_graph))
    if len(new_path) < len(dft_traversal_path):
        dft_traversal_path = list(new_path)

bft_traversal_path = explore2(Player(player.current_room), len(room_graph))

dft_steps = len(dft_traversal_path)
bft_steps = len(bft_traversal_path)
print(f"Depth-First traversal: {dft_steps} steps")
print(f"Breath-First traversal: {bft_steps} steps")

traversal_path = dft_traversal_path if dft_steps < bft_steps else bft_traversal_path

# print(traversal_path)


if len(traversal_path) < 960:
    print(traversal_path)


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
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


# ######
# UNCOMMENT TO WALK BASED ON PATH
# ######
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room.id)
world.print_map(player.current_room, visited_rooms, world.starting_room)
cur_path = []
for move in traversal_path:
    cmds = input("-> ").lower().split(" ")
    player.travel(move)
    cur_path.append(move)
    visited_rooms.add(player.current_room.id)
    world.print_map(player.current_room, visited_rooms, world.starting_room)
    print(cur_path)
