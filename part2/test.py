import math
import sys
#Fair
#Function to add cities to dictionary
def add_to_map(route_problem,city,latitude,longitude):
    route_problem[city]={}
    route_problem[city]["Latitude"]=float(latitude)
    route_problem[city]["Longitude"]=float(longitude)
    route_problem[city]["Segment"]={}
    route_problem[city]["Path"]=""
    route_problem[city]["Total_Distance"]=0
    route_problem[city]["Total_Time"]=0
    route_problem[city]["Visited"]=0
    route_problem[city]["Lat_Visited"]=0
    route_problem[city]["Cost"]=0
    route_problem[city]["Distance_Coordinate"]=0
    route_problem[city]["Heuristic_Distance"]=0
    route_problem[city]["Heuristic"]=0
    route_problem[city]["Heuristic_Cost"]=0
    route_problem[city]["Total_Segment"]=0
    
#If latitude of goal city is unknown, assigning a latitude to it and assigning distance from    
# city to subtract from. Only to be called if goal city lat is 0
# Heuristic dist= great circle dist to nearest city-dist travelled between this city and goal city
#If negative then 0
def lat_long_dist(route_problem,cities):
    lat_goal=0
    lat_fringe=[cities]
    lat_dist=[0]
    distance=0
    lat_goal_city=""
    route_problem[cities]["Lat_Visited"]=1
    while (lat_goal==0 and len(lat_fringe)>0) or (len(lat_fringe)>0 and lat_goal==1 and distance>min(lat_dist)):                        
        min_lat_dist_index = lat_dist.index(min(lat_dist))
        lat_current_city= lat_fringe.pop(min_lat_dist_index)                
        del(lat_dist[min_lat_dist_index])
        for cities_segment in route_problem[lat_current_city]["Segment"]:
            if route_problem[cities_segment]["Lat_Visited"]==1:
                if route_problem[cities_segment]["Distance_Coordinate"]>route_problem[lat_current_city]["Segment"][cities_segment]["Length"] + route_problem[lat_current_city]["Distance_Coordinate"]:
                    route_problem[cities_segment]["Distance_Coordinate"]=route_problem[lat_current_city]["Segment"][cities_segment]["Length"] + route_problem[lat_current_city]["Distance_Coordinate"]
                    if cities_segment !=lat_goal_city:
                       lat_dist[lat_fringe.index(cities_segment)]=route_problem[cities_segment]["Distance_Coordinate"]
                    else:
                       distance= route_problem[cities_segment]["Distance_Coordinate"]
            if route_problem[cities_segment]["Lat_Visited"]==0:
                route_problem[cities_segment]["Lat_Visited"]=1
                route_problem[cities_segment]["Distance_Coordinate"]=route_problem[lat_current_city]["Segment"][cities_segment]["Length"] + route_problem[lat_current_city]["Distance_Coordinate"]
                if route_problem[cities_segment]["Latitude"]>0:
                    if lat_goal==0:
                       lat_goal=1
                       lat_goal_city=cities_segment
                       distance=route_problem[lat_current_city]["Segment"][cities_segment]["Length"] + route_problem[lat_current_city]["Distance_Coordinate"]
                    elif distance>route_problem[lat_current_city]["Segment"][cities_segment]["Length"] + route_problem[lat_current_city]["Distance_Coordinate"]:           
                       distance=route_problem[lat_current_city]["Segment"][cities_segment]["Length"] + route_problem[lat_current_city]["Distance_Coordinate"]
                       lat_goal_city=cities_segment                                
                else:
                    lat_fringe.append(cities_segment)
                    lat_dist.append(route_problem[cities_segment]["Distance_Coordinate"])                                
    route_problem[cities]["Latitude"]=route_problem[lat_goal_city]["Latitude"]
    route_problem[cities]["Longitude"]=route_problem[lat_goal_city]["Longitude"]
    route_problem[cities]["Distance_Coordinate"]=distance
    
#Calculating Great Circle distance    
#Only if current city latitude is known
#For unknown latitude for a city, previous city heuristic distance from route map-dist between previous city
#And current city. If negative, then 0
def heuristic(route_problem,current_city,goal_city,cost_function):    
    #https://en.wikipedia.org/wiki/Great-circle_distance
    Lat1=(route_problem[current_city]["Latitude"])*math.pi/180
    Lon1=(route_problem[current_city]["Longitude"])*math.pi/180
    Lat2=(route_problem[goal_city]["Latitude"])*math.pi/180
    Lon2=(route_problem[goal_city]["Longitude"])*math.pi/180    
    del_Lon = (Lon2-Lon1)
    del_sigma = math.acos(math.sin(Lat1)*math.sin(Lat2) + math.cos(Lat1)*math.cos(Lat2)*math.cos(del_Lon))
    distance=0.5*3959*del_sigma - route_problem[goal_city]["Distance_Coordinate"]  #3959 is radius of earth
    return distance
    #Returning value based on cost function



