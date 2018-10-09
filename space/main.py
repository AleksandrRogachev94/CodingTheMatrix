import sys
sys.path.append('../vectors')
from vec import Vec

def vec_select(veclist, k):
    return [v for v in veclist if v[k] == 0]

def vec_sum(veclist, D):
    return sum([Vec(D, { d: v[d] for d in D }) for v in veclist], Vec(D, {}))
    # return sum(veclist, Vec(D, {}))

def vec_select_sum(veclist, D, k):
    return vec_sum(vec_select(veclist, k), D)

def scale_vecs(vecdict):
    '''
    >>> v1 = Vec({1,2,4}, {2: 9})
    >>> v2 = Vec({1,2,4}, {1: 1, 2: 2, 4: 8})
    >>> result = scale_vecs({3: v1, 5: v2})
    >>> len(result)
    2
    >>> [v in [Vec({1,2,4},{2: 3.0}), Vec({1,2,4},{1: 0.2, 2: 0.4, 4: 1.6})] for v in result]
    [True, True]
    '''
    return [ (1 / k) * v for k, v in vecdict.items() ]


def GF2_span(D, L):
    '''
    >>> from GF2 import one
    >>> D = {'a', 'b', 'c'}
    >>> set(GF2_span(D, [Vec(D, {'a':one, 'c':one}), Vec(D, {'c':one})])) == {Vec(D,{}), Vec(D,{'a':one, 'c':one}), Vec(D,{'c': one}), Vec(D,{'a':one})}
    True
    >>> set(GF2_span(D, [Vec(D, {'a':one, 'b':one}), Vec(D, {'a':one}), Vec(D, {'b':one})])) == {Vec(D,{'a':one, 'b':one}), Vec(D,{'b':one}), Vec(D,{'a':one}), Vec(D,{})}
    True
    >>> set(GF2_span(D, [Vec(D, {'a':one, 'b':one}), Vec(D, {'c':one})])) == {Vec(D,{}), Vec(D,{'a':one, 'b':one}), Vec(D,{'a':one, 'b':one, 'c':one}), Vec(D,{'c':one})}
    True
    >>> S=[Vec({0,1},{0:one}), Vec({0,1},{1:one})]
    >>> set(GF2_span({0,1}, S)) == {Vec({0, 1},{0: one, 1: one}), Vec({0, 1},{1: one}), Vec({0, 1},{0: one}), Vec({0, 1},{})}
    True
    >>> D = {'a', 'b', 'c'}
    >>> L = [Vec(D, {'a': one, 'c': one}), Vec(D, {'b': one})]
    >>> len(GF2_span(D, L))
    4
    >>> Vec(D, {}) in GF2_span(D, L)
    True
    >>> Vec(D, {'b': one}) in GF2_span(D, L)
    True
    >>> Vec(D, {'a':one, 'c':one}) in GF2_span(D, L)
    True
    >>> Vec(D, {x:one for x in D}) in GF2_span(D, L)
    True
    '''
    if len(L) <= 0:
        return [Vec(D, {})]
    elif len(L) == 1:
        return [L[0], 0 * L[0]]

    next_combs = GF2_span(D, L[1:])
    coefs = [0, 1]
    return [ coef * L[0] + next_comb for coef in coefs for next_comb in next_combs ]

print(vec_select([Vec({ "A", "B" }, { "A": 1, "B": 0 }), Vec({ "A", "B" }, { "A": 0, "B": 1 }), Vec({ "A", "B" }, {})], "A"))
print(vec_sum([Vec({"A", "C", "B"},{"A": 10, "C": 30}), Vec({"A", "B", "D"},{"A": 3, "B": 2, "D":1})], {"A", "B"}))
print(vec_sum([], {"A", "B"}))

print('=========')
print(GF2_span({}, [Vec({0,1,2}, {0: 1, 1: 2, 2: 3}), Vec({0,1,2}, {0: 2, 1: 3, 2: 4})]))
