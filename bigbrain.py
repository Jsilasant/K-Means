import sys
import json
import re
import copy
import math

#intial data cleaning and preprocessing using regular expressions

regex_str = [
     r'<[^>]+>', 
    r'(?:@[\w_]+)', 
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", 
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', 
    r"(?:[a-z][a-z'\-_]+[a-z])", 
    r'(?:[\w_]+)', 
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens

def jaccard(a,b):
	inter= list(set(a) & set(b))
	I=len(inter)
	union= list(set(a) | set(b))
	U=len(union)
	return round(1-(float(I)/U),4)



def SSE(cluster, centroids, terms_all, k, l):
    indices1 = []
    indices = [id.index(item) for item in centroids]
    cen_txt = [terms_all[x] for x in indices]
    sum = 0
    for i in range(k):
        indices1.append([j for j, u in enumerate(cluster) if u == i])
        # print indices1[i]
        t = [terms_all[x] for x in indices1[i]]
        for j in range(len(indices1[i])):
            sum = sum + math.pow(jaccard(t[j], cen_txt[i]), 2)
    print('SSE', sum, file=f)

def kmeans(id, centroids, terms_all, l, k):
    count = 0 
    for h in range(k):
        count  = count + 1
        indices = [id.index(item) for item in centroids]
        cen_txt = [terms_all[x] for x in indices]
        cluster = []
        for i in range(l):
            d = [jaccard(terms_all[i], cen_txt[j]) for j in range(k)]
            ans = d.index(min(d))
            cluster.append(ans)

        centroids1 = update(id, cluster, terms_all, l, k)
        sum = 0 
        for i in range(k):
            if ( centroids1[i] == centroids[i]):
                sum = sum +1
        if(sum == k):
            break
        centroids = copy.deepcopy(centroids1)
    
    output(cluster, k, id)
    SSE(cluster, centroids, terms_all, k , l)
    f.close()

def update(id, cluster, terms_all, l, k):
    indices = []
    new_centroid_index = []
    new_centroid = []
    for i in range(k):
        indices.append([j for j, u in enumerate(cluster) if u == i])
        m = indices[i]

        if(len(m) != 0 ):
            txt = [terms_all[p] for p in m]
            sim = [[jaccard(txt[i], txt[j]) for j in range(len(m))] for i in range(len(m))]
            floor = [sum(i) for i in sim]

        new_centroid_index.append(m[(floor.index(min([sum(i) for i in sim])))])
    new_centroid = [id[x] for x in new_centroid_index]
    return new_centroid

def output(cluster, k, id):
    final = []
    for i in range(k):
        final.append([j for j, u in enumerate(cluster) if u == i])
        t = [x for x in final[i]]
        print(i + 1, [id[x] for x in t] , file = f)


terms_all = []
id = []
centroids = [581465076458106880,581189107105161216,581141361031712769,581141360352239616,581141359664328706]
n = open('cbchealth.txt', encoding='utf-8')
for line in n.readlines():
    tweet = line.split('|')
    tokens = preprocess(tweet[2])
    terms_all.append([term for term in tokens])
    id.append(int(tweet[0]))
l=len(terms_all)
f = open('output.txt', 'w')
kmeans(id,centroids,terms_all,l,5)