import sys
sys.path.append('../vectors')
from vec import Vec
from vecutil import list2vec
sys.path.append('../matrix')
from mat import Mat
from matutil import rowdict2mat, mat2coldict, coldict2mat, listlist2mat
sys.path.append('../dim')
from solver import solve
from independence import is_independent
from GF2 import one
import random
from factoring_support import intsqrt, gcd, primes, dumb_factor
from math import sqrt
from echelon import transformation, row_reduce

# ********************* LAB 1 *********************

def randGF2(): return random.randint(0,1)*one

a0 = list2vec([one, one, 0, one, 0, one])
b0 = list2vec([one, one, 0, 0, 0, one])

def rand_vec():
    return list2vec([ randGF2() for i in range(6) ])

def choose_secret_vector(s,t):
    while True:
        u = rand_vec()
        if u * a0 == s and u * b0 == t:
            return u

def find_base_vecs():
    combs = { (i, j, k) for i in range(8) for j in range(8) for k in range(8) }

    while True:
        vecs = [ rand_vec() for i in range(8) ]

        for comb in combs:
            if not is_independent({ vecs[comb[0]], vecs[comb[1]], vecs[comb[2]] }):
                continue

        return vecs

secret = choose_secret_vector(0, 0)
base_vecs = find_base_vecs()

# ******************** LAB 2 **********************

def root_method(N):
    a = intsqrt(N)
    print(a)
    while True:
        a += 1
        b = sqrt(a * a - N)

        if b == int(b):
            return (a - b, a + int(b))

    # return (0, 0)

def int2GF2(i):
    return 0 if i % 2 == 0 else one

def make_Vec(primeset, factors):
    return Vec(primeset, { p: int2GF2(a) for p, a in factors })

def find_candidates(N, primeset):
    roots = []; rowlist = []
    x = intsqrt(N) + 1
    while(True):
        x += 1
        factors = dumb_factor(x * x - N, primeset)
        if len(factors) > 0:
            roots.append(x)
            rowlist.append(make_Vec(primeset, factors))
            if len(roots) >= len(primeset) + 1:
                break

    return (roots, rowlist)

print(root_method(55))
print(root_method(77))
print(root_method(146771))
# print(root_method(118))

print(gcd(23, 15))
N = 367160330145890434494322103
a = 67469780066325164
b = 9429601150488992
c = a * a - b * b
print(gcd(a - b, N))

print(make_Vec({2,3,5,7,11}, [(3,1)]))
print(make_Vec({2,3,5,7,11}, [(2,17), (3, 0), (5,1), (11,3)]))
print(find_candidates(2419, primes(32))[1])

A = listlist2mat([[0, 2, 3, 4, 5], [0, 0, 0, 3, 2], [1, 2, 3, 4, 5], [0, 0, 0, 6, 7], [0, 0, 0, 9, 8]])
print(A)
M = transformation(A)
print(M)
# print(M * A)
print(M * A)
# print()
# print(listlist2mat([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 0, 2, 1, 0], [0, 0, 3.004, 0.667, 1]]) * (M * A))
print(row_reduce([list2vec([one, one, 0, 0]), list2vec([one, 0, one, 0]), list2vec([0, one, one, one]), list2vec([one, 0, 0, 0])]))

# *********************** PROBLEMS *************************
def is_echelon(rowlist):
    col_label_list = sorted(rowlist[0].D, key=repr)
    prev_last_nonzero = None
    for r in rowlist:
        next_last_nonzero = next((col_label for col_label in col_label_list if r[col_label] != 0), None)
        if prev_last_nonzero is None:
            prev_last_nonzero = next_last_nonzero
        else:
            if col_label_list.index(next_last_nonzero) <= col_label_list.index(prev_last_nonzero):
                return False
            prev_last_nonzero = next_last_nonzero

    return True

print(is_echelon([list2vec([2, 1, 0]), list2vec([0, -4, 0]), list2vec([0, 0, 1])]))
print(is_echelon([list2vec([2, 1, 0]), list2vec([-4, 0, 0]), list2vec([0, 0, 1])]))
print(is_echelon([list2vec([2, 1, 0]), list2vec([0, 3, 0]), list2vec([1, 0, 1])]))
print(is_echelon([list2vec([1, 1, 1, 1, 1]), list2vec([0, 2, 0, 1, 3]), list2vec([0, 0, 0, 5, 3])]))
