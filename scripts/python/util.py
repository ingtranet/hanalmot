import json 
from itertools import chain
import numpy as np

simple_pos_iv = {
    'Noun': ('NNB', 'NNG', 'NNP', 'XR', 'XSN', 'NN', 'N'),
    'Number': ('NR',), 
    'Pronoun': ('NP',), 
    'Determiner': ('MM', 'XPN', 'XP', 'M'), 
    'Adverb' : ('MAG', 'MAJ', 'MA'), 
    'Josa': ('JC', 'JKB', 'JKC', 'JKG', 'JKO', 'JKQ', 'JKS', 'JKV', 'JX', 'JK', 'J'),
    'Exclamation': ('IC', 'I'),
    'Adjective' : ('VA', 'VCN', 'VCP', 'XSA', 'VC'), 
    'Verb': ('VV', 'VX', 'XSV', 'V', 'XS', 'XSB'),
    'Eomi': ('EC', 'EF', 'EP', 'ETM', 'ETN', 'E', 'ET'), 
    'Unk': ('NA',), 
    'Symbol': ('SE', 'SF', 'SH', 'SL', 'SN', 'SO', 'SP', 'SS', 'SW', 'S'),
    'Space': ('Space',)
}

simple_pos = dict()
for k, v in simple_pos_iv.items():
    for p in v:
        simple_pos[p] = k

def compare(original, tagged):
    result = list()
    
    table = np.zeros((len(original), len(tagged)), dtype=np.uint16)
    
    for i, o in enumerate(original):
        for j, t in enumerate(tagged):
            if original[i] == tagged[j]:
                table[i][j] = table[max(i-1, 0)][max(j-1, 0)] + 1
            else:
                table[i][j] = max(table[i][max(j-1, 0)], table[max(i-1, 0)][j])
    
    i, j = table.shape
    i -= 1
    j -= 1
    while i != 0 and j != 0:
        if original[i] == tagged[j]:
            i -= 1
            j -= 1
        else:
            if table[i-1][j] >= table[i][j-1]:
                result.append(('-', original[i], i,  j))
                i -= 1
            else:
                result.append(('+', tagged[j], i,  j))
                j -= 1
    
    return result

def split_changes(changes):
    result = list()
    q = list()
    for c in changes:
        if not q:
            q.append(c)
            continue
            
        if c[2] == q[-1][2] or c[3] == q[-1][3]:
            q.append(c)
        else:
            result.append(q)
            q = list()
            q.append(c)
    if q:
        result.append(q)
    return result

def remove_index(parsed, idxs):
    i = 0
    idxs = set(idxs)
    for t in parsed:
        ids = list()
        for c in t['token']:
            ids.append(i)
            i += 1
        t['ids'] = set(ids)
    
    result = list()
    for t in parsed:
        if t['ids'] & idxs:
            continue
        else:
            del t['ids']
            result.append(t)
            
    return result