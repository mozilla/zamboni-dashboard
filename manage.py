from tempfile import NamedTemporaryFile
import os
import time

from flaskext.script import Manager
import requests

from zamboni_dashboard import app
from zamboni_dashboard.data.pingdom import pingdom

import gc

manager = Manager(app)


@manager.command
def fetch_nagios_state():
    while True:

        try:
            r = requests.get(app.config['NAGIOS_STATUS_URL'], timeout=10)
        except requests.exceptions.ConnectionError, e:
            print "Error:", e
            time.sleep(30)
            continue
        except requests.exceptions.Timeout, e:
            print "Timeout:", e
            time.sleep(30)
            continue

        if r.status_code == 200:
            f = NamedTemporaryFile(delete=False)
            f.write(r.content)
            r = None
            f.close()
            os.rename(f.name, app.config['NAGIOS_STATUS_FILE'])

        gc.collect()
        time.sleep(15)


@manager.command
def precache_pingdom():
    pingdom.checks(with_summary=True, refresh=True)

if __name__ == "__main__":
    manager.run()
