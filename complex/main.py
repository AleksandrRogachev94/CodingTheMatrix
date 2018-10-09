def my_filter(L, num):
    return [ el for el in L if el % 2 != 0 ]

arr = [1,2,4,5,7]; num = 2

print(my_filter(arr, num))

def my_lists(L):
    return [ list(range(1, el + 1)) for el in L ]

print(my_lists([1,2,4]))
print(my_lists([0]))

def my_function_composition(f, g):
    return { key: g[f[key]] for key in f.keys() }

print(my_function_composition({0:"a", 1:"b"}, {"a":"apple", "b":"banana"}))

def transform(a, b, L):
    return [ a * z + b for z in L ]

a = 1j
b = 1 + 1j
L = [1 + 1j]

print(transform(a, b, L))
