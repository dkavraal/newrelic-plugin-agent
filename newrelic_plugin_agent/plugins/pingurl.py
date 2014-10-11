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
    TIMEOUT      = 10
    GUID = 'com.dincerkavraal.PingURL'

    def add_datapoints(self, stats):
        try:
            timeout = self.config.get('timeout', self.TIMEOUT)
            url = 'http://%s:%s%s' % (self.config.get('host', self.DEFAULT_HOST), self.config.get('port', self.DEFAULT_PORT), self.config.get('path', self.DEFAULT_PATH))
            r = requests.request('HEAD', url, timeout=timeout)
            if r.status_code == 200:
                self.add_gauge_value('ReachTime', 'miliseconds', r.elapsed.microseconds/1000)
                LOGGER.info('URL Ping reached target at %f secs.', r.elapsed.total_seconds())
            else:
                self.add_gauge_value('ReachTime', 'miliseconds', timeout)
                LOGGER.info('Couldnot reach URL %s' % url)
        except:
            LOGGER.error('PingURL failed.', exc_info=True)