#Main    
route_problem={}
max_speed_limit=0
max_segment_length=0

#Opening city gps file and adding to the dictionary
f=open("city-gps.txt")
for line in f:
    add_to_map(route_problem, line.split()[0] ,float(line.split()[1]) , float(line.split()[2]))    
f.close()

#Opening road segments and adding to dictionary
f=open("road-segments.txt")
for line in f:
    if line.split()[0]==line.split()[1]:
        continue
    #If city 1 not found in dictionary, add to dictionary
    if line.split()[0] not in route_problem:
        add_to_map(route_problem, line.split()[0] ,0 , 0)        
    #If ends
    # if city 2 not found in dictionary, add to dictionary
    if line.split()[1] not in route_problem:
        add_to_map(route_problem, line.split()[1] ,0 , 0)
    #If ends
    #Add to city 1 key - length, speed limit and highway    
    route_problem[line.split()[0]]["Segment"][line.split()[1]]={}
    route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"]=float(line.split()[2])
    #Handling Missing Speed and 0 speed
    if len(line.split())==5 and float(line.split()[3])>0:
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]=float(line.split()[3])
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["Highway"]=line.split()[4]
    else:
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]=40
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["Highway"]=line.split()[3]
    route_problem[line.split()[0]]["Segment"][line.split()[1]]["Time"]=route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"]/route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]
    route_problem[line.split()[0]]["Segment"][line.split()[1]]["Segment"]=1
    #Add to city 2 key    
    route_problem[line.split()[1]]["Segment"][line.split()[0]]={}
    route_problem[line.split()[1]]["Segment"][line.split()[0]]["Length"]=float(line.split()[2])
    #Handling missing speed and 0 speed
    if len(line.split())==5 and float(line.split()[3])>0:
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["Speed_Limit"]=float(line.split()[3])
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["Highway"]=line.split()[4]
    else:
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["Speed_Limit"]=40  
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["Highway"]=line.split()[3]
    route_problem[line.split()[1]]["Segment"][line.split()[0]]["Time"]=route_problem[line.split()[1]]["Segment"][line.split()[0]]["Length"]/route_problem[line.split()[1]]["Segment"][line.split()[0]]["Speed_Limit"]
    route_problem[line.split()[1]]["Segment"][line.split()[0]]["Segment"]=1
    #Updating max_segment_length 
    if route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"] > max_segment_length:
        max_segment_length=route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"]
    #updating max_speed_limit    
    if route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]>max_speed_limit:
        max_speed_limit=route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]
        
f.close()



#Routing Problem

#Traversing from Initial City to Goal City
goal=0
initial_city= sys.argv[1]
goal_city= sys.argv[2]
if route_problem[goal_city]["Latitude"]==0:
   lat_long_dist(route_problem,goal_city)
routing_algorithm= sys.argv[3]
cost_function= sys.argv[4]

#Defining cost factor
if cost_function=="distance":
        cost_factor= 1
elif cost_function=="time":
        cost_factor=max_speed_limit
elif cost_function=="segments":
        cost_factor= math.ceil(max_segment_length)
        
route_problem[initial_city]["Visited"]=1
route_problem[initial_city]["Path"] = initial_city
#current_city=initial_city
fringe=[initial_city]
if routing_algorithm in ["uniform","bfs","dfs"]:
   cost=[0]
if routing_algorithm=="astar":
   heuristic_cost=[0]
# Based on cost function, specific key to be accessed
if cost_function=="distance":
    key="Length"
elif cost_function=="segments":
    key="Segment"
elif cost_function=="time":
    key="Time"

