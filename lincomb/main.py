import sys
sys.path.append('../vectors')
from vec import Vec

def lin_comb(vlist, clist):
    assert len(vlist) == len(clist)

    return sum([ clist[i] * vlist[i] for i in range(len(vlist)) ])

def standard(D, one):
    return [ Vec(D, { key: one }) for key in D]


print(lin_comb([ Vec({ 0, 1 }, { 0: 10, 1: 20 }), Vec({ 0, 1 }, { 0: 30, 1: 40 }) ], [2, 1]))

print(standard({ "A", "B", "C" }, 1))
