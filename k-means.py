import sys
import re
import math
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans


regex_str = [r'<[^>]+>',
    r'(?:@[\w_]+)',
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',
    r"(?:[a-z][a-z'\-_]+[a-z])",
    r'(?:[\w_]+)',]

token_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)

def tokenchar(s):
    return token_re.findall(s)

def preprocess(s, lowercase=True):
    tokens = tokenchar(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens

def jaccard(a, b):
    inter = list(set(a) & set(b))
    I = len(inter)
    union = list(set(a) | set(b))
    U = len(union)
    return round(1 - (float(I) / U), 4)

