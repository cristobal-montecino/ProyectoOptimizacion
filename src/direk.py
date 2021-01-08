import math
DEFAULT_SCALAR_EPSILON = 10**-11
DEFAULT_VECTOR3_EPSILON = 10**-11
DEFAULT_ARBITRARY_VECTOR = (1,0,0)
DEBUG=False

# x a 3d vector
# y a 3d vector
def dot(x,y):
    return x[0]*y[0] + x[1]*y[1] + x[2]*y[2]

def clone_v3(x):
    return [x[0], x[1], x[2]]

def pow2(x):
    return x*x

# x a 3d vector
def norm2(x):
    return dot(x,x)
# s a scalar
# x a 3d vector
# returns s*x
def scale(s, x):
    return [x[0] * s, x[1] * s, x[2] * s]

# x a 3d vector
# y a 3d vector
def add_v3(x, y):
    return [x[0]+y[0], x[1]+y[1], x[2]+y[2]]

# x a 3d vector
# y a 3d vector
def sub_v3(x, y):
    return [x[0]-y[0], x[1]-y[1], x[2]-y[2]]

# x a number
def sqrt(x):
    return math.sqrt(x)

# TODO: make the default epsilon a global constant
# x a 3d vector
def is_near_zero_vector3(x, epsilon=DEFAULT_VECTOR3_EPSILON):
    return norm2(x) <= epsilon

# x a scalar
def is_near_zero_scalar(x, epsilon=DEFAULT_SCALAR_EPSILON):
    return abs(x) <= epsilon

    
def normalize(x, default=[0,0,0], epsilon=DEFAULT_VECTOR3_EPSILON):
    return scale(1/sqrt(norm2(x)), x) if not is_near_zero_vector3(x, epsilon=epsilon) else default

# need len(lengths) >= 1
def get_boundaries(lengths):
    assert len(lengths) >= 1
    
    boundaries = [[0,0], [lengths[0], lengths[0]]]
    r = lengths[0]
    R = lengths[0]
    
    for l in lengths[1:]:
        if r-l <= 0 and 0 <= R-l:
            r = 0
        else:
            r = min(abs(l - r), abs(R - l))
        
        R = R + l
        boundaries.append((r, R))

    return boundaries

# x the 3d vector to project
# r the radius of the 3d sphere shell
def project_to_sphere_shell(x, r,
                            default_arbitrary_vector=DEFAULT_ARBITRARY_VECTOR,
                            epsilon=DEFAULT_VECTOR3_EPSILON):
    return scale(r, normalize(x, default=default_arbitrary_vector, epsilon=DEFAULT_VECTOR3_EPSILON))

# y the 3d vector target
def get_xn(boundaries, y, default_arbitrary_vector=DEFAULT_ARBITRARY_VECTOR, vector3_epsilon=DEFAULT_VECTOR3_EPSILON):
    rn, Rn = boundaries[-1]
    ylength2 = norm2(y)
    
    if rn*rn <= ylength2 and ylength2 <= Rn*Rn:
        return y
    
    # Rn if ylength >= Rn
    # rn if ylength <= rn
    r = Rn if ylength2 >= Rn*Rn else rn
    
    return project_to_sphere_shell(y, r, default_arbitrary_vector=default_arbitrary_vector, epsilon=vector3_epsilon)

def get_xk_radius_dependent(r, y, xk1, lk1, scalar_epsilon=DEFAULT_SCALAR_EPSILON):
    tmp = r*r - lk1*lk1 + norm2(xk1)
    
    if DEBUG:
        print(f'sqrt of {r*r - tmp*tmp/norm2(xk1)/4}')
    if r*r - tmp*tmp/norm2(xk1)/4 < 0:
        if is_near_zero_scalar(r*r - tmp*tmp/norm2(xk1)/4, epsilon=scalar_epsilon):
            if DEBUG:
                print(f'near zero')
            return scale(tmp/norm2(xk1)/2, xk1)
        else:
            return None
        
    return add_v3(scale(sqrt(r*r - tmp*tmp/norm2(xk1)/4), normalize(sub_v3(y, scale(dot(y, xk1)/norm2(xk1), xk1)))), scale(tmp/norm2(xk1)/2, xk1))

def check_y_condition(y, xk1, epsilon=DEFAULT_VECTOR3_EPSILON):
    return not is_near_zero_vector3(sub_v3(y, scale(dot(y, xk1)/norm2(xk1), xk1)), epsilon=epsilon)

