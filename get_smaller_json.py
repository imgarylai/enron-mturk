import json

data_path = 'email.threads.strict.only.ner.json'
outout_path = 'test2.json'

with open(data_path) as data_file:
    data = json.load(data_file)

result = []

for i, d in enumerate(data):
    if i > 100:
        break
    else:
        result.append(d)

with open(outout_path, 'w') as outfile:
    json.dump(result, outfile)

