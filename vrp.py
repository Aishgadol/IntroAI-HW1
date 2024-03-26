#import lib
import numpy as np
import matplotlib.pyplot as plt
import itertools

class VRP:
  def __init__(self,file_path):

    self.file_path = file_path  # path to data to initalize vrp
    self.locations = []         # locations holds all x,y coordinates of the locations (including depot)
    self.dim = None             # dim holds the number of locations
    self.dis_mtx = []           # distance matrix - stores the distance from location i to location j
    self.time_mtx =[]           # time matrix - stores the time it takes travel from location i to location j
    self.parse_data_file()
    self.dis_mtx = self.compute_distance_matrix()


  def parse_data_file(self):
    with open(self.file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('DIMENSION'):
                self.dim = int(line.split(': ')[1])
            elif line == 'NODE_COORD_SECTION':
              for i in range(self.dim):
                  line = next(f)
                  node_id, x, y = line.split()
                  self.locations.append((float(x), float(y)))
              self.locations = np.array(self.locations)
            elif line == 'TIME':
              time_lines = []
              for i in range(self.dim):
                line = next(f)
                time_lines.append(line)
              self.time_mtx = np.array([list(map(float, line.split())) for line in time_lines])



  def compute_distance_matrix(self):
    #we're calculating euclidean distance
    self.dis_mtx=np.zeros((self.dim,self.dim))
    for i in range(self.dim):
        for j in range(self.dim):
            self.dis_mtx[i][j]=np.sqrt(np.square(self.locations[i][0]-self.locations[j][0])+np.square(self.locations[i][1]-self.locations[j][1]))
    return self.dis_mtx

  def plot_locations(self):
    plt.scatter(self.locations[:, 0], self.locations[:, 1])
    plt.title("Locations")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

  def plot_routes(self, routes):
    # ~~TODO 3: Plot routes, each route hold ordered locations to visit~~~~
    #   Note: Make sure to add depot to the start and end of each route
    #NOTE: we assume [0] is depot, since in most vehicle routing problems the depot is considered at [0]
    for route in routes:
        #add depot at the start and ending of each route
        route_with_depot = [0] + route + [0]
        #get x,y cords for locations in route
        route_x = [self.locations[i][0] for i in route_with_depot]
        route_y = [self.locations[i][1] for i in route_with_depot]
        #plot the route
        plt.plot(route_x, route_y, marker='o')
    plt.title("Routes")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

  def compute_route_distance(self,route):
    #~~~ TODO 4: given a route calculate the distance it took to travel~~~~
    total_distance = 0
    for i in range(len(route) - 1):
        # add the distance between location i,i+1 in the route
        total_distance += self.dis_mtx[route[i]][route[i+1]]
    return total_distance

  def compute_route_time(self, route):
    # TODO 5: given a route calculate the distance it took to travel~~~~~~
    total_time = 0
    for i in range(len(route) - 1):
        # add the time between locations i,i+1 by getting the travel time from self.time_mtx
        total_time += self.time_mtx[route[i]][route[i+1]]
    return total_time



  def print_routes(self, routes):
    total_time, total_distance = 0, 0
    longest_dist=0
    longest_time=0
    for i,r in enumerate(routes):
        route_string = "depot ->" + " -> ".join(map(str, r)) + " -> depot"
        print(f"vehicle {i + 1} route: " + route_string)
        r_distance = self.compute_route_distance(r)
        r_time = self.compute_route_time(r)
        print(f"Distance for vehicle {i + 1} {r_distance=}, Time traveled = {r_time}")
        total_time+= r_time
        total_distance += r_distance
        if(r_time>longest_time):
            longest_time=r_time
        if(r_distance>longest_dist):
            longest_dist=r_distance
    print(f"Total Distance is: {total_distance}, Total Time = {total_time}")
    print(f'longest route: {longest_dist}, route that takes longest time: {longest_time}')

    #added here
    return longest_dist,longest_time
