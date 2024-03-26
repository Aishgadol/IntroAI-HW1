import numpy as np
import matplotlib.pyplot as plt
import itertools
import multiprocessing
import VRP
import pso
import functools

def w_update(w_min ,w_max, max_iter, i):
  return ((w_max - w_min) * ((max_iter-i)/max_iter) + w_min )

def discretization(x, lb, ub):
  res=np.zeros(len(x))
  for i,val in enumerate(x):
    if(np.round(val)>ub):
        res[i]=int(ub)
    else:
        res[i]=int(np.round(val))
  return res

def split_into_assigned_routes(a, ub):
  #TODO: fill in function
  routes=[[] for _ in range(ub)]
  for i, route_number in enumerate(a):
    routes[min((ub-1),int(route_number))].append(i+1)
  return routes
def find_order_for_assignment(locations, vrp):
  #used nearest neighbor approach where cost is distance+time
  def compute_cost_of_path(route,vrp):
    cost=vrp.compute_route_distance(route)+vrp.compute_route_time(route)
    return cost
  cost_table=np.zeros((len(locations),len(locations)))
  ordered=[0]
  visited=[]
  for i in range(len(locations)):
    remaining_locs=locations.copy()
    for loc in visited:
        remaining_locs.remove(loc)
    costs_from_curr={loc:compute_cost_of_path([ordered[-1],loc],vrp) for loc in remaining_locs}
    best_loc=min(costs_from_curr,key=costs_from_curr.get)
    ordered.append(best_loc)
    visited.append(best_loc)
  ordered.append(0)
  return ordered

def objective_function(vrp, lb, ub, particle):
    sum=0
    for route in particle:
        sum+=0.65*vrp.compute_route_distance([0]+route+[0])+vrp.compute_route_time([0]+route+[0])
    return sum

vrp=VRP.VRP('Ex3-d33')
#Defining parameter for the run
SWARM_SIZE = 1000
MAX_ROUTES = 10
C1 = 2
C2 = 2
W_MIN = 0.4
W_MAX = 0.9
MAX_ITER = 500

# Define functions to pass to pso
pso_obj_func = functools.partial(objective_function, vrp, 0, MAX_ROUTES-1)
pso_w_update = functools.partial(w_update, W_MIN ,W_MAX, MAX_ITER)


# Run PSO
sol,f_sol = pso.pso(s = SWARM_SIZE,
            d = vrp.dim-1,
            lb = 0,
            ub = MAX_ROUTES - 1,
            c1 = C1,
            c2 = C2,
            maxiter = MAX_ITER,
            obj_func = pso_obj_func,
            wupdate_func = pso_w_update)

d_sol = discretization(sol,0,MAX_ROUTES-1)
print(d_sol)
route_assignments = split_into_assigned_routes(d_sol,MAX_ROUTES-1)
sol = [find_order_for_assignment(r, vrp) for r in route_assignments]

vrp.plot_routes(sol)
total_distance,total_time=vrp.print_routes(sol)

'''
C1=2
C2=2
W_MIN=0.4
W_MAX=0.9
best_swarm_size=0
best_max_routes=0
best_c1=0
best_c2=0
best_max_iter=0
dists={}
times={}
costs={}
for MAX_ITER in [10,50,100,500,1000,5000,10000]:
    for SWARM_SIZE in [10,50,100,500,1000,5000]:
        for MAX_ROUTES in range(2,11):
            # Run PSO
            pso_obj_func = functools.partial(objective_function, vrp, 0, MAX_ROUTES-1)
            pso_w_update = functools.partial(w_update, W_MIN ,W_MAX, MAX_ITER)
            sol,f_sol = pso.pso(s = SWARM_SIZE,
                        d = vrp.dim-1,
                        lb = 0,
                        ub = MAX_ROUTES - 1,
                        c1 = C1,
                        c2 = C2,
                        maxiter = MAX_ITER,
                        obj_func = pso_obj_func,
                        wupdate_func = pso_w_update)
            # Print and plot solution
            d_sol = discretization(sol,0,MAX_ROUTES-1)
            print(d_sol)
            route_assignments = split_into_assigned_routes(d_sol,MAX_ROUTES-1)
            sol = [find_order_for_assignment(r, vrp) for r in route_assignments]

            #vrp.plot_routes(sol)
            longest_distance,longest_time=vrp.print_routes(sol)
            dists[longest_distance]=f'Longest Distance: {longest_distance} , Swarm size: {SWARM_SIZE} , max routes: {MAX_ROUTES},  max iter: {MAX_ITER}'
            times[longest_time]=f'Longest time: {longest_time} , Swarm size: {SWARM_SIZE} , max routes: {MAX_ROUTES}, max iter: {MAX_ITER}'
min_dist=min(dists,key=dists.get)
min_time=min(times,key=times.get)
print(f'shortest longest distance we got: {min_dist} with info: {dists[min_dist]} ')
print(f'shortest longest time we got: {min_time} with info: {times[min_time]}')
'''