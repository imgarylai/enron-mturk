import json
import os
import random

data_path = 'email.threads.strict.only.ner.json'
high_quality_thread_path = 'email.threads.strict.only.ner.hq.json'

with open(data_path) as data_file:
    data = json.load(data_file)

if __name__ == '__main__':
    result = []
    thread_count = 0
    random.shuffle(data)
    for i, thread in enumerate(data):
        for email in thread['emails']:
            receivers = []
            for r in ['To', 'Cc', 'Bcc']:
                try:
                    res = email[r]
                    receivers.extend(res)
                except KeyError:
                    continue
            try:
                print("Sender: {}".format(email['From']))
            except KeyError:
                continue
            print("----------")
            print("Receivers: {}".format(",".join(receivers)))
            print("----------")
            print("Body:")
            print("==========")
            print(email["body"])
            print("==========")
        print("Thread: {}, HQ threads: {}".format(i, thread_count))
        q = raw_input('HQ? Y:1/N:other')
        os.system('cls' if os.name == 'nt' else 'clear')
        if q == '1':
            result.append(thread)
            thread_count += 1
            with open(high_quality_thread_path, 'w') as outfile:
                json.dump(result, outfile, indent = 2)
        else:
            continue
