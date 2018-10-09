from dictutil import dict2list, list2dict

docs = open("stories_big.txt")

def makeInverseIndex(strlist):
    inverseIndex = {}
    for (i, doc) in enumerate(strlist):
        for word in doc.split():
            if word in inverseIndex:
                inverseIndex[word].add(i)
            else:
                inverseIndex[word] = set()
                inverseIndex[word].add(i)
    return inverseIndex

def orSearch(inverseIndex, query):
    return list({ doc_i for word in query if word in inverseIndex for doc_i in inverseIndex[word] })

def andSearch(inverseIndex, query):
    result = inverseIndex[query[0]]

    for word in query[1:]:
        if not word in inverseIndex:
            continue;

        result = result & inverseIndex[word]

    return list(result)

inverseIndex = makeInverseIndex(docs)
print(orSearch(inverseIndex, ['nigger', 'Jaguar']))
print(andSearch(inverseIndex, ['nigger', 'Jaguar']))
