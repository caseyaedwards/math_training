# Images

* [graph-anatomy.svg](graph-anatomy.svg): the parts of a graph: vertex, two-way edge, directed edge, weighted edge, and in-degree and out-degree on one vertex.
* [dependency-dag.svg](dependency-dag.svg): the nine-service dependency DAG drawn in five layers, arrows from each service to what it needs.
* [adjacency-list-vs-matrix.svg](adjacency-list-vs-matrix.svg): one four-vertex graph shown as a picture, an adjacency list and an adjacency matrix.
* [kahn-steps.svg](kahn-steps.svg): five frames of the Kahn algorithm on the four-vertex graph, with remaining counts and the queue in each frame.
* [dependency-cycle.svg](dependency-cycle.svg): the services after the bad edge db needs web, with the cycle api, auth, db, web in the accent color.
* [dfs-three-colors.svg](dfs-three-colors.svg): the three-color DFS at the moment it finds the back edge web to api, with walk order numbers.
* [region-dijkstra.svg](region-dijkstra.svg): seven regions with link latencies and the lowest-latency route us-east, eu-west, ap-south highlighted.
* [dijkstra-ripple.svg](dijkstra-ripple.svg): the seven regions on a distance number line, numbered in the order Dijkstra finishes them.
* [bfs-rings.svg](bfs-rings.svg): BFS from us-east drawn as rings of equal hop count, with the BFS tree in the accent color.
* [blast-radius-db.svg](blast-radius-db.svg): the services shaded by whether they transitively need db, with the hop distance from db.
* [fan-in-vs-blast.svg](fan-in-vs-blast.svg): paired bars of in-degree and blast radius for every service.
* [articulation-points.svg](articulation-points.svg): the service graph as two-way links with the articulation points web, api and auth highlighted.
