# Author: Jethjera Silasant, Jonny Le
# CS 4375.002
# University of Texas at Dallas
# Fall 2019
#
# Usage: kmeans-tweets.py N_CLUSTERS SEED FILE

import sys
import re
import copy
import math
import random

# Preprocess data:
# Removes URL links, # symbol, and words beginning with @
# Converts to lowercase
def preprocess(s):
    preprocessed_s = re.sub(r'https?://(?:[\w_./]+)', '', s.lower())
    preprocessed_s = re.sub('[#]', '', preprocessed_s)
    preprocessed_s = re.sub(r'(?:@[\w_]+)', '', preprocessed_s)
    return preprocessed_s

# Jaccard Distance
def jaccard(a,b):
	inter= list(set(a) & set(b))
	I=len(inter)
	union= list(set(a) | set(b))
	U=len(union)
	return round(1-(float(I)/float(U)),4)

# Sum of Squared Errors
def SSE(cluster, centroids, terms_all, tweet_id, k):
    indices1 = []
    indices = [tweet_id.index(item) for item in centroids]
    cen_txt = [terms_all[x] for x in indices]
    sum = 0
    for i in range(k):
        indices1.append([j for j, u in enumerate(cluster) if u == i])
        t = [terms_all[x] for x in indices1[i]]
        for j in range(len(indices1[i])):
            sum = sum + math.pow(jaccard(t[j], cen_txt[i]), 2)
    print('SSE:', round(sum, 4))
    
# K-Means Implementation
def kmeans(tweet_id, centroids, terms_all, l, k):
    count = 0 
    for h in range(k):
        count  = count + 1
        indices = [tweet_id.index(item) for item in centroids]
        cen_txt = [terms_all[x] for x in indices]
        cluster = []
        for i in range(l):
            d = [jaccard(terms_all[i], cen_txt[j]) for j in range(k)]
            ans = d.index(min(d))
            cluster.append(ans)

        centroids1 = update(tweet_id, cluster, terms_all, l, k)
        sum = 0 
        for i in range(k):
            if ( centroids1[i] == centroids[i]):
                sum = sum +1
        if(sum == k):
            break
        centroids = copy.deepcopy(centroids1)
    
    # Print results
    print('K-Means for k =', k)
    output(cluster, k, tweet_id)
    SSE(cluster, centroids, terms_all, tweet_id, k)

# Updates new centroids at each iteration
def update(tweet_id, cluster, terms_all, l, k):
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
    new_centroid = [tweet_id[x] for x in new_centroid_index]
    return new_centroid

# Output of K-Means:
# Prints size of each cluster
def output(cluster, k, tweet_id):
    final = []
    for i in range(k):
        final.append([j for j, u in enumerate(cluster) if u == i])
        t = [x for x in final[i]]
        print('%3d. size of cluster: %d' %(i+1, len([tweet_id[x] for x in t])))

# Gets inital random centroids for K-Means
def getrandcentroids(seed, k, ids):
    random.seed(seed)
    rand_indexes = []
    i = k
    while(i != 0):
        rand_num = random.randrange(0, len(ids))
        if rand_num in rand_indexes:
            continue
        rand_indexes.append(rand_num)
        i -= 1

    centroids = []
    for val in rand_indexes:
        centroids.append(ids[val])
    return centroids

def main():
    if len(sys.argv) != 4:
        print('Usage: %s N_CLUSTERS SEED FILE' %(sys.argv[0]))
        sys.exit(1)
    
    try:
        k = int(sys.argv[1])
        seed = int(sys.argv[2])
    except TypeError:
        print('K and seed must be an integer.')
        sys.exit(1)

    if k <= 0:
        print('K value must be greater than 0.')
        sys.exit(1)
    if seed < 0:
        print('Seed value must be a non-negative number.')
        sys.exit(1)
    file_name = sys.argv[3]

    terms_all = []
    tweet_id = []
    try:
        f = open(file_name, encoding='utf-8')
        for line in f.readlines():
            tweet = line.split('|')
            preprocessed_s = preprocess(tweet[2])
            terms_all.append([term for term in preprocessed_s.split()])
            tweet_id.append(int(tweet[0]))
    except IOError:
        print('Could not read file:', file_name)
        sys.exit(1)
    f.close()

    centroids = getrandcentroids(seed, k, tweet_id)
    l=len(terms_all)
    kmeans(tweet_id,centroids,terms_all,l,k)

if __name__ == '__main__':
    main()