from vec import Vec

def list2vec(L):
    return Vec(set(range(len(L))), {k:x for k,x in enumerate(L)})
