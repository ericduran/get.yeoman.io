#!/usr/bin/env python

"""This module the bootstrap App Engine app for the curl install script."""

__author__ = 'ebidel@gmail.com (Eric Bidelman)'

import logging
import os
import time
import urllib
import urllib2
import webapp2

# TODO: This app.yaml version should probably be changed when the yeoman
# package.json revs, unless we want to keep the install.sh version separate from
# the CLI version.
APP_VERSION = os.environ['CURRENT_VERSION_ID'].split('.')[0]
APP_NAME = 'Yeoman Insight'

# This is a stripped down version of github.com/yeoman/bin/yeomaninsight.py.
# Changes there should most likely be reflected here as well.
class Analytics(object):

  TRACKING_CODE = 'UA-31537568-1'
  BASE_URL = 'http://www.google-analytics.com/collect/__utm.gif'

  def __init__(self, tracking_code):
    self.tracking_code = tracking_code
    self.client_id = APP_VERSION

  def send(self, path='/', recorded_at=None):
    """Sends one pageview entry to Google Analytics.

    This method constructs the appropriate URL and makes a GET request to the
    tracking API.

    Args:
      path: A string representing the url path of the pageview to record.
          URL query parameters may be included. The format should map to the
          the command that was issued:
            yeoman init -> /init
            yeoman add model -> /add/model
      recorded_at: When the hit was recorded in seconds since the epoch.
          If absent, now is used.
    Returns:
      True if message was sent, otherwise false.
    """
    recorded_at = recorded_at or time.time()

    params = {
      'v': '1', # GA API tracking version.
      'tid': self.tracking_code, # Tracking code ID.
      't': 'pageview', # Event type
      'cid': self.client_id, # Client ID
      'aip': '1', # Anonymize IP
      'qt': int((time.time() - recorded_at) * 1e3), # Queue Time. Delta (milliseconds) between now and when hit was recorded.
      'dp': path,
      'an': APP_NAME, # Application Name.
      'av': APP_VERSION.replace('-', '.'), # App Version. 0-0-1 -> 0.0.1
      'z': time.time() # Cache bust. Probably don't need, but be safe. Should be last param.
    }

    encoded_params = urllib.urlencode(params)
    url = '%s?%s' % (self.BASE_URL, encoded_params)

    try:
      response = urllib2.urlopen(url)
      #if response.code == 200:
      #  return True
      return True
    except urllib2.URLError:
      logging.error('Could not make request ' + url)


class MainHandler(webapp2.RequestHandler):

  # TODO: remove LOGIN and TOKEN when repos are public.
  LOGIN = 'paulirish'
  TOKEN = '6d70f2a657b7738d157779c11127528d'
  INSTALL_URL = ('https://raw.github.com/yeoman/yeoman/master/setup/install.sh'
                 '?login=%s&token=%s' % (LOGIN, TOKEN))

  def get(self, path):
    # Record this hit in Insight.
    ga = Analytics(Analytics.TRACKING_CODE)

    # Record pageview and include version number. Example: /curl/0.0.1
    ga.send(path='/curl/' + APP_VERSION.replace('-', '.'))

    # Redirect to install script.
    self.redirect(self.INSTALL_URL, permanent=True)


def handle_404(request, response, exception):
  response.write('Oops! Not Found.')
  response.set_status(404)

def handle_500(request, response, exception):
  response.write('Oops! Internal Server Error.')
  response.set_status(500)


# App URL routes.
routes = [
  (r'/(.*)', MainHandler)
]

app = webapp2.WSGIApplication(routes, debug=False)
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
