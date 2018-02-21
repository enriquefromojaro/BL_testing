import requests


class OnlineInformation(object):

    def __init__(self, name):
        self.t_name = name

    @property
    def url(self):
        return 'https://www.qwertee.com/product/{}'.format(self.t_name)

    @staticmethod
    def get_online_info(url):
        resp = requests.get(url)
        if not resp.ok:
            raise ValueError('Invalid response. Status: %s' % resp.status_code)
        return resp.text[:50]

    def get_info(self):
        url = self.url
        return self.get_online_info(url)