while (len(fringe)>0 and goal ==0) or (len(fringe)>0 and goal ==1 and routing_algorithm=="uniform" and route_problem[goal_city]["Cost"]>min(cost))   or (len(fringe)>0 and goal ==1 and routing_algorithm=="astar" and route_problem[goal_city]["Heuristic_Cost"]>min(heuristic_cost)):
   #Getting min index
   ##https://stackoverflow.com/questions/11237630/finding-the-index-value-of-the-smallest-number-in-a-list
   #min_cost_index=cost.index(min(cost))
   #Based on routing algo, the index of fringe that needs to be popped out
   if routing_algorithm=="bfs":
       current_city=fringe.pop(0)
       del(cost[0])
   elif routing_algorithm=="dfs":
       current_city=fringe.pop()
       del(cost[len(cost)-1])
   elif routing_algorithm=="uniform":
       min_cost_index=cost.index(min(cost))
       current_city=fringe.pop(min_cost_index)
       del(cost[min_cost_index])
   elif routing_algorithm=="astar":
       min_heuristic_cost_index=heuristic_cost.index(min(heuristic_cost))
       current_city=fringe.pop(min_heuristic_cost_index)       
       del(heuristic_cost[min_heuristic_cost_index])
   
   
   for cities in route_problem[current_city]["Segment"]:
       if route_problem[cities]["Visited"]==1 and routing_algorithm in ["uniform","astar"]:
          if  route_problem[cities]["Cost"]>route_problem[current_city]["Segment"][cities][key] +route_problem[current_city]["Cost"]:
              route_problem[cities]["Path"]= route_problem[current_city]["Path"] + " " + cities
              #Total Distance
              route_problem[cities]["Total_Distance"]= \
              route_problem[current_city]["Segment"][cities]["Length"] + \
              route_problem[current_city]["Total_Distance"]
              #Total Time
              route_problem[cities]["Total_Time"]= \
              route_problem[current_city]["Segment"][cities]["Time"] + \
              route_problem[current_city]["Total_Time"]
              #Total Segments
              route_problem[cities]["Total_Segment"]= \
              route_problem[current_city]["Segment"][cities]["Segment"] + \
              route_problem[current_city]["Total_Segment"]
              #Total Cost
              route_problem[cities]["Cost"]= \
              route_problem[current_city]["Segment"][cities][key] + \
              route_problem[current_city]["Cost"]
              #If latitude=0, comparing heuristic and if greater, updating
              if routing_algorithm=="astar":
                  if route_problem[cities]["Latitude"]==0:
                      route_problem[cities]["Heuristic"]= max(route_problem[cities]["Heuristic_Distance"],route_problem[current_city]["Heuristic_Distance"]- route_problem[current_city]["Segment"][cities]["Length"])/cost_factor
                          
              #Updating heuristic_cost if astar
              if routing_algorithm=="astar":
                  route_problem[cities]["Heuristic_Cost"]= route_problem[cities]["Heuristic"] + route_problem[cities]["Cost"]
              #Updating cost in cost array and heuristic cost in heuristic cost array
              if cities !=goal_city and cities not in fringe and routing_algorithm=="astar":
                 fringe.append(cities) 
                 heuristic_cost.append(route_problem[cities]["Heuristic_Cost"])                 
              if cities !=goal_city:
                 if routing_algorithm=="uniform": 
                     cost[fringe.index(cities)]=route_problem[cities]["Cost"]
                 if routing_algorithm=="astar":
                     heuristic_cost[fringe.index(cities)]=route_problem[cities]["Heuristic_Cost"]
                     
       #When Visited=0              
       if (route_problem[cities]["Visited"]==0):
          if cities==goal_city:              
              goal=1              
          else:
              fringe.append(cities)
          route_problem[cities]["Visited"]=1
          route_problem[cities]["Path"]= route_problem[current_city]["Path"] + " " + cities
          #Calculating and updating Heuristic
          if routing_algorithm=="astar":
              if route_problem[cities]["Latitude"]>0:
                 route_problem[cities]["Heuristic_Distance"]= heuristic(route_problem,cities,goal_city,cost_function)
                 if route_problem[cities]["Heuristic_Distance"] <0:
                     route_problem[cities]["Heuristic_Distance"]=0
                 route_problem[cities]["Heuristic"] = route_problem[cities]["Heuristic_Distance"]/cost_factor
              else:
                 route_problem[cities]["Heuristic_Distance"]=route_problem[current_city]["Heuristic_Distance"] -route_problem[current_city]["Segment"][cities]["Length"]
                 if route_problem[cities]["Heuristic_Distance"] <0:
                     route_problem[cities]["Heuristic_Distance"]=0
                 route_problem[cities]["Heuristic"] = route_problem[cities]["Heuristic_Distance"]/cost_factor
          #Total Distance
          route_problem[cities]["Total_Distance"]= \
          route_problem[current_city]["Segment"][cities]["Length"] + \
          route_problem[current_city]["Total_Distance"]
          #Total Time
          route_problem[cities]["Total_Time"]= \
          route_problem[current_city]["Segment"][cities]["Time"] + \
          route_problem[current_city]["Total_Time"]
          #Total Segments
          route_problem[cities]["Total_Segment"]= \
          route_problem[current_city]["Segment"][cities]["Segment"] + \
          route_problem[current_city]["Total_Segment"]
          #Total Cost
          route_problem[cities]["Cost"]= \
          route_problem[current_city]["Segment"][cities][key] + \
          route_problem[current_city]["Cost"]
          #Heuristic + cost
          if routing_algorithm=="astar":
              route_problem[cities]["Heuristic_Cost"]= route_problem[cities]["Heuristic"] + route_problem[cities]["Cost"]
          #Appending the cost array
          if cities !=goal_city and routing_algorithm in ["uniform","bfs","dfs"]:
              cost.append(route_problem[cities]["Cost"])
          if cities !=goal_city and routing_algorithm=="astar":
              heuristic_cost.append(route_problem[cities]["Heuristic_Cost"])
          
                  
#route_problem
if goal==0 and initial_city!=goal_city:
    print("Sorry, No Path Found")
elif initial_city==goal_city:
    print("Please input different cities")
else:
    print(str(route_problem[goal_city]["Total_Distance"])+" "+str(route_problem[goal_city]["Total_Time"]) + \
          " " + route_problem[goal_city]["Path"])    