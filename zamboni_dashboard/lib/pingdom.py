import json
from hashlib import md5

import requests


class Pingdom(object):

    ENDPOINT = 'https://api.pingdom.com/api/2.0'
    
    def __init__(self, user, password, key, cache=None):
        self.user = user
        self.password = password
        self.key = key
        self.cache = cache

    def checks(self, with_summary=False, refresh=False):
        """Returns a list of checks"""
        checks = self._fetch('checks', refresh=refresh)['checks']

        if with_summary:
            for c in checks:
                s = self.summary(c['id'], refresh)
                c['avg_response'] = s['responsetime']['avgresponse']
                
                status = s['status']
                c['uptime'] = float(status['totalup']) / (status['totalup'] + status['totaldown'])

        return checks

    def summary(self, check_id, refresh=False):
        """Returns summary of response time and uptime for check"""
        return self._fetch('summary.average/%s' % check_id,
                           {'includeuptime': 'true'},
                           refresh=refresh)['summary']
    
    def _obj_cache_key(self, func, *args):
        key = 'pingdom:%s:%s:%s:%s:%s' % (self.user, self.password, self.key,
                                               func, md5(str(args)).hexdigest())
        return md5(key).hexdigest()

    def _fetch(self, resource, params=None, refresh=False):
        key = self._obj_cache_key('_fetch', resource, params)
        if not refresh and self.cache:
            res = self.cache.get(key)
            if res:
                return res

        headers = {'App-Key': self.key}
        r = requests.get("%s/%s" % (self.ENDPOINT, resource),
                         headers=headers, auth=(self.user, self.password),
                         params=params)
        res = r.json

        if self.cache:
            self.cache.set(key, res, timeout=150)

        return res
