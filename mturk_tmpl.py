import cgi
import os
import jinja2
from boto.mturk.question import HTMLQuestion
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ReceiversTooMuch(Error):
    pass

class TokenLength(Error):
    pass

class MturkTmpl():
    def render(self, tpl_path, email):
        path, filename = os.path.split(tpl_path)
        return jinja2.Environment(
            loader = jinja2.FileSystemLoader(path or './')
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
        # if len(data['token']) > 250 or len(data['token']) < 10:
        #     raise TokenLength
        receivers = '/'.join(receivers)
        data['receivers'] = cgi.escape(receivers)
        question_html_value = self.render('question_tpl.html', data)

        # The first parameter is the HTML content
        # The second is the height of the frame it will be shown in
        # Check out the documentation on HTMLQuestion for more details
        return HTMLQuestion(question_html_value, 500)

