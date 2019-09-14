import re
import json
import subprocess

from progress.bar import ShadyBar

def parse_tagged(text):
    tokens = list()
    for ejol in text.split(' '):
        for parsed in re.split(r'[A-Z]\+', ejol):
            tag = parsed[parsed.rindex('/') + 1:]
            if '_' in parsed:
                token = parsed[:parsed.index('_')]
            else:
                token = parsed[:parsed.rindex('/')]
            tokens.append({
                'token': token,
                'tag': tag
            })
        tokens.append({
            'token': ' ',
            'tag': 'Space'
        })
    return tokens[:-1]

with ShadyBar('make training.json file', max=5156589) as bar:
    i_training = open('./resources/training_corpus_exbrain.txt', 'rb')
    o_training = open('./resources/training.json', mode='w', encoding='utf-8')

    success = 0
    failed = 0

    while True:
        try:
            line1 =  i_training.readline().replace(b'\r\n', b'')
            line2 =  i_training.readline().replace(b'\r\n', b'')
            line3 =  i_training.readline().replace(b'\r\n', b'')

            if not line1:
                break

            output = dict()
            output['original'] = line1.decode('cp949')
            output['tagged'] = parse_tagged(line2.decode('cp949').replace('+ ', ''))

            o_training.write(json.dumps(output, ensure_ascii=False) + '\n')
            success += 1
        except Exception as e:
            failed += 1
        finally:
            bar.next(3)
            
    i_training.close()
    o_training.close()

    print(f'\nfinished: success: {success}, failed: {failed}')

with ShadyBar('make test.json file', max=190985) as bar:
    i_test = open('./resources/test_exbrain.txt', mode='rb')
    i_answer = open('./resources/answer_exbrain.txt', mode='rb')
    o_test = open('./resources/test.json', mode='w', encoding='utf-8')

    success = 0
    failed = 0
    while True:
        try:
            line1 = i_test.readline().replace(b'\r\n', b'')
            line2 = i_answer.readline().replace(b'\r\n', b'')

            if not line1:
                break

            output = dict()
            output['original'] = line1.decode('cp949')
            output['tagged'] = parse_tagged(line2.decode('cp949').replace('+ ', ''))

            o_test.write(json.dumps(output, ensure_ascii=False) + '\n')
            success += 1
        except Exception as e:
            failed += 1
        finally:
            bar.next()
            
    i_test.close()
    i_answer.close()
    o_test.close()

    print(f'\nfinished: success: {success}, failed: {failed}')