# Shortest Path

This application was developed as part of the course "Mathematical Modeling" by Dr. Rockefeller from the University of Koblenz-Landau, Germany.
The task was to determine the shortest path indoors by means of a graph. The application was written using python and the A* and Jump Point Search algorithms were used to solve the problem.


# A* algorithm
Solves shortest path problem between two nodes. It is a generalization of the dijkstra algorithm. A heuristic is used to find the goal faster.

Every node gets a g-score and a f-score. The g-score is the length from start to the current node. The f-score ist the estimated length from start to the end point using the current node: f(node) = g(node)+h(node). The node with the lowest f-score is choosen.

# Jump Point Search algorithm
Is an improvement of A* by making the cost for parallel paths equal. The algorithm searches larg areas quicker and marks interesting points for search. In the beginning it is necessary to dearch the starting point beforehand to ensure "safe" beginning. 
From the starting point a search is started in all vertical, horizontal directions and then in all diagonal directions, then the list of interesting points is used as in A* by choosing a closest point.

# Our Approach

Our approach does not use graphs as in the original problem, but uses a Uniform grid as a basis. The idea behind this was that we are not limited in terms of room plans, but can use a simple image as input. 

To be able to use any image we liked, we had to apply some image processing algorithm's.
  - if the image is in RGB color space, it is converted to a grayscale image
  - then a the threshold is determined with the otsu method
  - with the threshold the image is binarized in a black and white image
  - if necessary erosion is applied for a cleaner look

The binarized image is used as the basis for the uniform grid. Pixel[0][0] equals Grid Cell[0][0]. The pixel value (0 or 1) is entered for the grid value. This results in a grid that represents the input image (depending on the resolution and preprocessing, slight deviations or inaccuracies may occur).

Each grid cell is a node with the value 0 for free space and 1 for walls or obstacles. Stepping horizontally or vertically through the grid has the cost of 1, going diagonally square(2).
In this approach the start and end point can be choosen freely.

# Results

![ScreenShot](/resources/floor_plan_a.png) 
![ScreenShot](/results/grid.png)
![ScreenShot](/results/prog1.png)

The floor plan was first preprocessed and than converted into a grid and the search algorithm was applied (in this example A*)

It also works with more complex plans and a higher grid resolution:

![ScreenShot](/resources/floor_plan_c.png) 
![ScreenShot](/results/res3.png)

Due to the resolution, the labeling of the plan could not be removed by the erosion algorithm, otherwise wall information would also have been lost.

The approach also works with mazes:

![ScreenShot](/resources/maze_c.png) 
![ScreenShot](/results/res6.png)
