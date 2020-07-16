import random
import time
from util import Stack, Queue  # These may come in handy

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.reset()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}


    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id not in self.users:
            print(f"WARNING: No user with ID {user_id} exists")
            return False
        if friend_id not in self.users:
            print(f"WARNING: No user with ID {friend_id} exists")
            return False

        if user_id == friend_id:
            # print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def random_fill(self, num_users, avg_friendships):
        self.__init__()
        print("--- reset graph ---")
        print(self.friendships)
        for i in range(1, num_users+1):
            self.add_user(f"User {i}")

        # friends_pool = list(self.users.keys())
        delta = 0
        if num_users - avg_friendships > avg_friendships:
            delta = avg_friendships
        else:
            delta = num_users - avg_friendships
        min_friends = avg_friendships - delta
        # print(min_friends)
        max_friends = avg_friendships + delta
        # print(max_friends)

        print("gen num of friends")
        for k in self.users.keys():
            num_of_friends = random.randint(min_friends, max_friends)
            # print(num_of_friends)
            # print(k)
            friends = self.generate_random_friends(k, num_of_friends)
            print(friends)
            for f in friends:
                self.add_friendship(k, f)

        
    def generate_random_friends(self, myself, num_of_friends):
        # ensure that num_of_friends
        if self.last_id < num_of_friends:
            raise "Out of bounds"

        friends = set()
        for _ in range(num_of_friends):
            new_friend = random.randint(1, self.last_id)
            while (new_friend in friends) or (new_friend == myself):
                new_friend = random.randint(1, self.last_id)
            friends.add(new_friend)
            
        return friends

    def get_friends(self, user_id):
        return self.friendships[user_id]

    def get_extended(self, user_id, network = set()):
        for u in self.get_friends(user_id):
            network.add(u)
            self.get_extended(u, network)



    
    def bfs(self, starting_user, target_user):
        pass
        # pending = Queue()
        # visited = set()
        # path = []

        # pending.add()



    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()
        # !!!! IMPLEMENT ME
        print("--- reset graph ---")
        print(self.friendships)

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible_friendships = []
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        # shuffle the possible friendships
        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])


    def populate_graph2(self, num_users, avg_friendships):
        self.reset()

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        target = num_users * avg_friendships
        total = 0

        while total < target:
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)
            while user_id == friend_id:
                # user_id = random.randint(1, self.last_id)
                friend_id = random.randint(1, self.last_id)

            if self.add_friendship(user_id, friend_id):
                total += 2


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        pending = Queue()
        # visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        visited = {}

        pending.enqueue([user_id])

        while len(pending) > 0:
            path = pending.dequeue()
            user = path[-1]

            if user not in visited:
                visited[user] = path
                for friend in self.friendships[user]:
                    new_path = list(path)
                    new_path.append(friend)
                    pending.enqueue(new_path)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    num_users = 10
    avg_friends = 2

    # print(sg.friendships)
    start_time = time.time()
    sg.populate_graph(num_users, avg_friends)
    end_time = time.time()
    print(f"O(n^2) runtime: {end_time - start_time}")

    start_time = time.time()
    sg.populate_graph2(num_users, avg_friends)
    end_time = time.time()
    print(f"O(n) runtime: {end_time - start_time}")

    # sg.random_fill(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
