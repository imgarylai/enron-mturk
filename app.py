import yaml
import json
import os
import jinja2
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import HTMLQuestion
from boto.mturk import qualification

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open("config.yml", 'r') as file:
    cfg = yaml.load(file)

with open('test.json') as data_file:
    data = json.load(data_file)

def render(tpl_path, email):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader = jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(email=email)

# Create your connection to MTurk
mturk = MTurkConnection(aws_access_key_id=cfg['aws_access_key_id'],
                        aws_secret_access_key=cfg['aws_secret_access_key'],
                        host=cfg['host'])
qualification.AdultRequirement(0, False)

account_balance = mturk.get_account_balance()
print("Testing connection: You have a balance of: {}".format(account_balance))

# Disable old hits.
hits = mturk.get_all_hits()
for hit in hits:
    print(mturk.disable_hit(hit.HITId))

# The first parameter is the HTML content
# The second is the height of the frame it will be shown in
# Check out the documentation on HTMLQuestion for more details
for thread in data:
    for email in thread['emails']:
        question_html_value = render('question_tpl.html', email)

        html_question = HTMLQuestion(question_html_value, 500)
        # These parameters define the HIT that will be created
        # question is what we defined above
        # max_assignments is the # of unique Workers you're requesting
        # title, description, and keywords help Workers find your HIT
        # duration is the # of seconds Workers have to complete your HIT
        # reward is what Workers will be paid when you approve their work
        # Check out the documentation on CreateHIT for more details
        response = mturk.create_hit(
            question = html_question,
            max_assignments = 1,
            title = cfg['title'],
            description = cfg['description'],
            keywords = cfg['keywords'],
            duration = 120,
            reward = cfg['reward_amount']
        )

        # The response included several fields that will be helpful later
        hit_type_id = response[0].HITTypeId
        hit_id = response[0].HITId
        print("Your HIT has been created. You can see it at this link:")
        print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
        print("Your HIT ID is: {}".format(hit_id))