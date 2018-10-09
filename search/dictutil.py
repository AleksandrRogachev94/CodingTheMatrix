# Copyright 2013 Philip N. Klein
def dict2list(dct, keylist):
    return [dct[key] for key in keylist]

def list2dict(L, keylist):
    return {key:el for key, el in zip(keylist, L)}

def listrange2dict(L):
    return { i:el for (i, el) in enumerate(L) }
