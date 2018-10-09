import sys
sys.path.append('../vectors')
from vec import Vec
from vecutil import list2vec
sys.path.append('../matrix')
from mat import Mat
from matutil import listlist2mat, rowdict2mat, mat2coldict, coldict2mat
from solver import solve
from image_mat_util import file2mat, mat2display
from GF2 import one
from independence import rank

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

def subset_basis(T):
    B = []
    for v in T:
        if not is_superfluous(B + [v], len(B)):
            B.append(v)
    return B

def vec2rep(v, veclist):
    M = coldict2mat(veclist)
    return solve(M, v)

def exchange(S, A, z):
    e = 1.e-14
    comb = vec2rep(z, S)
    for i, coef in enumerate(comb.f.values()):
        if abs(coef - e) > 0 and (not S[i] in A):
            return S[i]

def morph(S, B):
    T = S.copy()
    pairs = []
    A = []

    for inject in B:
        eject = exchange(T, A, B[0])
        A.append(inject)
        T.append(inject)
        T.remove(eject)
        pairs.append((inject, eject))

    return pairs

def my_is_independent(veclist):
    return len(veclist) == rank(veclist)

def my_rank(veclist):
    return len(subset_basis(veclist))

def direct_sum_decompose(U_basis, V_basis, w):
    '''
    input:  A list of Vecs, U_basis, containing a basis for a vector space, U.
    A list of Vecs, V_basis, containing a basis for a vector space, V.
    A Vec, w, that belongs to the direct sum of these spaces.
    output: A pair, (u, v), such that u+v=w and u is an element of U and
    v is an element of V.

    >>> U_basis = [Vec({0, 1, 2, 3, 4, 5},{0: 2, 1: 1, 2: 0, 3: 0, 4: 6, 5: 0}), Vec({0, 1, 2, 3, 4, 5},{0: 11, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0}), Vec({0, 1, 2, 3, 4, 5},{0: 3, 1: 1.5, 2: 0, 3: 0, 4: 7.5, 5: 0})]
    >>> V_basis = [Vec({0, 1, 2, 3, 4, 5},{0: 0, 1: 0, 2: 7, 3: 0, 4: 0, 5: 1}), Vec({0, 1, 2, 3, 4, 5},{0: 0, 1: 0, 2: 15, 3: 0, 4: 0, 5: 2})]
    >>> w = Vec({0, 1, 2, 3, 4, 5},{0: 2, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0})
    >>> direct_sum_decompose(U_basis, V_basis, w) == (Vec({0, 1, 2, 3, 4, 5},{0: 2.0, 1: 4.999999999999972, 2: 0.0, 3: 0.0, 4: 1.0, 5: 0.0}), Vec({0, 1, 2, 3, 4, 5},{0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0}))
    True
    '''

    rep = vec2rep(w, U_basis + V_basis)
    rep_u = Vec(set(range(len(U_basis))), { k: v for k, v in rep.f.items() if k < len(U_basis)  })
    rep_v = Vec(set(range(len(V_basis))), { (k - len(U_basis)): v for k, v in rep.f.items() if k - len(U_basis) >= 0  })

    u = coldict2mat(U_basis) * rep_u
    v = coldict2mat(V_basis) * rep_v
    return (u, v)

def is_invertible(M):
    return len(M.D[0]) == len(M.D[1]) and my_is_independent([v for v in mat2coldict(M).values()])

def find_matrix_inverse(A):
    if(not is_invertible(A)):
        raise ValueError("Non Invertible Matrix")

    cols = []
    for i in A.D[1]:
        cols.append(solve(A, Vec(A.D[1], { i: 1 })))

    res = coldict2mat(cols)
    print(res * A)
    return res

S = [list2vec(v) for v in [[2,4,0],[1,0,3],[0,4,4],[1,1,1]]]
B = [list2vec(v) for v in [[1,0,0],[0,1,0],[0,0,1]]]
for (z,w) in morph(S, B):
    print("injecting ", z)
    print("ejecting ", w)

print(my_is_independent([list2vec(v) for v in [[2,4,0],[8,16,4],[0,0,7]]]))
print(my_is_independent([list2vec(v) for v in [[2,4,0],[8,16,4]]]))
print(my_rank([list2vec(v) for v in [[1,2,3],[4,5,6],[1.1,1.1,1.1]]]))
print(my_rank([ list2vec(v) for v in [[1, 2, 3], [4, 5, 6], [1.1, 1.1, 1.1]] ]))

U_basis = [ list2vec(v) for v in [[2,1,0,0,6,0],[11,5,0,0,1,0],[3,1.5,0,0,7.5,0]] ]
V_basis = [ list2vec(v) for v in [[0, 0, 7, 0, 0, 1], [0, 0, 15, 0, 0, 2]] ]

res = direct_sum_decompose(U_basis, V_basis, list2vec([2,5,0,0,1,0]))
print(direct_sum_decompose(U_basis, V_basis, list2vec([2,5,0,0,1,0])))
print(res[0] + res[1])

res = direct_sum_decompose(U_basis, V_basis, list2vec([0,0,3,0,0,-4]))
print(direct_sum_decompose(U_basis, V_basis, list2vec([0,0,3,0,0,-4])))
print(res[0] + res[1])

res = direct_sum_decompose(U_basis, V_basis, list2vec([1,2,0,0,2,1]))
print(direct_sum_decompose(U_basis, V_basis, list2vec([1,2,0,0,2,1])))
print(res[0] + res[1])

res = direct_sum_decompose(U_basis, V_basis, list2vec([-6,2,4,0,4,5]))
print(direct_sum_decompose(U_basis, V_basis, list2vec([-6,2,4,0,4,5])))
print(res[0] + res[1])

print(is_invertible(listlist2mat([[1, 0, 1, 0], [0, 2, 1, 0], [0, 0, 3, 1], [0, 0, 0, 4]])))
print(is_invertible(listlist2mat([[1, 2, 3], [3, 1, 1]])))

print(find_matrix_inverse(listlist2mat([[1, 0, 1, 0], [0, 2, 1, 0], [0, 0, 3, 1], [0, 0, 0, 4]])))
