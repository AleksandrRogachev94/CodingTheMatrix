import sys
sys.path.append('../vectors')
from vec import Vec
from vecutil import list2vec
sys.path.append('../matrix')
from mat import Mat
from matutil import rowdict2mat, mat2coldict, coldict2mat
from solver import solve
from image_mat_util import file2mat, mat2display
from GF2 import one

#%%%%%%%%%%%%%%%%%%%% LAB %%%%%%%%%%%%%%%%%%%%

D = { (y, x) for x in ["x1", "x2", "x3"] for y in ["y1", "y2", "y3"] }

def move2board(y):
    return Vec(y.D, { 'y1': y['y1'] / y['y3'], 'y2': y['y2'] / y['y3'], 'y3': 1  })
    # return Vec(y.D, { 'y3': 1  })

def mat_move2board(M):
    return coldict2mat({ d: move2board(pnt) for d, pnt in mat2coldict(M).items() })

def make_equations(x1, x2, w1, w2):
    return [
        Vec(D, { ("y1", "x1"): -x1, ("y1", "x2"): -x2, ("y1", "x3"): -1,
            ("y3", "x1"): w1 * x1, ("y3", "x2"): w1 * x2, ("y3", "x3"): w1 }),
        Vec(D, { ("y2", "x1"): -x1, ("y2", "x2"): -x2, ("y2", "x3"): -1,
            ("y3", "x1"): w2 * x1, ("y3", "x2"): w2 * x2, ("y3", "x3"): w2 })
    ]


scaling_eq = Vec(D, { ("y1", "x1"): 1 })

# top_left = make_equations(358, 36, 0, 0)
# top_right = make_equations(592, 157, 1, 0)
# bottom_left = make_equations(329, 597, 0, 1)
# bottom_right = make_equations(580, 483, 1, 1)
#
# L = rowdict2mat({ 0: top_left[0], 1: top_left[1], 2: top_right[0], 3: top_right[1],
#     4: bottom_left[0], 5: bottom_left[1], 6: bottom_right[0], 7: bottom_right[1], 8: scaling_eq })
#
# b = Vec(set(range(9)), { 8: 1 })
#
# h = solve(L, b)
# print(h)
# H = Mat(({ "y1", "y2", "y3" }, { "x1", "x2", "x3" }), h.f)
# print(H)
#
# (X_pts, colors) = file2mat('board.png', ('x1','x2','x3'))
# Y_pts = H * X_pts
# Y_board = mat_move2board(Y_pts)
#
# print(H * Vec({ "x1", "x2", "x3" }, { "x1": 358, "x2": 36, "x3": 1 }))

# mat2display(Y_board, colors, ('y1', 'y2', 'y3'),
# scale=100, xmin=None, ymin=None)


#%%%%%% ANOTHER IMAGE %%%%%%%%%%%

# top_left = make_equations(232, 202, 0, 0)
# top_right = make_equations(295, 192, 1, 0)
# bottom_left = make_equations(228, 286, 0, 1)
# bottom_right = make_equations(293, 281, 1, 1)
#
# L = rowdict2mat({ 0: top_left[0], 1: top_left[1], 2: top_right[0], 3: top_right[1],
#     4: bottom_left[0], 5: bottom_left[1], 6: bottom_right[0], 7: bottom_right[1], 8: scaling_eq })
#
# b = Vec(set(range(9)), { 8: 1 })
#
# h = solve(L, b)
# print(h)
# H = Mat(({ "y1", "y2", "y3" }, { "x1", "x2", "x3" }), h.f)
# print(H)
#
# (X_pts, colors) = file2mat('cit.png', ('x1','x2','x3'))
# Y_pts = H * X_pts
# Y_board = mat_move2board(Y_pts)
#
# print(H * Vec({ "x1", "x2", "x3" }, { "x1": 358, "x2": 36, "x3": 1 }))

# mat2display(Y_board, colors, ('y1', 'y2', 'y3'),
# scale=100, xmin=None, ymin=None)

#%%%%%%%%%%%%%%%%%%%% PROBLEMS %%%%%%%%%%%%%%%%%%%%

def rep2vec(u, veclist):
    return coldict2mat(veclist) * u

def vec2rep(v, veclist):
    M = coldict2mat(veclist)
    return solve(M, v)

veclist= [[1,0,2,0],[1,2,5,1],[1,5,-1,3]]
veclist = [ list2vec(v) for v in veclist ]
u = list2vec([5, 3, -2])
print(rep2vec(u, veclist))

