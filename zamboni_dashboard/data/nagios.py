from .. import app
from ..lib.nagios import NagiosStatus


def get_nagios_status():
    with open(app.config['NAGIOS_STATUS_FILE']) as f:
        return NagiosStatus(f)


def get_nagios_service_status():
    nstatus = get_nagios_status()
    status = []
    for group, hosts, services in app.config['NAGIOS_SERVICE_GROUPS']:
        group_status = {}
        for s in services:
            group_status[s] = {'all': [], 'OK': [],
                                'WARNING': [], 'CRITICAL': [], 'UNKNOWN': []}
            for h in hosts:
                tmp = nstatus.services[h][s]
                if tmp:
                    group_status[s][tmp.state].append(tmp)
                    group_status[s]['all'].append(tmp)
                else:
                    app.logger.warning('Service %s:%s defined, but does not exist.' % (h, s))

        status.append((group, group_status))

    return status, nstatus.updated
