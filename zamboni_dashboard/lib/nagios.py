from collections import defaultdict
from datetime import datetime
import re


class NagiosServiceGroup(object):
    def __init__(self):
        self.services = {}

    def append(self, s):
        self.services[s.description] = s

    def __getitem__(self, key):
        return self.services.get(key)

    def __len__(self):
        return len(self.services)

    def __iter__(self):
        return (s for s in self.services.values())


class NagiosService(object):

    STATES = {'0': 'OK', '1': 'WARNING', '2': 'CRITICAL'}

    def __init__(self, data):
        self._data = data
        self.host = data['host_name']
        self.description = data['service_description']
        self.status = data.get('plugin_output', '')

    @property
    def state(self):
        return self.STATES.get(self._data['current_state'], 'UNKNOWN')

    @property
    def label_class(self):
        label_map = {'OK': 'label-success',
                     'WARNING': 'label-warning',
                     'CRITICAL': 'label-important',
                     'UNKNOWN': 'label-info'}
        return label_map.get(self.state, 'label')


class NagiosStatus(object):

    RE_BLOCKSTART = re.compile('(\w+)\s*{')
    RE_BLOCKEND = re.compile('^\s*}\s*$')
    RE_DEF = re.compile('(\S+)\s*=(.+)$')

    def __init__(self, f):
        self.f = f
        self.hosts = defaultdict(list)
        self.services = defaultdict(NagiosServiceGroup)
        self.updated = None
        try:
            self._parse_blocks()
        except StopIteration:
            pass

    def _parse_blocks(self):
        while True:
            l = self.f.next()
            m = self.RE_BLOCKSTART.search(l)
            if m:
                defs = self._parse_defs()
                if m.group(1) == 'servicestatus':
                    self.services[defs['host_name']].append(NagiosService(defs))
                elif m.group(1) == 'hoststatus':
                    self.hosts[defs['host_name']].append(defs)
                elif m.group(1) == 'info':
                    self.updated = datetime.fromtimestamp(
                                                    float(defs.get('created')))

    def _parse_defs(self):
        defs = {}
        while True:
            l = self.f.next()
            m = self.RE_BLOCKEND.search(l)
            if m:
                return defs

            m = self.RE_DEF.search(l)
            if m:
                defs[m.group(1)] = m.group(2)
