import datetime
import logging
import os
import re
import sys

import urllib
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class XnatSession():
    def __init__(self, **kwargs):
        try:
            self.starttime = None
            self.httpsess = None
            self.lastrenew = None
            self.logger = None
            self.logfile = None

            # Set up logging
            self.setup_logger()

            # Pull u/p from env if not set in args
            if kwargs['username'] is None or kwargs['password'] is None:
                (self.username, self.password) = os.environ['XNATCREDS'].split(':', 2)
            else:
                self.username = kwargs['username']
                self.password = kwargs['password']

            self.host = kwargs['host']
            self.timeout = 120
            self.sessiontimeout = datetime.timedelta(minutes=15)

        except KeyError as e:
            logging.error('Unable to initialize XnatSession, missing argument: %s' % str(e))
            exit(1)

    def renew_httpsession(self):
        # Set up request session and get cookie
        if self.lastrenew is None or ((self.lastrenew + self.sessiontimeout) < datetime.datetime.now()):
            self.logger.debug('[SESSION] Renewing XNAT session as %s from %s' % (self.username, self.host))
            # Delete old session if exists
            try:
                self.close_httpsession()
            except:
                # Do nothing
                pass

            # Renew expired session, or set up new session
            self.httpsess = requests.Session()
    
            # Retry logic
            retry = Retry(connect=5, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            self.httpsess.mount('http://', adapter)
            self.httpsess.mount('https://', adapter)
    
            # Log in and generate xnat session
            response = self.httpsess.post(self.host + '/data/JSESSION', auth=(self.username, self.password),
                                          timeout=(30, self.timeout))
            if response.status_code != 200:
                self.logger.error("[SESSION] Renewal failed, no session acquired: %d %s" % (response.status_code,
                                                                                            response.reason))
                exit(1)
    
            self.lastrenew = datetime.datetime.now()
        else:
            # self.logger.debug('[SESSION] Reusing existing https session until %s' % (self.lastrenew +
            #                                                                         self.sessiontimeout))
            return True
    
        return True
    
    def close_httpsession(self):
        # Logs out of session for cleanup
        self.httpsess.delete(self.host + '/data/JSESSION', timeout=(30, self.timeout))
        self.logger.debug('[SESSION] Deleting XNAT session')
        self.httpsess.close()
        return True

    def setup_logger(self):
        # Set up logging
        hdlr = None
        if self.logfile is not None:
            if os.path.exists(os.path.dirname(os.path.realpath(self.logfile))):
                hdlr = logging.FileHandler(self.logfile)
            else:
                logging.error('Log path %s does not exists' % str(self.logfile))
                exit(1)
        else:
            hdlr = logging.StreamHandler(sys.stdout)

        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)
        return True
