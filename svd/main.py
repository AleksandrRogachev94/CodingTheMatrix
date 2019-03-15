from image import color2gray, file2image, image2display
from svd import factor
import os
from math import sqrt

import sys
sys.path.append('../vectors')
sys.path.append('../matrix')
from vec import Vec
from mat import Mat
from vecutil import list2vec
from matutil import rowdict2mat, mat2coldict, coldict2mat

def load_images(path, n = 20):
    '''
    Input:
        - path: path to directory containing img*.png
        - n: number of images to load
    Output:
        - dict mapping numbers 0 to (n-1) to a list of rows,
          each of which is a list of pixel brightnesses
    '''
    return {i:color2gray(file2image(os.path.join(path,"img%02d.png" % i))) for i in range(n)}

def vec2image(vec, rowsCnt, colsCnt):
    indexes = sorted(list(vec.D))
    result = []
    for i in range(rowsCnt):
        result.append([])
        for j in range(colsCnt):
            result[-1].append(vec[i * colsCnt + j])

    return result

def find_centroid(images):
    return sum(images.values()) / len(images)

def center_images(images, centroid):
    return { key: (val - centroid) for key, val in images.items() }

def projected_representation(M, x):
    return M * x

def projection_length_squared(M, x):
    repr = projected_representation(M, x)
    return repr * repr

def distance_squared(M, x):
    repr = projected_representation(M, x)
    return x * x - repr * repr

def project(M, x):
    coordinates = projected_representation(M, x)
    return coordinates * M

raw_images = load_images('./faces')
rowsCnt = len(raw_images[0])
colsCnt = len(raw_images[0][0])

images = { key: list2vec([ el for row in image for el in row ]) for key, image in raw_images.items() }
centroid = find_centroid(images)
centered_images = center_images(images, centroid)
M = rowdict2mat(centered_images)

print('Factoring...')
U, E, V = factor(M)
print('Done')
print(len(U.D[0]), len(U.D[1]))
print(len(E.D[0]), len(E.D[1]))
print(len(V.D[0]), len(V.D[1]))
print(E[0,0], E[1,1], E[2,2], E[3,3])

orth_basis = rowdict2mat({ key: vec for key, vec in mat2coldict(V).items() if key < 10 })
print(len(orth_basis.D[0]), len(orth_basis.D[1]))
print(len(centered_images[0].D))

print({ key: distance_squared(orth_basis, image) for key, image in centered_images.items() })

print('UNCLASIFIED')
raw_images_uncl = load_images('./unclassified', 10)
images_uncl = { key: list2vec([ el for row in image for el in row ]) for key, image in raw_images_uncl.items() }
centered_images_uncl = center_images(images_uncl, centroid)

dist = { key: distance_squared(orth_basis, image) for key, image in centered_images_uncl.items() }
max = max(dist.values())
dist = { key: val * 100 / max for key, val in dist.items() }

print(dist)

print("Eigen Faces")

for i in range(10):
    projection = project(orth_basis, centered_images_uncl[i]) + centroid
    image2display(vec2image(projection, rowsCnt, colsCnt))
