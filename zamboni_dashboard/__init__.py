from flask import Flask

from .settings_local import LocalSettings


app = Flask(__name__)
app.config.from_object(LocalSettings)

from . import views
