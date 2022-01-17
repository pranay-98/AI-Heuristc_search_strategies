#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: "Pranay Reddy / pdasari, Vamsee Krishna Sai / vnarams, Anil Ravi/ anilravi "
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import heapq
import math


def get_map():

    route_problem={}
    max_segment=0
    max_speed=0
    

    f=open("city-gps.txt")
    for line in f:
        add_map(route_problem, line.split()[0] ,float(line.split()[1]) , float(line.split()[2]))    
    f.close()

    
    f=open("road-segments.txt")
    for line in f:
        p=0.0
        if line.split()[0]==line.split()[1]:
            continue
        if line.split()[0] not in route_problem:
            add_map(route_problem, line.split()[0] ,0 , 0)    
        if line.split()[1] not in route_problem:
            add_map(route_problem, line.split()[1] ,0 , 0)   
        route_problem[line.split()[0]]["Segment"][line.split()[1]]={}
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"]=float(line.split()[2])
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]=float(line.split()[3])
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["Highway"]=line.split()[4]
        
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["Time"]=route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"]/route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]

        if route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]>=50:
            p=float(math.tanh(route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"]/1000))
            route_problem[line.split()[0]]["Segment"][line.split()[1]]["p_mistake"]=p
        route_problem[line.split()[0]]["Segment"][line.split()[1]]["p_mistake"]=p

        route_problem[line.split()[1]]["Segment"][line.split()[0]]={}
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["Length"]=float(line.split()[2])
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["Speed_Limit"]=float(line.split()[3])
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["Highway"]=line.split()[4]
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["Time"]=route_problem[line.split()[1]]["Segment"][line.split()[0]]["Length"]/route_problem[line.split()[1]]["Segment"][line.split()[0]]["Speed_Limit"]
        route_problem[line.split()[1]]["Segment"][line.split()[0]]["p_mistake"]=p

        if route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"] > max_segment:
            max_segment=route_problem[line.split()[0]]["Segment"][line.split()[1]]["Length"]
  
        if route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]>max_speed:
            max_speed=route_problem[line.split()[0]]["Segment"][line.split()[1]]["Speed_Limit"]
            
    f.close()

    return route_problem,max_segment,max_speed

def heuristic(route_problem,successor_cities,goal_city):
    if route_problem[successor_cities]["Latitude"]==0:
        return 0
# below code is sourced from the following link 
#https://python.plainenglish.io/calculating-great-circle-distances-in-python-cf98f64c1ea0
    Lat1=(route_problem[successor_cities]["Latitude"])*math.pi/180
    Lon1=(route_problem[successor_cities]["Longitude"])*math.pi/180
    Lat2=(route_problem[goal_city]["Latitude"])*math.pi/180
    Lon2=(route_problem[goal_city]["Longitude"])*math.pi/180    
    del_Lon = (Lon2-Lon1)
    del_sigma = math.acos(math.sin(Lat1)*math.sin(Lat2) + math.cos(Lat1)*math.cos(Lat2)*math.cos(del_Lon))
    distance=0.5*3959*del_sigma
# copied code ends here
    return distance

def add_map(route_problem,city,latitude,longitude):
    route_problem[city]={}
    route_problem[city]["Latitude"]=float(latitude)
    route_problem[city]["Longitude"]=float(longitude)
    route_problem[city]["Segment"]={}

def total_score(route_problem,current_city,successor_city,goal,cost_function,max_segment,max_speed):

    if cost_function=='segments':
        hscore=heuristic(route_problem,successor_city[0],goal)
        if hscore==0:
            hscore=current_city[0]+route_problem[current_city[1]]["Segment"][successor_city[0]]["Length"]
        
        f_score=(hscore/max_segment)+(len(current_city[2])/2)

    elif cost_function=='time':
        hscore=heuristic(route_problem,successor_city[0],goal)
        if hscore==0:
            hscore=current_city[0]+route_problem[current_city[1]]["Segment"][successor_city[0]]["Length"]
        f_score=(hscore/max_speed)+successor_city[3]

    elif cost_function=='distance':
        hscore=heuristic(route_problem,successor_city[0],goal)
        if hscore==0:
            hscore=current_city[0]+route_problem[current_city[1]]["Segment"][successor_city[0]]["Length"]

        f_score=hscore+current_city[0]

    elif cost_function=='delivery':
        t_road=route_problem[current_city[1]]["Segment"][successor_city[0]]["Time"]
        p=route_problem[current_city[1]]["Segment"][successor_city[0]]["p_mistake"]
        t_trip=successor_city[3]
        cost=t_road + (p*2*(t_road+t_trip))
        
        hscore=heuristic(route_problem,successor_city[0],goal)

        f_score=(hscore/max_speed)+cost

    return f_score

    

def successor(route_problem,current_city):
    successor_nodes=[]
    for cities in route_problem[current_city[1]]["Segment"].keys():
        successor_nodes.append([cities,\
                current_city[2][0:]+[cities,"{} for {} miles".format(route_problem[current_city[1]]["Segment"][cities]['Highway'] ,route_problem[current_city[1]]["Segment"][cities]['Length'])]\
                ,route_problem[current_city[1]]["Segment"][cities]['Length']+current_city[3],\
                route_problem[current_city[1]]["Segment"][cities]['Time']+current_city[4],\
                    (route_problem[current_city[1]]["Segment"][cities]['Time']+(2*route_problem[current_city[1]]["Segment"][cities]['p_mistake']*(route_problem[current_city[1]]["Segment"][cities]['Time']+current_city[4])))+current_city[5]])
    
    return successor_nodes


def get_route(start, end, cost):

    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    route_problem,max_segment,max_speed=get_map()


    goal=0
    explored=[]
    route_taken=[]
    miles,hours,delivery_hours=0,0,0
    fringe=[[0,start,[],miles,hours,delivery_hours]]
    heapq.heapify(fringe)   
    while len(fringe)>0:
        current_city=heapq.heappop(fringe)
        if current_city[1]==end:
            goal=1
            break

        explored.append(current_city[1])
        successor_cities=successor(route_problem,current_city)

        for i in range(len(successor_cities)):
            f_score=total_score(route_problem,current_city,successor_cities[i],end,cost,max_segment,max_speed)
            present=False
            if successor_cities[i][0] not in explored:
                for node in fringe:
                    if successor_cities[i][0]==node[1]:
                        present=True
                        break
                if not present:
                    heapq.heappush(fringe,(f_score,successor_cities[i][0],successor_cities[i][1],successor_cities[i][2],successor_cities[i][3],successor_cities[i][4]))

            for node in fringe:
                if successor_cities[i][0]==node[1]:
                    if f_score<node[0]:
                            heapq.heappush(fringe,(f_score,successor_cities[i][0],successor_cities[i][1],successor_cities[i][2],successor_cities[i][3],successor_cities[i][4]))
                    
    route_taken=[]
    for i in range(0,len(current_city[2]),2):
        tuple1 = list()
        tuple1.append(current_city[2][i:i+2][0])
        tuple1.append(current_city[2][i:i+2][1])
        route_taken.append(tuple(tuple1))
    
    if goal==1:
        return {"total-segments" : len(route_taken), 
                "total-miles" : current_city[3], 
                "total-hours" : current_city[4], 
                "total-delivery-hours" : current_city[5], 
                "route-taken" : route_taken}





# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("  Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


