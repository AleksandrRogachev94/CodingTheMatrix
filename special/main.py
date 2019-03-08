from math import sqrt

def forward_no_normalization(v):
    D = {}

    while len(v) > 1:
        k = len(v)
        w = [ (v[2 * i] - v[2 * i + 1]) for i in range(k // 2) ]
        v = [ (v[2 * i] + v[2 * i + 1]) / 2 for i in range(k // 2) ]

        D.update({ (k // 2, i): w[i] for i in range(k // 2) })

    D[(0, 0)] = v[0]
    return D

def backward_no_normalization(D):
    v = [D[0, 0]]

    while len(v) < len(D):
        k = 2 * len(v)
        v = [
            v[i // 2] + (0.5 if i % 2 == 0 else -0.5) * D[k // 2, i // 2]
        for i in range(k) ]

    return v

def normalize_coefficients(n, D):
    D[(0, 0)] *= sqrt(n)
    for i, j in D.keys():
        if i != 0:
            D[(i, j)] *= sqrt(n / (4 * i))

    return D

def unnormalize_coefficients(n, D):
    D[(0, 0)] /= sqrt(n)
    for i, j in D.keys():
        if i != 0:
            D[(i, j)] /= sqrt(n / (4 * i))

    return D

def forward(v):
    D = forward_no_normalization(v)
    return normalize_coefficients(len(v), D)

def backward(D):
    D = unnormalize_coefficients(len(D.keys()), D)
    return backward_no_normalization(D)

def suppress(D, threshold):
    return { key: value if abs(value) >= threshold else 0 for key, value in D.items() }

def sparsity(D):
    return sum(abs(val) > 1.e-15 for val in D.values()) / len(D.values())

print(forward([1,2,3,4]))
print(suppress(forward([1,2,3,4]), 1))
print(sparsity(suppress(forward([1,2,3,4]), 1)))
print(backward(forward([1,2,3,4])))

print(backward(suppress(forward([1,2,3,4]), 1)))
