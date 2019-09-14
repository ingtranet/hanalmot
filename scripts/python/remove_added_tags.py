import json 
from itertools import chain
import numpy as np

from util import split_changes, compare, remove_index

train_i = open('./resources/training_simple.json')
train_o = open('./resources/training_simple_noadd.json', mode='w')

for line in train_i:
    line = json.loads(line)
    original = line['original']
    tagged = line['tagged']
    tagged_string = ''.join(token['token'] for token in line['tagged'])
    changes = split_changes(compare(original, tagged_string))
    add_changes = list(chain(*[c for c in changes if '-' not in list(map(lambda x: x[0], c))]))
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
    add_changes = list(chain(*[c for c in changes if '-' not in list(map(lambda x: x[0], c))]))
    idx_to_remove = [c[3] for c in add_changes]
    line['tagged'] = remove_index(tagged, idx_to_remove)
    test_o.write(json.dumps(line, ensure_ascii=False) + '\n')
    
test_i.close()
test_o.close()