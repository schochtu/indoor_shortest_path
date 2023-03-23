# Shortest Path

This application was developed as part of the course "Mathematical Modeling" by Dr. Rockefeller from the University of Koblenz-Landau, Germany.
The task was to determine the shortest path indoors by means of a graph. The application was written using python and the A* and Jump Point Search algorithms were used to solve the problem.


# A* algorithm
Solves shortest path problem between two nodes. It is a generalization of the dijkstra algorithm. A heuristic is used to find the goal faster.

Every node gets a g-score and a f-score. The g-score is the length from start to the current node. The f-score ist the estimated length from start to the end point using the current node: f(node) = g(node)+h(node). The node with the lowest f-score is choosen.

# Jump Point Search algorithm