v = list2vec([6,-4,27,-3])
veclist = [[1,0,2,0],[1,2,5,1],[1,5,-1,3]]
veclist = [ list2vec(v) for v in veclist ]
print(vec2rep(v, veclist))

def is_superfluous(L, i):
    '''
    >>> a0 = Vec({'a','b','c','d'}, {'a':1})
    >>> a1 = Vec({'a','b','c','d'}, {'b':1})
    >>> a2 = Vec({'a','b','c','d'}, {'c':1})
    >>> a3 = Vec({'a','b','c','d'}, {'a':1,'c':3})
    >>> is_superfluous([a0,a1,a2,a3], 3)
    True
    >>> is_superfluous([a0,a1,a2,a3], 0)
    True
    >>> is_superfluous([a0,a1,a2,a3], 1)
    False
    '''
    if len(L) <= 1:
        return False

    M = coldict2mat(L[0:i] + L[i + 1:])
    sol = solve(M, L[i])
    # print(sol)
    e = 1.e-14
    residual = M * sol - L[i]
    return residual * residual < e

def is_independent(L):
    '''
    input: a list L of vectors (using vec class)
    output: True if the vectors form a linearly independent list.
    >>> vlist = [Vec({0, 1, 2},{0: 1, 1: 0, 2: 0}), Vec({0, 1, 2},{0: 0, 1: 1, 2: 0}), Vec({0, 1, 2},{0: 0, 1: 0, 2: 1}), Vec({0, 1, 2},{0: 1, 1: 1, 2: 1}), Vec({0, 1, 2},{0: 0, 1: 1, 2: 1}), Vec({0, 1, 2},{0: 1, 1: 1, 2: 0})]
    >>> is_independent(vlist)
    False
    >>> is_independent(vlist[:3])
    True
    >>> is_independent(vlist[:2])
    True
    >>> is_independent(vlist[1:4])
    True
    >>> is_independent(vlist[2:5])
    True
    >>> is_independent(vlist[2:6])
    False
    >>> is_independent(vlist[1:3])
    True
    >>> is_independent(vlist[5:])
    True
    '''

    for i in range(len(L)):
        if is_superfluous(L, i):
            return False

    return True

def subset_basis(T):
    B = []
    for v in T:
        if not is_superfluous(B + [v], len(B)):
            B.append(v)
    return B

def superset_basis(T, L):
    B = T.copy()
    for v in L:
        if not is_superfluous(B + [v], len(B)):
            B.append(v)
    return B

def exchange(S, A, z):
    e = 1.e-14
    comb = vec2rep(z, S)
    for i, coef in enumerate(comb.f.values()):
        if abs(coef - e) > 0 and (not S[i] in A):
            return S[i]

a0 = Vec({'a','b','c','d'}, {'a':1})
a1 = Vec({'a','b','c','d'}, {'b':1})
a2 = Vec({'a','b','c','d'}, {'c':1})
a3 = Vec({'a','b','c','d'}, {'a':1,'c':3})
print(solve(coldict2mat([a0, a1, a2, a3]), Vec({'a','b','c','d'}, {})))

L = [[2,5,5,6],[2,0,1,3],[0,5,4,3]]
L = [ list2vec(v) for v in L ]
print(is_superfluous(L, 2))
L = [[one,one,0,0],[one,one,one,one],[0,0,0,one]]
L = [ list2vec(v) for v in L ]
print(is_superfluous(L, 2))

L = [[1,3,0,0],[2,1,1,0],[0,0,1,0],[1,1,4,-1]]
L = [ list2vec(v) for v in L ]
print(is_independent(L))

L = [1,1,2,1],[2,1,1,1],[1,2,2,1],[2,2,1,2],[2,2,2,2]
L = [ list2vec(v) for v in L ]
print(subset_basis(L))

T = [[0,5,3],[0,2,2],[1,5,7]]; L = [[1,1,1],[0,1,1],[0,0,1]]
T = [ list2vec(v) for v in T ]; L = [ list2vec(v) for v in L ]
print(superset_basis(T, L))
T = [[0,5,3],[0,2,2]]; L = [[1,1,1],[0,1,1],[0,0,1]]
T = [ list2vec(v) for v in T ]; L = [ list2vec(v) for v in L ]
print(superset_basis(T, L))

S=[list2vec(v) for v in [[0,0,5,3] , [2,0,1,3],[0,0,1,0],[1,2,3,4]]]
A=[list2vec(v) for v in [[0,0,5,3],[2,0,1,3]]]
z=list2vec([0,2,1,1])
print(exchange(S, A, z))
