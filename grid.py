# Here goes anything that is related to searching
# the grid and determining the paths for the monsters
import heapq

# the change of the matrix coordinates depending on where you move
dir_dict = {
    'l': (0, -1),
    'r': (0, 1),
    'u': (-1, 0),
    'd': (1, 0)
}

reverse_dir_dict = {
    (0, -1): 'l',
    (0, 1): 'r',
    (-1, 0): 'u',
    (1, 0): 'd'
}


def a_star_search(graph, start, destiny, grid):
    """
    Finds the shortest path from start to destiny using A* search.
    Takes abs(i1-i2) + abs(j1-j2) as the heuristic function, where
    i and j define the blocks coordinates on the grid.
    If the start/destiny nodes are not in the graph, they are added with edges
    to their closest nodes
    :param graph: dict {{i, j): [((i0, j0), edge_weight, direction)]}
    :param start: (i, j)
    :param destiny: (i, j)
    :param grid: list of lists, 0 for walls, 1 otherwise
    :return: The direction in which the monster needs to move at that moment
    """
    print(start in graph.keys(), destiny in graph.keys())
    graph = add_to_graph(start, graph, grid)
    graph = add_to_graph(destiny, graph, grid)
    close_set = set(graph.keys())
    close_set.remove(start)
    min_dists = {
        start: (0, None)
        # node: (min dist, the direction to be taken from start for min dist)
    }

    # will save tuples (min_dist + heuristic, node)
    # python compares tuples position by position, that is helpful
    heap = []  # list will be treated as a priority queue
    prev_node = start
    while destiny in close_set:
        for edge in graph[prev_node]:
            if edge[0] in close_set:
                new_dist = min_dists[prev_node][0] + edge[1]
                old_dist = min_dists.get(edge[0], None)
                if old_dist is None or new_dist < old_dist[0]:
                    if prev_node == start:
                        new_dir = edge[2]
                    else:
                        new_dir = min_dists[prev_node][1]
                    min_dists[edge[0]] = (new_dist, new_dir)
                    heuristic = \
                        abs(edge[0][0]-destiny[0]) + abs(edge[0][1]-destiny[1])
                    heapq.heappush(heap, (new_dist + heuristic, edge[0]))
        while prev_node not in close_set:
            prev_node = heapq.heappop(heap)[1]
        close_set.remove(prev_node)

    return min_dists[destiny][1]


def get_graph(grid):
    """
    Creates a list representation of the undirected graph, where the nodes
    are all the points where pacman/monsters can turn 90 degrees
    :param grid: list of lists, representing all points on the original grid
        value is 0, if there is wall at that point, 1 otherwise
    :return: dict of nodes, keyed with the coordinate of the node(tuple).
        Value of each key is a list of tuples.
        Each tuple contains the key of a node that is connected to this node,
        length of the edge connecting them and the direction in which
        you have to move for reaching that node (u, d, l, r)
    """
    graph = {}
    directions = {}
    nodes = 0
    for i, line in enumerate(grid[1:-1]):
        for j, element in enumerate(line[1:-1]):
            if element == 0:
                continue
            up = grid[i][j+1]
            down = grid[i+2][j+1]
            left = grid[i+1][j]
            right = grid[i+1][j+2]
            if (up or down) and (left or right):
                graph[(i+1, j+1)] = []
                directions[(i+1, j+1)] = []
                if up:
                    directions[(i+1, j+1)].append('u')
                if down:
                    directions[(i+1, j+1)].append('d')
                if left:
                    directions[(i+1, j+1)].append('l')
                if right:
                    directions[(i+1, j+1)].append('r')
                nodes += 1

    for node in graph.keys():
        for direction in directions[node]:
            change = dir_dict[direction]
            next_node = node
            dist = 0
            while True:
                next_node = next_node[0] + change[0], next_node[1] + change[1]
                dist += 1
                if next_node in graph.keys():
                    break
            graph[node].append((next_node, dist, direction))

    return graph


def add_to_graph(block, graph, grid):
    """
    Finds the 2 nodes from the nodes that are closest to the the block and
    adds the block to the graph by connecting it to those nodes
    """
    if block in graph.keys():
        return graph

    if grid[block[0]][block[1]+1] == 1:
        direction = (0, 1)
    else:
        direction = (1, 0)

    close_nodes = [block, block]
    dist1, dist2 = 0, 0
    while close_nodes[0] not in graph.keys():
        close_nodes[0] = close_nodes[0][0]+direction[0], \
                         close_nodes[0][1]+direction[1]
        dist1 += 1
    while close_nodes[1] not in graph.keys():
        close_nodes[1] = close_nodes[1][0]-direction[0], \
                         close_nodes[1][1]-direction[1]
        dist2 += 1

    dir1 = reverse_dir_dict[direction]
    dir2 = reverse_dir_dict[(-direction[0], -direction[1])]
    graph[block] = [(close_nodes[0], dist1, dir1),
                    (close_nodes[1], dist2, dir2)]

    graph[close_nodes[0]].append((block, dist1, dir2))
    graph[close_nodes[1]].append((block, dist2, dir1))
    return graph


# test_graph = {
#     (0, 0): [((0, 2), 2, 'r'), ((1, 0), 1, 'd')],
#     (1, 0): [((1, 1), 1, 'r'), ((0, 0), 1, 'u')],
#     (1, 1): [((1, 2), 1, 'r'), ((1, 0), 1, 'l')],
#     (1, 2): [((0, 2), 1, 'u'), ((1, 1), 1, 'l')],
#     (0, 2): [((0, 1), 1, 'l'), ((1, 2), 1, 'd')]
# }
#
# print(a_star_search(test_graph, (0, 0), (1, 1)))
