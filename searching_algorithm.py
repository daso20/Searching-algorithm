import pygame
from dijkstra_algorithm import Graph, dijkstras_algorithm

## Screen settings
background_colour = (255, 255, 255)
screen = pygame.display.set_mode((1000, 1000)) 
pygame.display.set_caption('Searching algorithm')
screen.fill(background_colour)
pygame.display.flip()

## Reference:
## circles = [{"selected" : 1, "coordinates": (100,100), "circle_for_edge": 0}, {"selected": 0 , "coordinates": (200,200), "circle_for_edge": 0}]
## edges = [[(50, 50),(50, 100),(0,1)], [(300,400),(500,600),(1,2)]] --> Coordinates vertex 1, coordinates vertex 2, vertex 1/vertex 2
circles = []
edges = []
selected_circles = []
edge_of_circles = []
path = []
dijkstras_algorithm_executed = 0

def check_collition(x, y):
    if len(circles) == 0:
         return (False, 0)
    
    i = 0

    for circle in circles:
        if ((y - circle["coordinates"][1])**2 + (x - circle["coordinates"][0])**2)**0.5 < 8:
            return (1, i)
        elif ((y - circle["coordinates"][1])**2 + (x - circle["coordinates"][0])**2)**0.5 < 15:
            return (2, i)
        i += 1

    return (False, 0)

def create_graph(edges):
    new_graph = Graph()
    for edge in edges:
        weight = int(((edge[1][1] - edge[0][1])**2 + (edge[1][0] - edge[0][0])**2)**0.5)
        new_graph.add_edge(edge[2][0], edge[2][1], weight)
    return new_graph
    


## Start display
running = True
while running:
    for circle in circles:
        pygame.draw.circle(screen, (0, 0, 0), circle["coordinates"], 8)
        if circle["circle_for_edge"] == 1:
            pygame.draw.circle(screen, (0, 255, 0), circle["coordinates"], 6)
        elif circle["selected"] == 1:
            pygame.draw.circle(screen, (255, 0, 0), circle["coordinates"], 6)
        else:
            pygame.draw.circle(screen, (255, 255, 255), circle["coordinates"], 6)
    
    for edge in edges:
        if edge[2][0] in path and edge[2][1] in path:
            pygame.draw.line(screen, (255, 0, 0), edge[0], edge[1])
        else:
            pygame.draw.line(screen, (0, 0, 0), edge[0], edge[1])

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]: # Left click
                check_collition_result, check_collition_index = check_collition(x, y)
                if check_collition_result == 1:
                    if check_collition_index in edge_of_circles:
                        pass
                    else:
                        circles[check_collition_index]["circle_for_edge"] = 1
                        edge_of_circles.append(check_collition_index)
                elif check_collition_result == 2:
                    pass
                else:
                    circles.append({"selected" : 0, "coordinates":(x, y), "circle_for_edge": 0})
                
            elif pygame.mouse.get_pressed()[2]: # Right click
                check_collition_result, check_collition_index = check_collition(x, y)
                if check_collition_result == 1:
                    if check_collition_index in selected_circles:
                        continue
                    else:
                        path = []
                        circles[check_collition_index]["selected"] = 1
                        selected_circles.append(check_collition_index)
                        if len(selected_circles) > 2:
                            circles[selected_circles[0]]["selected"] = 0
                            selected_circles.pop(0)
                        pass

            if len(edge_of_circles) == 2:
                edges_coordinates = [edge[2] for edge in edges]
                if (edge_of_circles[0],edge_of_circles[1]) not in edges_coordinates and (edge_of_circles[1],edge_of_circles[0]) not in edges_coordinates:
                    edges.append([circles[edge_of_circles[0]]["coordinates"],circles[edge_of_circles[1]]["coordinates"], (edge_of_circles[0], edge_of_circles[1])])
                    path = []

                i = 0
                while i < 2:
                    circles[edge_of_circles[0]]["circle_for_edge"] = 0
                    edge_of_circles.pop(0)
                    i += 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen.fill(background_colour)
                circles = []
                edges = []
                selected_circles = []
                edge_of_circles = []
                path = []

            if event.key == pygame.K_RETURN:
                if len(selected_circles) < 2:
                    pass
                else:
                    graph = create_graph(edges)
                    ## TODO catch error if graph is disjointed
                    if bool(graph.graph) == False:
                        print("Graph is disjoined")
                    else:
                        path = dijkstras_algorithm(graph, selected_circles[0], selected_circles[1])