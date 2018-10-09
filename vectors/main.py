import matplotlib.pyplot as plt

def segment(p1, p2):
    a = 0
    b = 1

    step = 1 / 100

    line = []

    while a <= 1 and b >= 0:
        line.append([el1 + el2 for el1, el2 in zip([el * a for el in p1], [el * b for el in p2])])
        a += step
        b -= step

    return line

result = segment([3.5, 3], [0.5, 1])
# x_list = [x for [x, y] in result]
# y_list = [y for [x, y] in result]
# plt.plot(x_list, y_list, 'ro')
# plt.show()

class Vec:
    def __init__(self, labels, function):
        self.D = labels
        self.f = function

def zero_vec(D):
    return Vec(D, {})

def setitem(v, d, val):
    v.f[d] = val

def getitem(v, d):
    return v.f[d] if d in v.f else 0

def scalar_mul(v, alpha):
    new_f = { d: alpha * val for d, val in v.f.items() }
    return Vec(v.D, new_f)

def add(v1, v2):
    new_D = v1.D | v2.D
    return Vec(new_D, { d:(getitem(v1, d) + getitem(v2, d)) for d in new_D })

def neg(v):
    return scalar_mul(v, -1)

def list2vec(L):
    return Vec(set(range(len(L))), {k:x for k,x in enumerate(L)})

def list_dot(u, v):
    return sum([ uel * vel for uel, vel in zip(u, v)])

def dot_product_list(needle, haystack):
    return [ list_dot(needle, haystack[i:i+len(needle)]) for i in range(len(haystack) - len(needle) + 1)]

def triangular_solve_n(rowlist, b):
    assert len(rowlist) == len(b)
    
    if len(rowlist) or len(b) <= 0:
        return []

    x = [0] * len(rowlist[0])
    for i in range(len(rowlist) - 1, -1, -1):
        x[i] = (b[i] - list_dot(x, rowlist[i])) / rowlist[i][i]

    return x




v = Vec({'A','B','C'}, {'A':1})

setitem(v, "B", 2)
print(getitem(v, 'A'))
print(getitem(v, 'B'))
print(getitem(v, 'C'))
print(getitem(v, 'F'))

print(v.f)
print(v.D)
print(scalar_mul(v, 10).f)
u = Vec(v.D, {'A':5., 'C':10.})
added = add(v, u)
print(added.f)
print(neg(added).f)

print(list_dot([1,2,3], [1,2,3]))
print(dot_product_list([1, -1, 1, 1, -1, 1], [1, -1, 1, 1, 1, -1, 1, 1, 1]))
print(list2vec([2,3,4]).f)
print(triangular_solve_n([[2, 3, -4], [0, 1, 2], [0, 0, 5]], [10, 3, 15]))
