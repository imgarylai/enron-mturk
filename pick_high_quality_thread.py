import json
import os
import shutil

source = 'ents'
hq_dist = 'ents_hq'
lq_dist = 'ents_lq'


def check_q(file_path):
    with open(file_path) as data_file:
        thread = json.load(data_file)
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
    q = input('HQ? Y:1 / N:other')
    os.system('cls' if os.name == 'nt' else 'clear')
    return q == '1'


if __name__ == '__main__':

    for dirpath, dnames, fnames in os.walk(source):
        for f in fnames:
            if f.endswith(".json"):
                source_path = os.path.join(dirpath, f)
                if check_q(os.path.join(dirpath, f)):
                    dist_path = "{}/{}".format(hq_dist,f)
                else:
                    dist_path = "{}/{}".format(lq_dist, f)
                shutil.move(source_path, dist_path)
