# PlaylistDJ
### Spotify Playlist Optimization Using Graph Theory

The idea for this project was to take a Spotify playlist and order the songs in an optimal order for listening.
The end result would be a playlist where each song was similar enough to the next, creating a smoother listening experience..
The transition between songs takes into account artist, genre, similar artists, and year released.
The Spotify API was used to get retrieve playlists and information about songs and artists.

### Collection

The Spotify API returns all HTTP responses as JSON format files.
Python can read these HTTP repsonses using the `requests` and `json` libraries.
Retrieving a playlist from Spotify's API requires authentication tokens that are not included in this project for security reasons.

The `JSON.txt` file used in this project is an example of Spotify's response to a request for a certain playlist.

### Processing

Firstly, the program takes the list of songs from `JSON.txt` and extracts all the songs Spotify ID numbers.
All further Spotify GET requests in this project use these ID's.

The list of all the songs' IDs can be found in Attached Files as `id.txt`.

A list is then created with each element in the list being a dictionary cotaining the song name, artist, year released, genres, related 
  artists, and an empty list which will be used to store the weights to each other song.
  
A formatted version of this song list can be found in Attached Files as `track_list.txt`.

### Weighting

Each song is given a weight in relation to each other song.
This weight is determined by several factors, namely the song's artist, genres, similar artists, and year released.
The maximum weight two songs can have to each other is 40 meaning they have nothing in common (this is stored as NONE in the program).
The lower a song's weight, the more similar they are. 
A song will have a weight of NONE with itself.

Each song's weight is calculated in relation to each other song and stored in the weights list.

The weight's of each song to each other song can be seen in Attached Files under `weights.txt`.

### Graping

Once the weights are calculated the songs are transferred from the list to a Graph class.
The Graph class contains a set of all vertices (songs) and a dictionary of all edges (weights).
The graph is initially undirected so these edges go both ways between vertices.

### Prim's Algortihm

Prim's Algorithm was used to create a minimum spanning tree of the data from an arbitrarily picked first song.

Here's a hand drawn representation of the minimum spanning tree.
![Minimum Spanning Tree](Attached%20Files/tree.jpg)

The algorithm returns a dictionary with every song being a key and the value associated is the song that points to it.

The child-parent dictionary can be see in Attached Files under `path.txt`.

An additional dictionary is created reversing the order of the previous.
This dictionary has every song as a key and the value associated is a list of any songs that it points to.

The parent-children dictionary can be seen in Attached Files under `graph_dict.txt`.

### Traversing

This minimum spanning tree is traversed with a custom Depth First Search algorithm.
A usual depth first search algorithm goes as deep as possible on a branch before exploring other branches.

This custom DFS algorithm skips every other vertex on a branch on its way down.
This is done so that on the way back up that branch is can collect those previosuly skipped vertices.

In the context of this project, the algorithm explores a branch of similarly related songs leaving behind songs 
  to traverse back through before going down another branch.
This ensures that no matter where you are in the tree, the current song is at most only two connection away from 
  the previous and next songs.

### Results

The final output of this program on the playlist can be seen in Attached Files under `results.txt`.
