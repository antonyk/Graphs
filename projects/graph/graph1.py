class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Graph:
  def __init__(self):
    self.vertices = {}


  def add_vertex(self, vertex_id):
    self.vertices[vertex_id] = set() # will hold edges

  def add_edge(self, start_vertex_id, end_vertex_id):
    if (start_vertex_id in self.vertices) and (end_vertex_id in self.vertices):
      self.vertices[start_vertex_id].add(end_vertex_id)
    else:
      raise IndexError("non-existent vert")

  def get_neighbors(self, vertex_id):
    return self.vertices[vertex_id]

  def bft(self, vertex_id):
    # create an empty queue
    q = Queue()
    # create a set to store the visited verts
    visited = set()

    # init with the starting vert
    q.enqueue(vertex_id)

    # while queue isn't empty
    while q.size > 0:
      # dequeue first item
      cur_vert = q.dequeue()
      # if it's not in visited
      if cur_vert not in visited:
        # mark as visited
        visited.add(cur_vert)
        print(f"Visited {cur_vert}")
        # add all neighbors to the queue
        for neighbor in self.get_neighbors(cur_vert):
          q.enqueue(neighbor)


  def shortest_path_search(self, starting_vertex_id, target_vertex_id):
    # shortest path to a location
    # use breath-first
    # store full path in together with each "visited" vert
    print("Not Implemented")



def breadth_first(graph, vertex_id):
  result = {}
  # neighbors = graph.get_neighbors(vertex_id)
  # while len(neighbors) > 0:
  #   for vert in neighbors:
  #     if vert not in result:
  #       result.add(vert)

  #   for vert in neighbors:
  #     children = graph.get_neighbors()

  #   for vert in children

  #   neighbors = graph.get_neighbors()

  return result


g = Graph()

g.add_vertex('A')
g.add_vertex('B')
g.add_vertex('C')

g.add_edge('A', 'B')
g.add_edge('A', 'C')

g.add_edge('B', 'B')
g.add_edge('B', 'A')
g.add_edge('B', 'C')

print(g.vertices)



