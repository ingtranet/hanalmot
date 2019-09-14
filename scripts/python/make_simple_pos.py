import json

from progress.bar import ShadyBar

from util import simple_pos

with ShadyBar("training.json to simple pos", max=1718806) as bar:
    train_i = open('./resources/training.json')
    train_o = open('./resources/training_simple.json', mode='w')

    for line in train_i:
        line = json.loads(line)
        for token in line['tagged']:
            token['tag'] = simple_pos[token['tag']]
        train_o.write(json.dumps(line, ensure_ascii=False) + '\n')
        bar.next()

    train_i.close()
    train_o.close()

with ShadyBar("test.json to simple pos", max=190977) as bar:
    test_i = open('./resources/test.json')
    test_o = open('./resources/test_simple.json', mode='w')

    for line in test_i:
        line = json.loads(line)
        for token in line['tagged']:
            token['tag'] = simple_pos[token['tag']]
        test_o.write(json.dumps(line, ensure_ascii=False) + '\n')
        bar.next()
        
    test_i.close()
    test_o.close()