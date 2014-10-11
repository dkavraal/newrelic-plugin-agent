"""
Check URL working
"""
import logging, requests

from newrelic_plugin_agent.plugins import base

LOGGER = logging.getLogger(__name__)

class PingURL(base.HTTPStatsPlugin):

    DEFAULT_PATH = 'PingURL'
    GUID = 'com.dincerkavraal.PingURL'

   def add_datapoints(self, stats):
        url = 'http://%s:%s%s' % (self.config.get('host'), self.config.get('port'), self.config.get('path'))
        r = requests.request('HEAD', url, int(timeout=self.config.get('timeout', 10)))
        if r.status_code == 200:
            self.add_derive_value('Requests/Duration', 'seconds', r.elapsed.total_seconds())
        else:
            self.add_derive_value('Requests/Duration', 'seconds', None)
