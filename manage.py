from tempfile import NamedTemporaryFile
import os
import time

from flaskext.script import Manager
import requests

from zamboni_dashboard import app


manager = Manager(app)


@manager.command
def fetch_nagios_state():
    while True:

        try:
            r = requests.get(app.config['NAGIOS_STATUS_URL'])
        except requests.exceptions.ConnectionError, e:
            print "Error:", e
            time.sleep(30)
            continue

        if r.status_code == 200:
            f = NamedTemporaryFile(delete=False)
            f.write(r.content)
            f.close()
            os.rename(f.name, app.config['NAGIOS_STATUS_FILE'])

        time.sleep(15)


if __name__ == "__main__":
    manager.run()
