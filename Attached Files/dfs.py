graph= {'A': set(['C', 'E', 'F']),
        'B': set(['G']),
        'C': set(['D', 'H']),
        'D': set(['L']),
        'E': set([]),
        'F': set(['B']),
        'G': set(['I']),
        'H': set(['J']),
        'I': set([]),
        'J': set(['K', 'M']),
        'K': set([]),
        'L': set([]),
        'M': set(['N']),
        'N': set([])}
      
def dfs1(start, visited):
    print(start)
    visited.append(start)
    for node in graph[start]:
        if node not in visited:
            if graph[node]:
                for vertex in graph[node]:
                    dfs1(vertex, visited)
                print(node)
            else:
                dfs1(node, visited)

def dfs(start):
    visited = []
    dfs1(start, visited)

dfs('A')
                   
