import pandas as pd
import math

filename="ner/maildir/arnold-j/deleted_items/176./2.tsv"
df = pd.read_csv(filename, sep = '\t', header=None, usecols=[2, 8], quotechar='"')

tags = []
for i in df.iterrows():
    tags.append((i[1][2], i[1][8]))

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
        print(tag[0])
        print(result)
    return result

print(group(tags))