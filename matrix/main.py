import sys
sys.path.append('../vectors')
from vec import Vec
from vecutil import list2vec
from GF2 import one
from matutil import coldict2mat, rowdict2mat, listlist2mat, mat2coldict, mat2rowdict
from mat import Mat
from image_mat_util import file2mat, mat2display
from transform import identity, translation, scale, rotation, rotation_about, scale_colors, grayscale
from math import pi

print([ [0 for j in range(0, 4) ] for i in range(0, 3) ])
print([ [i - j for i in range(0, 3) ] for j in range(0, 4) ])

# class Mat:
#     def __init__(self, labels, function):
#         self.D = labels
#         self.f = function

# def identity(D):
#     return Mat((D, D), { (d, d): 1 for d in D })

def mat2rowdict(M):
    # TODO smart getter with sparcity.
    return { r: Vec(M.D[1], { c: M.f[(r, c)] for c in M.D[1] }) for r in M.D[0] }

def mat2coldict(M):
    # TODO smart getter with sparcity.
    return { c: Vec(M.D[0], { r: M.f[(r, c)] for r in M.D[0] }) for c in M.D[1] }

def mat2vec(M):
    # TODO smart getter with sparcity.
    return Vec({ (r,c) for c in M.D[1] for r in M.D[0] }, M.f)

def transpose(M):
    return Mat((M.D[1], M.D[0]), { (pair[1], pair[0]): val for pair, val in M.f.items() })

def button_vectors(n):
 D = {(i,j) for i in range(n) for j in range(n)}
 vecdict={(i,j):Vec(D,dict([((x,j),one) for x in range(max(i-1,0), min(i+2,n))]
                           +[((i,y),one) for y in range(max(j-1,0), min(j+2,n))]))
                           for (i,j) in D}

def diag(D, entries):
    return Mat((D, D), { (key, key):val for key, val in entries.items() })

M = Mat(({'a','b'}, {'@', '#', '?'}), {('a','@'):1, ('a','#'):2,
          ('a','?'):3, ('b','@'):10, ('b','#'):20, ('b','?'):30})

I = Mat(({'a', 'b', 'c'}, {'a', 'b', 'c'}), { ('a', 'a'):1, ('b', 'b'):1, ('c', 'c'):1 })
# I = identity({ 'a', 'b', 'c' })
print(mat2rowdict(M))
print(mat2coldict(M))
print(mat2vec(M))
print(mat2vec(transpose(M)))

# print('==========')
# B = coldict2mat(button_vectors(5))
# print(B)

print(diag({"a", "b", "c"}, { "a": 1, "b": 2, "c": 3 }).f)

print("%%%%%%%%%%%%%%%%%%%%%%")
print("HAMMING CODE")
G = listlist2mat([[one, 0, one, one], [one, one, 0, one], [0, 0, 0, one], [one, one, one, 0], [0, 0, one, 0], [0, one, 0, 0], [one, 0, 0, 0]])

word = list2vec([one,0,0,one])
codeword = G * word
print("Codeword:")
print(codeword)

R = Mat((G.D[1], G.D[0]), { (0, 6): one, (1, 5): one, (2, 4): one, (3, 2): one })
print("Decoded:")
print(R * codeword)
print("R * G:")
print(R * G)

H = listlist2mat([[0, 0, 0, one, one, one, one], [0, one, one, 0, 0, one, one], [one, 0, one, 0, one, 0, one]])

print(H * G)

def find_error(synd):
    cols = mat2coldict(H)
    return Vec(H.D[1], { key: one for key, col in cols.items() if col == synd })

non_codeword = list2vec([one, 0, one, one, 0, one, one])
synd = H * non_codeword
print("Syndrome for non-codeword:")
print(synd)
error = find_error(synd)
print("Error vector:")
print(error)
fixed = non_codeword + error
print("Fixed:")
print(fixed)
orig = R * fixed
print("Original message:")
print(orig)

def find_error_matrix(S):
    cols = mat2coldict(S)
    return coldict2mat({ key: find_error(col) for key, col in cols.items() })

print("With error matrix:")
print(find_error_matrix(coldict2mat({ 0: list2vec([one, one, one]), 1: list2vec([0, 0, one])})))

print('%%%%%%%%%%%%%%%%%%%%%%%%%')
print("IMAGE TRANSFORMATIONS")
file = file2mat('./tt.png')
# file = (identity() * file[0], file[1])
# file = (translation(-100, 0) * file[0], file[1])
# file = (scale(1, 2) * file[0], file[1])
# file = (rotation(-0 / 8) * (translation(300, 200) * file[0]), file[1])
# file = (rotation_about(0, 300, 200) * file[0], file[1])
# file = (file[0], scale_colors(1, 10, 1) * file[1])
file = (file[0], grayscale() * file[1])
# mat2display(file[0], file[1])

print('%%%%%%%%%%%%%%%%%%%%%%%%%')
print("Different Matrix Opertaions Implementation")

A = listlist2mat([[-1,1,2], [1,2,3], [2,2,1]])
v1 = list2vec([1,2,0])
print(A * v1)
v2 = list2vec([4,3,2,1])
B = listlist2mat([[-5, 10], [-4, 8], [-3, 6], [-2, 4]])
print(v2 * B)
C = listlist2mat([[1,2], [4,5], [5,6]])
print(A * C)

def lin_comb_mat_vec_mult(M,v):
    cols = mat2coldict(M)
    return sum([ v[d] * col  for d, col in cols.items() ])

def lin_comb_vec_mat_mult(v,M):
    rows = mat2rowdict(M)
    return sum([ v[d] * row for d, row in rows.items() ])

def dot_product_mat_vec_mult(M,v):
    rows = mat2rowdict(M)
    return Vec(M.D[1], { d: row * v for d, row in rows.items() })

def dot_product_vec_mat_mult(v,M):
    cols = mat2coldict(M)
    return Vec(M.D[1], { d: v * col for d, col in cols.items() })

def Mv_mat_mat_mult(A,B):
    cols = mat2coldict(B)
    return coldict2mat({ d: A * col for d, col in cols.items() })

def vM_mat_mat_mult(A,B):
    rows = mat2rowdict(A)
    return rowdict2mat({ d: row * B for d, row in rows.items() })

print(lin_comb_mat_vec_mult(A, v1))
print(lin_comb_vec_mat_mult(v2, B))
print(dot_product_mat_vec_mult(A, v1))
print(dot_product_vec_mat_mult(v2, B))
print(Mv_mat_mat_mult(A, C))
print(vM_mat_mat_mult(A, C))

def dictlist_helper(dlist, k):
    return [ d[k] for d in dlist ]

print(dictlist_helper([{'a':'apple', 'b':'bear'}, {'a':1, 'b':2}], 'a'))

Inv1 = listlist2mat([[3,1],[0,2]])
Inv2 = listlist2mat([[1, 1/6], [-2, 1/2]])

print(Inv1 * Inv2)
print(Inv2 * Inv1)
