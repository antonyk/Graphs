"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if (vertex_id not in self.vertices):
            self.vertices[vertex_id] = set()
            # print(f"Added vertex {vertex_id}")
        else:
            raise KeyError("Vertex already exists")

    def add_edge(self, v1, v2):
        if v1 not in self.vertices:
            raise IndexError(f"Failed to add edge {v1}, {v2}. Source vertex {v1} does not exist.")
        if v2 not in self.vertices:
            raise IndexError(f"Failed to add edge {v1}, {v2}. Target vertex {v2} does not exist.")

        self.vertices[v1].add(v2)
        # print(f"Added edge from {v1} to {v2}")

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        pending = Queue()
        visited = set()

        if starting_vertex in self.vertices:
            pending.enqueue(starting_vertex)
        while len(pending) > 0:
            vert = pending.dequeue()
            if vert not in visited:
                visited.add(vert)
                print(vert)
                # print(f"BFT: Visited vertex {vert}")
                for neighbor in self.get_neighbors(vert):
                    pending.enqueue(neighbor)

    def dft(self, starting_vertex):
        pending = Stack()
        visited = set()

        if starting_vertex in self.vertices:
            pending.push(starting_vertex)
        while len(pending) > 0:
            vert = pending.pop()
            if vert not in visited:
                visited.add(vert)
                print(vert)
                # print(f"DFT: Visited vertex {vert}")
                for neighbor in self.get_neighbors(vert):
                    pending.push(neighbor)

    def dft_recursive(self, starting_vertex):
        # visited = set()

        # def dft_rec(self, visited, vert):
        #     for neighbor in self.get_neighbors(vert):
        #         if neighbor not in visited:
        #             dft_rec(visited, neighbor)

        # dft_rec(visited, starting_vertex)




        # self.get_neighbors(starting_vertex)
        print("NOT implemented")

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path
        """
        if starting_vertex not in self.vertices:
            raise KeyError("Invalid starting vertex")
        if destination_vertex not in self.vertices:
            raise KeyError("Invalid destination vertex")

        visited = set()
        pending = Queue()
        path = [starting_vertex]
        pending.enqueue(path)
        while len(pending) > 0:
            path = pending.dequeue()
            # print(path)
            vert = path[-1]
            # potentially move this inside the visited check
            if vert == destination_vertex:
                return path

            if vert not in visited:
                visited.add(vert)
                for neighbor in self.get_neighbors(vert):
                    new_path = list(path)
                    new_path.append(neighbor)
                    pending.enqueue(new_path)

        return None # path to destination vert not found


    def word_search(self, starting_word, ending_word):

        pass


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        if starting_vertex not in self.vertices:
            raise KeyError("Invalid starting vertex")
        if destination_vertex not in self.vertices:
            raise KeyError("Invalid destination vertex")

        visited = set()
        pending = Stack()
        path = [starting_vertex]
        pending.push(path)
        while len(pending) > 0:
            path = pending.pop()
            vert = path[-1]
            if vert == destination_vertex:
                return path

            if vert not in visited:
                visited.add(vert)
                for neighbor in self.get_neighbors(vert):
                    new_path = list(path)
                    new_path.append(neighbor)
                    pending.push(new_path)

        return None # path to destination vert not found


    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        print("NOT implemented")

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))


    # print("----- FROM README -----")
    # graph = Graph()
    # graph.add_vertex('0')
    # graph.add_vertex('1')
    # graph.add_vertex('2')
    # graph.add_vertex('3')
    # graph.add_edge('0', '1')
    # graph.add_edge('1', '0')
    # graph.add_edge('0', '3')
    # graph.add_edge('3', '0')
    # graph.add_edge('0', '4')  # No '4' vertex, should raise an Exception!    
    # print(graph.vertices)

    # graph.bft('0')



    def find_words(starting_word, ending_word):
        visited = set()
        pending = Queue()

        pending.enqueue([starting_word])

        while len(pending) > 0:
            path = pending.dequeue()
            vert = path[-1]

            if vert == ending_word:
                return path
            
            if vert not in visited:
                visited.add(vert)
                for neighbor in get_neighbors(vert):
                    new_path = list(path)
                    new_path.append(neighbor)
                    pending.enqueue(new_path)


    import string
    letters = list(string.ascii_lowercase)
    word_set = set(['hit', 'hot', 'hog', 'cog', 'cot'])

    def get_neighbors(word):
        neighbors = []
        # g = Graph()

        # starting_word = list(word)

        for i, _ in enumerate(word):
            for letter in letters:
                new_word = list(word)
                new_word[i] = letter
                w = "".join(new_word)

                if w == word:
                    continue

                if w in word_set:
                    neighbors.append(w)

        return neighbors



    print(find_words("hit", "cog"))