# xk1 = x[k+1]
# lk1 = lengths[k]
def get_xk(boundary, lk1, yk, xk1,
           default_arbitrary_vector=DEFAULT_ARBITRARY_VECTOR,
           vector3_epsilon=DEFAULT_VECTOR3_EPSILON,
           scalar_epsilon=DEFAULT_SCALAR_EPSILON):
    if is_near_zero_vector3(xk1, epsilon=vector3_epsilon):
        if DEBUG:
            print('xk1 is zero')
        return project_to_sphere_shell(yk, lk1, default_arbitrary_vector=default_arbitrary_vector)
    
    rk, Rk = boundary
    
    a2 = pow2(norm2(xk1) - dot(yk, xk1))
    b2 = norm2(yk) * norm2(xk1) - pow2(dot(yk,xk1))
    
    candidates = [rk, Rk, 0.0, 0.0, 0.0]
    ncandidates = 2 if rk > 0.0 else 3
    
    if not is_near_zero_scalar(a2 + b2, epsilon=scalar_epsilon):
        d = (lk1*lk1 + norm2(xk1))
        e = pow2(norm2(xk1)-lk1*lk1)
        
        tmp = sqrt(d*d-(a2*e+b2*d*d)/(a2 + b2))
        candidates[ncandidates] = sqrt(d - tmp)
        if rk <= candidates[ncandidates] and candidates[ncandidates] <= Rk:
            ncandidates += 1
        
        candidates[ncandidates] = sqrt(d + tmp)
        if rk <= candidates[ncandidates] and candidates[ncandidates] <= Rk:
            ncandidates += 1
                
    if check_y_condition(yk, xk1, epsilon=vector3_epsilon):
        y = yk
    else:
        if DEBUG:
            print('no y condition')
        
        # TODO: change this with a policy
        y = (0, 1, 0)
        if not check_y_condition(y, xk1, epsilon=vector3_epsilon):
            if DEBUG:
                print('no y condition subcase')
            y = (1, 0, 0)
    
    min_r = 0.0
    min_value = float('inf')
    min_xk = None
    
    for i in range(ncandidates):
        r = candidates[i]
        xk = get_xk_radius_dependent(r, y, xk1, lk1, scalar_epsilon=scalar_epsilon)
        if xk is not None:
            value = norm2(sub_v3(xk, yk))
            if value < min_value:
                min_value = value
                min_xk = xk
                min_r = r    
    if DEBUG:
        print(f'rk={rk} Rk={Rk} candidates {candidates}')
        print(f'pick candidate r={min_r}')
        
    return min_xk
                      
# y is a list of 3d vectors
def get_nodes(y, target, lengths,
              default_arbitrary_vector=DEFAULT_ARBITRARY_VECTOR,
              scalar_epsilon=DEFAULT_SCALAR_EPSILON,
              vector3_epsilon=DEFAULT_VECTOR3_EPSILON):
    n = len(y) - 1
    x = [None] * len(y)

    x0 = y[0]
    y = [sub_v3(yk, x0) for yk in y]
    target = sub_v3(target, x0)
    x[0] = (0.0, 0.0, 0.0)
    
    boundaries = get_boundaries(lengths)
    
    if DEBUG:
        print(f'boundaries = {boundaries}')
    
    x[n] = get_xn(boundaries, target,
                  default_arbitrary_vector=default_arbitrary_vector,
                  vector3_epsilon=vector3_epsilon)
                      
    for k in range(n-1,0,-1):
        if DEBUG:
            print(f'k = {k}')
            print(f'length = {lengths[k]}')
            print(f'boundary = {boundaries[k]}')
        
        # IMPROVEMENT: default_arbitrary_vector based on the xk history
        x[k] = get_xk(boundaries[k], lengths[k], y[k], x[k+1],
                      default_arbitrary_vector=default_arbitrary_vector,
                      scalar_epsilon=scalar_epsilon,
                      vector3_epsilon=vector3_epsilon)
        
    return [add_v3(xk, x0) for xk in x]

def reversed_method(y, target, lengths,
                    default_arbitrary_vector=DEFAULT_ARBITRARY_VECTOR,
                    scalar_epsilon=DEFAULT_SCALAR_EPSILON,
                    vector3_epsilon=DEFAULT_VECTOR3_EPSILON):
    boundaries = get_boundaries(lengths)
    xn = get_xn(boundaries, target,
                  default_arbitrary_vector=default_arbitrary_vector,
                  vector3_epsilon=vector3_epsilon)
    
    rev_lengths = list(reversed(lengths))
    
    rev_y = list(reversed(y))
    rev_y[0] = xn
    
    zero_vector = [0.0, 0.0, 0.0]
    
    x = get_nodes(rev_y, zero_vector, rev_lengths, scalar_epsilon=scalar_epsilon, vector3_epsilon=vector3_epsilon)
    x.reverse()
    
    return x

def direk_from_effector_to_base(y, target, lengths, scalar_epsilon=DEFAULT_SCALAR_EPSILON, vector3_epsilon=DEFAULT_VECTOR3_EPSILON):
    return get_nodes(y, target, lengths, scalar_epsilon=scalar_epsilon, vector3_epsilon=vector3_epsilon)

def direk_from_base_to_effector(y, target, lengths, scalar_epsilon=DEFAULT_SCALAR_EPSILON, vector3_epsilon=DEFAULT_VECTOR3_EPSILON):
    return reversed_method(y, target, lengths, scalar_epsilon=scalar_epsilon, vector3_epsilon=vector3_epsilon)

# method: 1: 'from_base', 0: 'from_effector'
# repulsion_coeff only works for method='from_effector'
def direk(y, target, lengths,
          repulsion_coeff=0.1,
          method=0,
          scalar_epsilon=DEFAULT_SCALAR_EPSILON,
          vector3_epsilon=DEFAULT_VECTOR3_EPSILON):
    if len(lengths) == 0:
        return [clone_v3(y[0])]
    
    if (method == 1):
        return direk_from_base_to_effector(y, target, lengths, scalar_epsilon=scalar_epsilon, vector3_epsilon=vector3_epsilon)
    elif (method == 0):
        new_y = [[0.0, 0.0, 0.0]]
        new_y.extend(scale(repulsion_coeff/lk,sub_v3(yk1,yk)) for yk, yk1, lk in zip(y[:-1], y[1:], lengths))

        accum = new_y[0]
        for i in range(1, len(new_y)):
            accum = add_v3(accum, new_y[i])
            new_y[i] = add_v3(y[i], accum)

        y = new_y
    
        return direk_from_effector_to_base(y, target, lengths, scalar_epsilon=scalar_epsilon, vector3_epsilon=vector3_epsilon)
    else:
        raise ValueError(f'invalid method \'{method}\'. Valid methods: \'from_base\', \'from_effector\'')