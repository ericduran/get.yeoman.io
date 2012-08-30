#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging


installurl = 'https://raw.github.com/yeoman/yeoman/master/setup/install.sh?login=paulirish&token=6d70f2a657b7738d157779c11127528d'

class MainHandler(webapp2.RequestHandler):

    def get(self, path):

        # Perform redirect
        if self.request.path == '/install':
            logging.info('Successfully redirecting ' + self.request.url + ' to ' + installurl);
            self.redirect(installurl, permanent=False)

        else:
            self.response.out.write('Yo man!')
            # Log that we didn't know what this was, and redirect to a good default
            logging.error('Unable to redirect this url: ' + self.request.url);

            # Don't do permanent (301), since we don't know what this is.
            # Move it into the dictionary above if needed
            # self.redirect('http://yeoman.io/', permanent=False)


app = webapp2.WSGIApplication([(r'/(.*)', MainHandler)],
                              debug=True)
