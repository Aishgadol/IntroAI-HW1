def pso(s, d, lb, ub, c1, c2, maxiter ,obj_func, wupdate_func):
    #:param s: number of particles
    #:param d: dimension of a particle
    #:param lb: lower bound in the search space
    #:param ub: upper bound in the search space
    #:param c1: constant for velocity update
    #:param c2: constant for velocity update
    #:param maxiter: maximum number of iteration defined to run
    #:param obj_func: function to evaluate particle position
    #:param wupdate_func: function to update the velocity weight

    # initialize swarm
    p = np.random.rand(s, d)   # particle positions
    v = np.zeros_like(p)       # particle velocities
    bp = p                     # best particle positions
    f_p = np.zeros(s)          # current particle function values
    f_bp = np.ones(s) * np.inf # best particle function values
    gp = []                    # best swarm position
    f_gp = np.inf              # best swarm position starting value

    # Initialize the particle's position
    p = lb + p * (ub - lb)

    # Initialize the multiprocessing module if necessary
    processes = 5
    mp_pool = multiprocessing.Pool(processes)

    # Calculate objective function
    f_p = np.array(mp_pool.map(obj_func, p))
    f_bp = f_p.copy()

    # Update swarm's best position
    i_min = np.argmin(f_p)
    if f_p[i_min] < f_gp:
        f_g = f_p[i_min]
        gp = p[i_min, :].copy()

    # Initialize the particle's velocity
    v = -1 + np.random.rand(s, d) * 2

    # Iterate until termination criterion met
    it = 1
    print("Running...")
    while it <= maxiter and np.std(f_p)>1:
      r1 = np.random.uniform(size=(s, d))
      r2 = np.random.uniform(size=(s, d))

      # Update the particles velocities
      w = wupdate_func(it)
      v = w * v + c1 * r1 * (bp - p) + c2 * r2 * (gp - p)

      # Update the particles' positions
      p = p + v

      # Correct for bound violations
      maskl = p < lb
      masku = p > ub
      p = p * (~np.logical_or(maskl, masku)) + lb * maskl + ub * masku

      # Update objectives
      f_p = np.array(mp_pool.map(obj_func, p))

      # Store particle's best position
      i_update = (f_p < f_bp)
      bp[i_update, :] = p[i_update, :].copy()
      f_bp[i_update] = f_p[i_update]

      # Compare swarm's best position with global best position
      i_min = np.argmin(f_bp)
      if f_bp[i_min] < f_gp:
          gp = bp[i_min, :].copy()
          f_gp = f_p[i_min]

      it += 1
    print("Finshed run")
    return gp, f_gp

