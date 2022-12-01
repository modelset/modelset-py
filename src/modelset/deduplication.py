"""
This module is in charge of enabling the deduplication functionality of ModelSet. This is useful to detect duplicate models and filter them when using the dataset. For this, see method get_duplicates of the Dataset class in dataset.py.
"""
from collections import defaultdict
from re import finditer

from tqdm import tqdm


def tokenizer(doc):
    def camel_case_split(identifier):
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]

    words = doc.split()
    words = [w2 for w1 in words for w2 in w1.split('_') if w2 != '']
    words = [w2.lower() for w1 in words for w2 in camel_case_split(w1) if w2 != '']
    return words


def get_multiset(data):
    multiset = defaultdict(int)
    for w in data:
        multiset[w.lower()] += 1
    return multiset


def jaccard_keys(multi1, multi2):
    x = multi1.keys()
    y = multi2.keys()
    intersection_cardinality = len(set(x).intersection(set(y)))
    union_cardinality = len(set(x).union(set(y)))
    return intersection_cardinality / float(union_cardinality)


def jaccard_generalized(multi1, multi2):
    sum_num = 0
    sum_den = 0
    for k in multi1:
        if k in multi2:
            sum_num += min(multi1[k], multi2[k])
            sum_den += max(multi1[k], multi2[k])
        else:
            sum_den += multi1[k]
    for k in multi2:
        if k not in multi1:
            sum_den += multi2[k]
    return float(sum_num) / float(sum_den)


def get_duplicates(multisets, ids, t0, t1):
    dup = {}
    words = {}
    for j, id in tqdm(enumerate(ids), desc='Duplicates main loop'):
        words[id] = multisets[j]
        bdup = False
        for id2 in dup:
            for id3 in dup[id2] + [id2]:
                if (jaccard_keys(words[id], words[id3]) > t0 and
                        jaccard_generalized(words[id], words[id3]) > t1):
                    dup[id2].append(id)
                    bdup = True
                    break
            if bdup:
                break
        if not bdup:
            dup[id] = []
    return dup
