from flask import Flask
from flaskext.cache import Cache

from .settings_local import LocalSettings


app = Flask(__name__)
app.config.from_object(LocalSettings)

if app.config.get('SENTRY_DSN'):
    from raven.contrib.flask import Sentry
    sentry = Sentry(app)

cache = Cache(app)

from . import views
