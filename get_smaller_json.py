import json
import os

hq_dist = 'ents_hq'

if __name__ == '__main__':

    result = []
    for dirpath, dnames, fnames in os.walk(hq_dist):
        for f in fnames:
            if f.endswith(".json"):
                path = os.path.join(dirpath, f)
                with open(path) as j:
                    data = json.load(j)
                result.append(data)

    with open('email.threads.strict.only.ents.json', 'w') as f:
        json.dump(result,f, indent=2)
