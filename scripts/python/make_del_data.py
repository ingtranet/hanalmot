import json
from itertools import chain

import numpy as np
from progress.bar import ShadyBar

from util import compare

def make_del_data(input_path, output_path, max=None):
    i_file = open(input_path)
    o_file = open(output_path, mode='w')
    
    with ShadyBar(f'make {output_path}', max=max) as bar:
        for line in i_file:
            line = json.loads(line)
            t_original = line['original']
            t_tagged = ''.join([t['token'] for t in line['tagged']])
            compared = compare(t_original, t_tagged)
            deleted_indices = {c[2] for c in compared if c[0] == '-'}
            arr = np.zeros((len(t_original),), dtype=np.uint8)
            for i in deleted_indices:
                arr[i] = 1
            arr = ''.join(str(i) for i in arr)
            o_file.write(f"{t_original}\t{arr}\n")
            bar.next()

        i_file.close()
        o_file.close()

make_del_data('./resources/training_simple.json', './resources/training_del_indices.tsv', 1718806)
make_del_data('./resources/test_simple.json', './resources/test_del_indices.tsv', 190985)
        