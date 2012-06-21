from flask import Flask

from .settings_local import LocalSettings


app = Flask(__name__)
app.config.from_object(LocalSettings)

if app.config.get('SENTRY_DSN'):
    from raven.contrib.flask import Sentry
    sentry = Sentry(app)

from . import views
