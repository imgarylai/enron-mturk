import json
from mturk import Mturk
import pandas as pd

data_path = 'test.json'

with open(data_path) as data_file:
    data = json.load(data_file)

# Create your connection to MTurk
mturk = Mturk()
mturk.account_balance()
mturk.remove_old_hits()

df = pd.DataFrame(columns=['path', 'hit_id'])

for thread in data:
    for email in thread['emails']:
        try:
            response = mturk.create_hit(email)
        except Exception as e:
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