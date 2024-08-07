## Define Graph
class Graph():
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex in list(self.graph.keys()):
            print(f"Vertex {vertex} already exists")
        else:
            self.graph[vertex] = {}
        
    def add_edge(self, first_vertex, second_vertex, weight):
        if first_vertex not in list(self.graph.keys()):
            self.add_vertex(first_vertex)
        
        if second_vertex not in list(self.graph.keys()):
            self.add_vertex(second_vertex)
    
        self.graph[first_vertex][second_vertex] = weight
        self.graph[second_vertex][first_vertex] = weight
    
    def remove_vertex(self, vertex_to_delete):
        self.list_of_edges = list(self.graph[vertex_to_delete].keys())
        for self.adjacent_vertex in self.list_of_edges:
            del self.graph[self.adjacent_vertex][vertex_to_delete]

        del self.graph[vertex_to_delete]

    def remove_edge(self, first_vertex, second_vertex):
        self.vertices = list(self.graph.keys())
        if first_vertex in self.vertices and second_vertex in self.vertices:
            del self.graph[first_vertex][second_vertex]
            del self.graph[second_vertex][first_vertex]
        else:
            print(f'Vertex {first_vertex} or {second_vertex} does not exist')

    def print_vertices(self):
        self.list_of_vertices = list(self.graph.keys())
        self.list_of_vertices.sort()
        for vertex in self.list_of_vertices:
                print(f"Vertex: {vertex}")
                print(f"Edges from vertex: {self.graph[vertex]}")


## Dijkstra’s algorithm function (must have a 0 vertex)
def dijkstras_algorithm(graph_instance, source_vertex, end_vertex):
    ## List of vertices: all vertices from graph
    ## Shortest Path Tree set: list of visited vertices
    ## List of distances: distances from visited vertices and their adjacent vertices
    list_of_vertices = list(graph_instance.graph.keys())
    
    sptSet = [0] * (max(list_of_vertices) + 1)
    
    distances_list = [float("inf")] * (max(list_of_vertices) + 1)
    distances_list[source_vertex] = 0

    while 0 in sptSet:
        ## Sort distances and loop through them to find
        ## non-visited vertice with smallest distance
        sorted_distances_list = distances_list.copy()
        sorted_distances_list.sort()

        ## Get all indeces for each distance,
        ## as they might repeat
        for distance in sorted_distances_list:
            each_distance_index = [i for i,x in enumerate(distances_list) if x == distance]                        
            for current_index in each_distance_index:
                if sptSet[current_index] == 0:
                    correct_vertex_index = current_index
                    break


            if sptSet[correct_vertex_index] == 0:
                vertex_with_smallest_distance = correct_vertex_index
                distance_of_current_vertex = distance
                break
        
        ## Set vertex as visited
        sptSet[vertex_with_smallest_distance] = 1

        ## Change distance of adjacent vertices if new path is shorter
        ## and if they are non-visited
        try:
            adjacent_vertices = graph_instance.graph[vertex_with_smallest_distance].keys()
        except KeyError:
            continue
        
        for vertex in adjacent_vertices:
            if sptSet[vertex] == 1:
                continue
            else:
                new_distance_for_adjacent_vertex = graph_instance.graph[vertex_with_smallest_distance][vertex] + distance_of_current_vertex
                if distances_list[vertex] == 0:
                    distances_list[vertex] = new_distance_for_adjacent_vertex
                elif distances_list[vertex] > new_distance_for_adjacent_vertex:
                    distances_list[vertex] = new_distance_for_adjacent_vertex

    ## Check fastest route
    if distances_list[end_vertex] == float("inf"):
        print("Graph is disjointed")
        return 1

    sum = distances_list[end_vertex]
    path = [end_vertex]
    current_vertex = end_vertex
    while sum != 0:
        for adjacent_vertex in graph_instance.graph[current_vertex].keys():
            if  distances_list[current_vertex] - distances_list[adjacent_vertex] == graph_instance.graph[current_vertex][adjacent_vertex]:
                sum -= graph_instance.graph[current_vertex][adjacent_vertex]
                current_vertex = adjacent_vertex
                path.append(current_vertex)
                break
    
    return path

                    
if __name__ == '__main__':
    graph_instance = Graph()
    graph_instance.add_edge(6,5,1)
    graph_instance.add_edge(5,1,2)
    graph_instance.add_edge(0,2,3)
    graph_instance.add_edge(0,1,4)
    graph_instance.add_edge(1,3,2)
    graph_instance.add_edge(2,3,5)
    graph_instance.add_edge(3,4,2)
    graph_instance.add_edge(6,3,1)
    graph_instance.add_edge(4,7,5)
    graph_instance.add_edge(4,9,1)
    graph_instance.add_edge(2,9,2)
    graph_instance.add_edge(7,8,4)
    graph_instance.add_edge(8,9,1)
    graph_instance.add_edge(9,10,3)
    graph_instance.add_edge(8,10,1)
    graph_instance.add_edge(10,11,2)

    graph_instance.print_vertices()

    path = dijkstras_algorithm(graph_instance, 6, 11)
    print(path)