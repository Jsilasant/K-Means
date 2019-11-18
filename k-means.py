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



def SSE(cluster, centroids, terms_all, l, k):
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
    print('number of k = ', k, file=f)
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
        print(i + 1, ', size of cluster: ', len([id[x] for x in t]) , file = f)


terms_all = []
id = []
#Random Centroids
centroids = [550684907186704385,552497754334064640,550722415693529088,569881582552657920,552453181016645634,
             550651682091446273,549982055854247936,585851005935476736,583078992103768064,581551315488239617,
             580811556977528833,580089214840266752,579301491271434241,578609645532667904,578235848627470336,
             577646889237155840,577109582285262848,576475398235668480,576188449461534720,575783385441943553,
             575478845228253186,574615897782009856,573671911600881664,571516416744161280,570234232477495297]
n = open('usnewshealth.txt', encoding='utf-8')
for line in n.readlines():
    tweet = line.split('|')
    tokens = preprocess(tweet[2])
    terms_all.append([term for term in tokens])
    id.append(int(tweet[0]))
l=len(terms_all)
f = open('output.txt', 'w')
#the integer value that is currently after l can be changed to the number of centroids that you would want to run.
#Up to 25
kmeans(id,centroids,terms_all,l,25)
