from .. import app, cache
from ..lib.pingdom import Pingdom


pingdom = Pingdom(app.config['PINGDOM_USER'], app.config['PINGDOM_PASS'],
                  app.config['PINGDOM_KEY'], cache)
