<h1> Problem1- The 2021 Puzzle </h1>

<h3> Files to Reffer : solver2021.py<h3>

<h3> Problem Statement <h3>

Consider the 2021 puzzle, which is a lot like the 15-puzzle we talked about in class, but: (1) it has 25 tiles, so
there are no empty spots on the board (2) instead of moving a single tile into an open space, a move in this
puzzle consists of either (a) sliding an entire row of tiles left or right one space, with the left- or right-most
tile 'wrapping around' to the other side of the board, (b) sliding an entire column of tiles up or down one
space, with the top- or bottom-most tile 'wrapping around' to the other side of the board, (c) rotating the
outer 'ring' of tiles either clockwise or counterclockwise, or (d) rotating the inner ring either clockwise or
counterclockwise.

The goal of the puzzle is to find a short sequence of moves that restores the canonical configuration (on the
left above) given an initial board configuration. 

where input-board-filename is a text file containing a board configuration (we have provided an example).
You'll need to complete the function called solve(), which should return a list of valid moves. The moves
should be encoded as strings in the following way:

1. For sliding rows, R (right) or L (left), followed by the row number indicating the row to move left or
right. The row numbers range from 1-5.

2. For sliding columns, U (up) or D (down), followed by the column number indicating the column to move
up or down. The column numbers range from 1-5.

3. For rotations, I (inner) or O (outer), followed by whether the rotation is clockwise (c) or counterclock-
wise (cc).

For example, the above diagram performs the moves L3 (slide row 3 left), D3 (slide column 3 down), Occ
(outer counterclockwise), and Ic (inner clockwise).

<h3> Abstraction </h3>

1. State Space: All possible arrangements of board with numbers 1 to 25.
2. Initial State: Any arrangement of board with numbers 1 to 25 on it.
3. Successor Function: Sliding the rows left,Sliding the rows right,Sliding the columns Up,Sliding the columns Down,Inner Rotation clockwise,Inner Rotation counter-clockwise,Outer Rotation clockwise,Outer Rotation counter-clockwise.
Set of valid moves {'R1','R2','R3','R4','R5','L1','L2','L3','L4','L5','U1','U2','U3','U4','U5','D1','D2','D3','D4','D5','Oc','Ic','Occ','Icc'}
4. Goal State: The correct arrengement of the numbers 1 to 25 on the board with the least possible number of moves.	
5. Cost: Increment by 1 for each action performed.
6. Heuristic: The distance between the tile and its position in the goal state(Manhattan distance).

In this problem, given a board of numbers from 1 to 25 which are placed in a random order, we need to find a sequence of moves that will restore the canonical configuration of the board(numbers in correct order).
Our approach to this problem was - Initially, we consider all possible successors to the initial state and calculate the f-score for each of the child. This f-score is given by the sum of h-score(heuristic) and step cost(no. of steps) taken to reach the particular child. Then we add these child nodes, its f-scores, the sequence of moves followed to reach that child node into the fringe. Our fringe is a priority queue and the highest priority is given to the child which has the least f-score. Next, we pop this child with least f-score and expand this child node and start entering its child nodes into the fringe. This process is continued until we find our goal state.

<h3> Our Approach to the solution: </h3>

We implemented Uniform Cost Search with Heuristic function which is A*. 
We implemented the 'No.of misplaced tiles' as our heuristic. This heuristic is not admissible since it is over-estimating for all the boards( For example,
by using no.of misplaced tiles would calculate the number of misplaced tiles as 6 but the board can be solved in one step, then it is over-estimating) 
We finalized 'Manhattan Distance' as our heuristic which is also not admissible but performing better than the previous heuristic.	

<h3>Additional Questions:</h3>
Question 1: In this problem, what is the branching factor of the search tree?
Answer: The branching factor will be 24

Question 2: If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search?
Answer: The branching factor if we used BFS would be 
&sum;<sub>k=0</sub><sup>N</sup>24<sup>K</sup>



<h1> Problem2- Road Trip</h1>

<h3> Files to Reffer : route.py<h3>

<h3> Problem Statement <h3>

