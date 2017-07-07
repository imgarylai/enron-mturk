import os
import jinja2
from boto.mturk.question import HTMLQuestion
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf-8')


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ReceiversTooMuch(Error):
    pass


class TokenLength(Error):
    pass


class MturkTmpl():

    @staticmethod
    def render(tpl_path, email):
        path, filename = os.path.split(tpl_path)
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename).render(email=email)

    def html_question(self, data):
        receivers = []
        for r in ['To', 'Cc', 'Bcc']:
            try:
                res = data[r]
                receivers.extend(res)
            except KeyError:
                continue
        if len(receivers) > 15:
            raise ReceiversTooMuch
        data['receivers'] = receivers
        question_html_value = self.render('question_tpl.html', data)

        # The first parameter is the HTML content
        # The second is the height of the frame it will be shown in
        # Check out the documentation on HTMLQuestion for more details
        return HTMLQuestion(question_html_value, 500)

# if __name__ == '__main__':
