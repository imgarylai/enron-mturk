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

    def remove_old_hits(self):
        # Disable old hits.
        for hit in self.mturk.get_all_hits():
            print("Hit {} has been removed.".format(hit.HITId))
            self.mturk.disable_hit(hit.HITId)

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
            max_assignments=1,
            title = self.config['title'],
            description = self.config['description'],
            keywords = self.config['keywords'],
            duration = 120,
            reward = self.config['reward_amount']
        )
        return response



if __name__ == '__main__':
    m = Mturk()
    print(m.mturk.get_account_balance())