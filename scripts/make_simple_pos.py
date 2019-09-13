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

import json

train_i = open('./resources/training.json')
train_o = open('./resources/training_simple.json', mode='w')

for line in train_i:
    line = json.loads(line)
    for token in line['tagged']:
        token['tag'] = simple_pos[token['tag']]
    train_o.write(json.dumps(line, ensure_ascii=False) + '\n')
train_i.close()
train_o.close()

test_i = open('./resources/test.json')
test_o = open('./resources/test_simple.json', mode='w')

for line in test_i:
    line = json.loads(line)
    for token in line['tagged']:
        token['tag'] = simple_pos[token['tag']]
    test_o.write(json.dumps(line, ensure_ascii=False) + '\n')
test_i.close()
test_o.close()