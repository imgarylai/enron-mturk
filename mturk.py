import itertools
import yaml
from boto.mturk.connection import MTurkConnection, MTurkRequestError
from mturk_tmpl import MturkTmpl, ReceiversTooMuch, TokenLength

class Mturk():
    def __init__(self):
        self.config = self.set_config()
        self.mturk = MTurkConnection(aws_access_key_id = self.config['aws_access_key_id'],
                                     aws_secret_access_key = self.config['aws_secret_access_key'],
                                     host = self.config['host'])
        self.mturk_tmpl  = MturkTmpl()

    def set_config(self, config_path = "config.yml"):
        with open(config_path, 'r') as file:
            config = yaml.load(file)
        return config

    def account_balance(self):
        account_balance = self.mturk.get_account_balance()
        print("Testing connection: You have a balance of: {}".format(account_balance))

    def get_hits(self):
        return self.mturk.get_all_hits()

    def get_all_assignments(self, hit_id):
        page_size = 100
        assignments = self.mturk.get_assignments(hit_id, page_size = page_size)
        total_records = int(assignments.TotalNumResults)
        get_page_assignments = lambda page: self.mturk.get_assignments(hit_id,
            page_size=page_size,
            page_number=page)
        page_nums = self.mturk._get_pages(page_size, total_records)
        assignments_sets = itertools.imap(get_page_assignments, page_nums)
        return itertools.chain.from_iterable(assignments_sets)

    def remove_old_hits(self):
        # Disable old hits.
        for hit in self.get_hits():
            print("Hit {} has been removed.".format(hit.HITId))
            self.mturk.disable_hit(hit.HITId)

    def cal_reward(self, data):
        read_instruction = 3.0
        word_count = len(data['ents']) * 1/30.0
        return round((read_instruction + word_count) / 60.0 * 6.0, 2)


    def create_hit(self, data):
        # These parameters define the HIT that will be created
        # question is what we defined above
        # max_assignments is the # of unique Workers you're requesting
        # title, description, and keywords help Workers find your HIT
        # duration is the # of seconds Workers have to complete your HIT
        # reward is what Workers will be paid when you approve their work
        # Check out the documentation on CreateHIT for more details
        response = self.mturk.create_hit(
            question = self.mturk_tmpl.html_question(data),
            max_assignments = 2,
            title = self.config['title'],
            description = self.config['description'],
            keywords = self.config['keywords'],
            duration = 120,
            reward = self.cal_reward(data)
        )
        return response

if __name__ == '__main__':
    m = Mturk()
    print(m.mturk.get_account_balance())