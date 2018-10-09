f = open('voting_record_dump109.txt')
mylist = list(f)

def create_voting_dict(strlist):
    dict = {}
    for str in strlist:
        parsed = str.split()
        dict[parsed[0]] = [ int(num) for num in parsed[3:] ]

    return dict

def dot(l1, l2):
    assert len(l1) == len(l2)
    return sum([ l1[i] * l2[i] for i in range(len(l1)) ])

def policy_compare(sen_a, sen_b, dict):
    return dot(dict[sen_a], dict[sen_b])

def most_similar(sen, dict):
    max = -1
    max_sen = None
    for sen_b, vec in dict.items():
        if(sen_b == sen):
            continue;

        sim = dot(dict[sen], vec)
        if sim > max:
            max = sim
            max_sen = sen_b

    return (max, max_sen)

def least_similar(sen, dict):
        min = -1
        min_sen = None
        for sen_b, vec in dict.items():
            if(sen_b == sen):
                continue;

            sim = dot(dict[sen], vec)
            if min < 0 or sim < min:
                min = sim
                min_sen = sen_b

        return (min, min_sen)


dict = create_voting_dict(mylist)
print(policy_compare('Santorum', 'Specter', dict))
print(most_similar("Chafee", dict))
print(least_similar("Santorum", dict))
