import json
import requests
from collections import defaultdict

# Takes artist and returns top 10 related artists
def getRelated(id):
    relatedArtists = []

    response = json.loads((requests.get('https://api.spotify.com/v1/artists/' + id + '/related-artists')).text[:])
    
#   The JSON file is a dictionary
#   The key "artists" contains a dictionary about the related artist
#   The key "name" contains the name of all the artists as a string
    for key1, value1 in response.items():
        for x in range(10):
            for key2, value2 in value1[x].items():
                if key2 == "name":
                    relatedArtists.append(value2)
    
    return(relatedArtists)
  
# Takes artist and returns list of genres
def getGenres(id):
    genres = []

    response = json.loads((requests.get('https://api.spotify.com/v1/artists/' + id)).text[:])

#   The JSON file is a dictionary
#   The key "genres" contains a list of genres of an artist
    for key1, value1 in response.items():
        if key1 == "genres":
            for x in value1:
                genres.append(x)
    
    return(genres)
    
# Takes song and returns artist id    
def getArtistId(id):
    artistId = ""
    
    response = json.loads((requests.get('https://api.spotify.com/v1/tracks/' + id)).text[:])

#   The JSON file is a dictionary
#   The key "artists" contains a dictionary about the artist
#   The key "id" contains the artist ID as a string
    for key1, value1 in response.items():
        if key1 == "artists":
            for key2, value2 in value1[0].items():
                if key2 == "id":
                    artistId = value2
                    
    return(artistId)
   
# Takes song and returns artist name
def getArtistName(id):
    name = ""
    
    response = json.loads((requests.get('https://api.spotify.com/v1/tracks/' + id)).text[:])
    
#   The JSON file is a dictionary
#   The key "artists" contains a dictionary about the artist
#   The key "name" contains the name if the artist as a string
    for key1, value1 in response.items():
        if key1 == "artists":
            for key2, value2 in value1[0].items():
                if key2 == "name":
                    name = value2
                    
    return(name)
 
# Takes song and returns name
def getTrackName(id):
    name = ""
    
    response = json.loads((requests.get('https://api.spotify.com/v1/tracks/' + id)).text[:])
    
#   The JSON file is a dictionary
#   The key "name" contains a the name of the song as a string
    for key1, value1 in response.items():
        if key1 == "name":
            name = value1
            
    return(name)
 
# Takes song and returns album id
def getAlbumId(id):
    albumId = ""
    
    response = json.loads((requests.get('https://api.spotify.com/v1/tracks/' + id)).text[:])
    
#   The JSON file is a dictionary
#   The key "album" contains a dictionary about the album
#   The key "id" contains the album ID as a string
    for key1, value1 in response.items():
        if key1 == "album":
            for key2, value2 in value1.items():
                if key2 == "id":
                    albumId = value2
                    
    return(albumId)

# Takes album and returns release year    
def getYear(id):
    year = ""
    
    response = json.loads((requests.get('https://api.spotify.com/v1/albums/' + id)).text[:])
    
#   The JSON file is a dictionary
#   The key "release_date" contains the year as a string
    for key1, value1 in response.items():
        if key1 == "release_date":
            year = value1
            
    return(year[:4])

# Class graph with: set of vertices (no repeats)
#                   dictionary of lists of edges (key = start, value = list of ends) 
#                   dictionary of weights (key = tuple, value = weight)
#
# It has two methods: add_vertex- adds a vertex to the graph
#                     add_edge- adds an edge to the graph in both directions and adds the weight of the graph
#                               from either side
class Graph:
  def __init__(self):
    self.vertices = set()
    self.edges = defaultdict(list)
    self.weights = {}

  def add_vertex(self, value):
    self.vertices.add(value)

  def add_edge(self, from_vertex, to_vertex, weight):
    self.edges[from_vertex].append(to_vertex)
    self.edges[to_vertex].append(from_vertex)
    self.weights[(from_vertex, to_vertex)] = weight
    self.weights[(to_vertex, from_vertex)] = weight

# Prims algorithm
# Runs through the graph and creates a minimum spanning tree from a selected vertex
# Returns a dictionary called "path" that contains a dictionary with kids as keys, and parents as values
def prims(graph, initial):
    visited = {initial: 0}
    path = {}

    vertices = set(graph.vertices)
    
    while vertices: 
        min_vert = None
        for vertex in vertices:
            if vertex in visited:
                if min_vert is None:
                    min_vert = vertex
                elif visited[vertex] < visited[min_vert]:
                    min_vert = vertex

        if min_vert is None:
            break

        vertices.remove(min_vert)
        
        for vertex in list(visited):
            if vertex not in vertices:
                for kid in graph.edges[vertex]:                    
                    if kid in vertices:
                        
                        weight = graph.weights[(vertex, kid)] 
                        if kid not in visited or weight < visited[kid]:
                            visited[kid] = weight
                            path[kid] = vertex
                            

    return path
    
