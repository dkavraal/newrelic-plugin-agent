"""
Check URL working
"""
import logging, requests

from newrelic_plugin_agent.plugins import base

LOGGER = logging.getLogger(__name__)

class PingURL(base.HTTPStatsPlugin):
    DEFAULT_HOST = 'google.com'
    DEFAULT_PORT = '80'
    DEFAULT_PATH = '/'
    GUID = 'com.dincerkavraal.PingURL'

    def add_datapoints(self, stats):
        try:
            url = 'http://%s:%s%s' % (self.config.get('host', self.DEFAULT_HOST), self.config.get('port', self.DEFAULT_PORT), self.config.get('path', self.DEFAULT_PATH))
            r = requests.request('HEAD', url, timeout=int(self.config.get('timeout', 10)))
            if r.status_code == 200:
                self.add_derive_value('Requests/Duration', 'seconds', r.elapsed.total_seconds())
                LOGGER.info('URL Ping reached target at %f secs.', r.elapsed.total_seconds())
            else:
                self.add_derive_value('Requests/Duration', 'seconds', None)
                LOGGER.info('Couldnot reach URL %s' % url)
        except:
            LOGGER.error('PingURL failed.', exc_info=True)
