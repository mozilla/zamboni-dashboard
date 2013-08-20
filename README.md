zamboni-dashboard
=================

Dashboard for zamboni operations.

Developers
==========

Get the source

    git clone git@github.com:mozilla/zamboni-dashboard.git
    cd zamboni-dashboard

Using [pip](http://www.pip-installer.org/)
and a [virtualenv](https://pypi.python.org/pypi/virtualenv) (optional),
install deps, initialize settings, and start a dev server.

    pip install -r requirements.txt
    cp zamboni_dashboard/settings_local.py.dist zamboni_dashboard/settings_local.py
    python runserver.py
