from mturk import Mturk
import ujson as json
import pandas as pd

source = 'tsv/'
enron_json = 'email.threads.strict.only.ner.json'

with open(enron_json) as data_file:
    data = json.load(data_file)

df = pd.DataFrame(columns=['path', 'hit_id'])

if __name__ == '__main__':
    # Create your connection to MTurk
    mturk = Mturk()
    mturk.account_balance()
    mturk.remove_old_hits()

    for thread in data:
        for email in thread['emails']:
            try:
                response = mturk.create_hit(email)
            except Exception as e:
                print(e.message)
                continue

            # The response included several fields that will be helpful later
            hit_type_id = response[0].HITTypeId
            hit_id = response[0].HITId
            print("Your HIT has been created. You can see it at this link:")
            print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
            print("Your HIT ID is: {}".format(hit_id))
            mturk_df = pd.DataFrame([[thread['path'], hit_id]],
                                    columns=['path', 'hit_id'])
            df = df.append(mturk_df, ignore_index=True)

            df.to_csv('hit.csv')
