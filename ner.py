import json
import pandas as pd
from tqdm import tqdm

data_path = 'email.threads.strict.only.json'
outout_path = 'email.threads.strict.only.ner.json'

with open(data_path) as data_file:
    data = json.load(data_file)

def group(tags):
    start = None
    result = []
    for i, tag in enumerate(tags):
        if tag[1].startswith('O'):
            if start is not None:
                type = tags[start][1].split("-")[1]
                word = " ".join([str(text[0]) for text in tags[start:i]])
                result.append((word, type))
                result.append(tag)
                start = None
            else:
                result.append(tag)
        elif tag[1].startswith('B'):
            start = i
        elif tag[1].startswith('U'):
            type = tag[1].split("-")[1]
            word = tag[0]
            result.append((word, type))
            if start is not None:
                result.append(tag)
                start = None
        elif tag[1].startswith('L'):
            type = tags[start][1].split("-")[1]
            word = " ".join([str(text[0]) for text in tags[start:i+1]])
            result.append((word, type))
            start = None
        else:
            continue
    return result

for thread in tqdm(data):
    for i, email in enumerate(thread['emails']):
        filename = "ner/{}/{}.tsv".format(thread['path'],i)
        df = pd.read_csv(filename, sep='\t', header=None, usecols=[2, 8], quotechar='\t')

        tags = [(i[1][2], i[1][8]) for i in df.iterrows()]

        try:
            email['ents'] = group(tags)
        except TypeError:
            email['ents'] = []

with open(outout_path, 'w') as outfile:
    json.dump(data, outfile)