import json 
from itertools import chain
import numpy as np

def compare(original, tagged):
    result = list()
    
    table = np.zeros((len(original), len(tagged)), dtype=np.uint8)
    
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

train_i = open('./resources/training_simple.json')
train_o = open('./resources/training_simple_noadd.json', mode='w')

for line in train_i:
    line = json.loads(line)
    original = line['original']
    tagged = line['tagged']
    tagged_string = ''.join(token['token'] for token in line['tagged'])
    changes = split_changes(compare(original, tagged_string))
    add_changes = list(chain(*[c for c in changes if '-' not in  list(map(lambda x: x[0], c))]))
    idx_to_remove = [c[3] for c in add_changes]
    line['tagged'] = remove_index(tagged, idx_to_remove)
    train_o.write(json.dumps(line, ensure_ascii=False) + '\n')

train_i.close()
train_o.close()

test_i = open('./resources/test_simple.json')
test_o = open('./resources/test_simple_noadd.json', mode='w')

for line in test_i:
    line = json.loads(line)
    original = line['original']
    tagged = line['tagged']
    tagged_string = ''.join(token['token'] for token in line['tagged'])
    changes = split_changes(compare(original, tagged_string))
    add_changes = list(chain(*[c for c in changes if '-' not in  list(map(lambda x: x[0], c))]))
    idx_to_remove = [c[3] for c in add_changes]
    line['tagged'] = remove_index(tagged, idx_to_remove)
    test_o.write(json.dumps(line, ensure_ascii=False) + '\n')
    
test_i.close()
test_o.close()