# DFS that hops down the roots of the tree and skips back to the top
# Checks to see if child's child exists, if so calls DFS on grandchild and prints first child after all grandchildren
def dfs1(graph, start, visited):
    print(start)
    visited.append(start)
    for vertex in graph[start]:
        if vertex not in visited:
            if graph[vertex]:
                for kid in graph[vertex]:
                    dfs1(graph, kid, visited)
                print(vertex)
            else:
                dfs1(graph, vertex, visited)

# Dummy function for DFS, includes an empty list outside the recursive function                
def dfs(graph, start):
    visited = []
    dfs1(graph, start, visited)
    
def main():

#   List of all the song ID's to parse through to get the data
    idList = []
#   List of dictioinaries about each song
    songList = []

#   Code.txt is the raw JSON output from the Spotify API
    f = open("JSON.txt")
    response = json.loads(f.read())

#   Takes list of tracks and creates list of ids
    for key1, value1 in response.items():
        if key1 == "items":
            for x in value1:
                for key2, value2 in x.items():
                    if key2 == "track":
                        for key3, value3 in value2.items():
                            if key3 == "id":
                                idList.append(value3)
                                
    print(idList)

#   Takes id list and returns list of dictionaries
#   Each dictionary contains data for each individual song:
#   Song NAME, ARTIST, GENRES, RELATED_ARTISTS, YEAR
#   Dictionary also has a list of the weights to all other songs                           
    counter = 1                          
    for x in idList:
        print(counter)
        tName = getTrackName(x)
        aName = getArtistName(x)
        albumId = getAlbumId(x)
        year = getYear(albumId)
        print(aName + ": " + tName + " (" + year + ") ")
        artistId = getArtistId(x)
        genres = getGenres(artistId)
        print(genres)
        related_artists = getRelated(artistId)
        print(related_artists)
        print("\n")
        
        songList.append({'song': tName , 'artist': aName , 'year': year , 'genres': genres , 'related_artists': related_artists , 'weights': []})
        
        counter+=1
                    
#   This calculates the weights from one song to all other songs
#   WEIGHT (Total 40 pts.)
#   Genre: 10 pts.                    \ If the artist is the same, these will always be the same
#   Related Artists: 20 pts.          |
#   Year Released: 10 pts.
    for track in songList:
        for other in songList:
            if track["song"] != other["song"]:
                weight = 40
                
#               If artist is the same, 30 pts. is taken off the top, and genres and related artists are skipped                
                if track["artist"] == other["artist"]:
                    weight -= 30
                else:  
                    weight_counter = 0
                    for g in track["genres"]:
                        if g in other["genres"]:
                            if weight_counter < 10:
                                weight_counter +=1
                    weight -= weight_counter
                    
#                   Index of artist in the other's list impacts the weight, 
#                   the closer to #1 the more the weight is lessened                    
                    if other["artist"] in track["related_artists"]:
                        weight -= 10 - (track["related_artists"].index(other["artist"]))
                    
                    if track["artist"] in other["related_artists"]:
                        weight -= 10 - (other["related_artists"].index(track["artist"]))
                
#               Year released is only a factor if genre and related artists changed the weight,
#               If this wasn't the case, all songs would have weights and that would slow down the algorithm
#               This helps make the tree a little more sparse considering all vertices could be connected                        
                if weight != 40:
                    
                    diff = abs(int(track["year"]) - int(other["year"]))
                    if diff <= 5:
                        weight -= diff*2
    
                    track["weights"].append(weight)
                    
#               If the weight is still 40 pts. after all that, it is set to None                
                else:
                    track["weights"].append(None)
                    
#           The weight between a song and itself is None
            else:
                track["weights"].append(None)
                
    print("\n")
          
    length = len(songList)
    
#   Takes songs and weights and inputs them into a graph class
    graph = Graph()
    
    for x in range(length-1):
        graph.add_vertex(songList[x]["song"])
        for y in range(x+1, length):
            if songList[x]["weights"][y] != None:
                graph.add_edge(songList[x]["song"], songList[y]["song"], songList[x]["weights"][y])               

    print(graph.edges)
    print("\n")
    print(graph.weights)
                
#   Runs Prim's Algorithm on graph                
    path = prims(graph, songList[0]["song"]) 
    
    print(path)
 
#   Recreates the dictionary so that each vertex is a key, and each value is a list of its kids
    graphDict = {}
    graphDict[songList[0]["song"]] = []

    for key, value in path.items():
        graphDict[key] = []
    
    for key, value in path.items():
        graphDict[value].append(key)
    
    print(graphDict)    
    print("\n")   

#   Custom DFS prints out order of vertices it visits   
    dfs(graphDict, songList[0]["song"])
    
main()
