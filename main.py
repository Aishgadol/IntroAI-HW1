def w_update(w_min ,w_max, max_iter, i):
  return ((w_max - w_min) * ((max_iter-i)/max_iter) + w_min )


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