It's not too early to start planning a post-pandemic road trip! If you stop and think about it, finding the
shortest driving route between two distant places  say, one on the east coast and one on the west coast of
the U.S.  is extremely complicated. There are over 4 million miles of roads in the U.S. alone, and trying
all possible paths between two places would be nearly impossible. So how can mapping software like Google
Maps find routes nearly instantly? The answer is A* search!
We've prepared a dataset of major highway segments of the United States (and parts of southern Canada
and northern Mexico), including highway names, distances, and speed limits; you can visualize this as a
graph with nodes as towns and highway segments as edges. We've also prepared a dataset of cities and
towns with corresponding latitude-longitude positions. Your job is to find good driving directions between
pairs of cities given by the user.

where:
1. start-city and end-city are the cities we need a route between.
2. cost-function is one of:
     segments tries to find a route with the fewest number of road segments (i.e. edges of the graph).
     distance tries to find a route with the shortest total distance.
     time finds the fastest route, assuming one drives the speed limit.
     delivery finds the fastest route, in expectation, for a certain delivery driver. Whenever this
driver drives on a road with a speed limit ≥50 mph, there is a chance that a package will fall out
of their truck and be destroyed. They will have to drive to the end of that road, turn around,
return to the start city to get a replacement, then drive all the way back to where they were (they
won’t make the same mistake the second time they drive on that road).
Consequently, this mistake will add an extra 2 *(troad + ttrip) hours to their trip, where ttrip is the
time it took to get from the start city to the beginning of the road, and troad is the time it takes
to drive the length of the road segment.
For a road of length l miles, the probability p of this mistake happening is equal to tanh (l/1000)
if the speed limit is ≥ 50 mph, and 0 otherwise.1 This means that, in expectation, it will take
troad + p ·2(troad + ttrip) hours to drive on this road.

<h3> Abstraction </h3>

1. State Space : All valid cities which have a segment from a given city1
2. Initial State: Start city which is valid and present in road-segments.txt and city-gps.txt  
3. Successor Function: Traversing to all the adjacent cities from the initial city where there is a road segment between them.
4. Goal State: Reaching the End City
5. Cost: There are 4 cost functions: segments(route with fewer number of road segments), distance(route with shortest total distance), time(fastest route within the speed limit), delivery(if the speed limit between 2 cities is greater than or equal to 50 mph then there is a probablity of making a mistake which is given by tanh(l/1000 and total hours to drive would be t_road+p*2(t_road+t_trip) or probablity of mistake will be zero and time taken will be equal to t_road)
6. Heuristic: Great Circle Distance(To find the distance between any two points on the earth using Latitude and Longitude values)

<h3> Our Approach to the solution: </h3>

1.The data present in road-segments.txt and city-gps.txt is loaded into a single list which contains city,latititudes,longitudes,segments between the cities.
2.We implemented the A* algorithm where the heuristic function used is Great Circle Distance which is admissible as it finds the straight line distance between any two cities given their latitude and longitude values and the cost functions are segments(route with fewer number of road segments), distance(route with shortest total distance), time(fastest route within the speed limit), delivery(if the speed limit between 2 cities is greater than or equal to 50 mph then there is a probablity of making a mistake which is given by tanh(l/1000 and total hours to drive would be t_road+p*2(t_road+t_trip) or probablity of mistake will be zero and time taken will be equal to t_road).
3.Sucessor functions returns all the adjacent cities where there is a road segment from the current city. 
4.If the latitude,longitude values of the current are missing, then we considered the latitude,longitude values of the previous city.We calculate the Great Circle distance between those previous cities values and the latitude,longitude values of the goal city, then we add the segment distance to the Great Circle distance calculated previously.
5.For the cost function 'segments', we calculate the f-score=h-score+cost where ;f-score=(h-score/max_segment)+(total_segments) ;h-score= Great Circle Distance from current city to goal city max_segement = maximum number of segments for a city in the road-segments.txt ;total_segments= number of segments in the route taken to reach the city
6.For the cost function 'Time', we calculate the f-score=h-score+cost where ;f-score=(h-score/max_speed)+succesor_city ; h-score= Great Circle Distance from current city to goal city  max_speed=road segment with the maximum speed limit in road-segments.txt
7. For the cost function 'Distance', we calculate the f-score=h-score+cost ;f-score=h-score+distance to reach the current city from previous city ;h-score=Great Circle Distance from current city to goal city 
8. For the cost function 'Distance', we calculate the f-score=h-score+cost;f-score=(h-score/max_speed)+cost ;cost= t_road+(p*2*(t_road+t_trip))
