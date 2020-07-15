"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

# Special case implementation... ?
class FamilyTree:
    def __init__(self, ancestors = []):
        self.vertices = {}
        for item in ancestors:
            self.add_pair(item)
    
    def __str__(self):
        return str(self.vertices)


    def add_pair(self, pair):
        if pair[0] not in self.vertices:
            self.vertices[pair[0]] = set()
        if pair[1] not in self.vertices:
            self.vertices[pair[1]] = set()
        self.add_edge(pair[1], pair[0])


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


    def get_parents(self, vertex_id):
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


    def earliest(self, child):
        if child not in self.vertices:
            raise KeyError("Invalid starting vertex")

        # # check if child parameter has parents
        pending = Queue()
        depth = 0
        parents = [-1]
        for p in self.get_parents(child):
            pending.enqueue((p, depth+1))

        while len(pending) > 0:
            entry = pending.dequeue()

            if depth != entry[1]:
                depth = entry[1]
                parents = [entry[0]]
            else:
                parents.append(entry[0])

            for p in self.get_parents(entry[0]):
                pending.enqueue((p, depth+1))

        parents.sort()
        return parents[0]


    def bfs(self, starting_vertex, destination_vertex):
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


'''
persons = set(ID1, ID2, ...)
input: data[(parent, child), (parent, child)], personID

function(data, ID)

'''

def earliest_ancestor(ancestors, starting_node):
    g = FamilyTree(ancestors)
    # print(g)

    return g.earliest(starting_node)


if __name__ == '__main__':

    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

    print("--- EARLIEST ANCESTOR ---")
    print(earliest_ancestor(test_ancestors, 6))



