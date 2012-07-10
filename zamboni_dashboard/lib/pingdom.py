import json

import requests


class Pingdom(object):

    ENDPOINT = 'https://api.pingdom.com/api/2.0'
    
    def __init__(self, user, password, key):
        self.user = user
        self.password = password
        self.key = key

    def checks(self):
        """Returns a list of checks"""
        return self._fetch('checks')['checks']
    
    def summary(self, check_id):
        """Returns summary of response time and uptime for check"""
        return self._fetch('summary.average/%s' % check_id,
                           {'includeuptime': 'true'})

    def _fetch(self, resource, params=None):
        headers = {'App-Key': self.key}
        r = requests.get("%s/%s" % (self.ENDPOINT, resource),
                         headers=headers, auth=(self.user, self.password),
                         params=params)
        return r.json
