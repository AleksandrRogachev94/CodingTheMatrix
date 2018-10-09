import sys
sys.path.append('../vectors')
from vec import Vec
from vecutil import list2vec
from mat import Mat
from matutil import coldict2mat, listlist2mat, mat2coldict
from math import sin, cos

def identity():
    D = { 'x', 'y', 'u' }
    return Mat((D, D), { (k, k): 1 for k in D })

def translation(alpha, beta):
    res = identity()
    res['x', 'u'] = alpha
    res['y', 'u'] = beta
    return res

def scale(alpha, beta):
    res = identity()
    res['x', 'x'] =  alpha
    res['y', 'y'] =  beta
    return res

def rotation(theta):
    D = { 'x', 'y', 'u' }
    return Mat((D, D), { ('x', 'x'): cos(theta), ('x', 'y'): -sin(theta),
        ('y', 'x'): sin(theta), ('y', 'y'): cos(theta),
        ('u', 'u'): 1  })

def rotation_about(theta, x, y):
    return translation(x, y) * rotation(theta)

def reflection_x():
    D = { 'x', 'y', 'u' }
    return Mat((D, D), { ('x', 'x'): 1, ('y', 'y'): -1, ('u', 'u'): 1 })

def reflection_y():
    D = { 'x', 'y', 'u' }
    return Mat((D, D), { ('x', 'x'): -1, ('y', 'y'): 1, ('u', 'u'): 1 })

def scale_colors(r, g, b):
    D = { 'r', 'g', 'b' }
    return Mat((D, D), { ('r', 'r'): r, ('g', 'g'): g, ('b', 'b'): b })

def grayscale():
    D = { 'r', 'g', 'b' }
    cr = 77 / 256; cg = 151 / 256; cb = 28 / 256
    return Mat((D, D), { ('r', 'r'): cr, ('r', 'g'): cg, ('r', 'b'): cb,
        ('g', 'r'): cr, ('g', 'g'): cg, ('g', 'b'): cb,
        ('b', 'r'): cr, ('b', 'g'): cg, ('b', 'b'): cb })

# def reflect_about(x1, y1, x2, y2):
#     return reflection()
