import itertools
from mturk import Mturk
import pandas as pd

mturk = Mturk()


if __name__ == '__main__':

    df = pd.DataFrame(columns=['hit_id', 'answer'])

    print("Retrieving answers...")
    for hit in mturk.get_hits():
        assignments = mturk.get_all_assignments(hit.HITId)
        for assignment in assignments:
            print(assignment.WorkerId)
            for answer in assignment.answers:
                print(answer)
                fields = list(itertools.chain.from_iterable([an.fields for an in answer]))
                mturk_df = pd.DataFrame([[hit.HITId, fields]],
                                        columns=['hit_id', 'answer'])
                df = df.append(mturk_df, ignore_index=True)

    print("Saving answers...")
    df.to_csv('result.csv')
