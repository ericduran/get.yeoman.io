#!/usr/bin/env python

"""This module the bootstrap App Engine app for the curl install script."""

__author__ = 'ebidel@gmail.com (Eric Bidelman)'

import webapp2
import logging


class MainHandler(webapp2.RequestHandler):

  LOGIN = 'paulirish'
  TOKEN = '6d70f2a657b7738d157779c11127528d'
  INSTALL_URL = ('https://raw.github.com/yeoman/yeoman/master/setup/install.sh'
                 '?login=%s&token=%s' % (LOGIN, TOKEN))

  def get(self, path):
    # Redirect everything to install URL.
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
