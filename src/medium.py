#!/usr/bin/python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-12-29
#

"""medium.py [options] <query>

Browse and search medium users, posts.

Usage:
    medium.py <query>
    medium.py [-p]
    medium.py (-h | --help)
    medium.py --version

Options:
    -p, --post            Open post
    -h, --help            Show this help text
    -version              Show version.

"""

import json
import os
import requests
import subprocess
import sys

from workflow import Workflow3

############### CONSTANTS ###############

HELP_URL = 'https://github.com/joshuajharris/alfred-medium-workflow'
VERSION = '0.1.0'
UPDATE_SETTINGS = {
    'github_slug': 'joshuajharris/alfred-medium-workflow',
    'version': VERSION
}

URL = 'https://medium.com'
SEARCH_URL = URL + '/search'
POST_URL = URL + '/post'

ICON_UPDATE = os.path.join(os.path.dirname(__file__), 'update-available.png')

USER_AGENT = 'Alfred-Medium-Workflow/{version} ({url})'

############### HELPERS ###############

def open_url(url):
    """Open URL in default browser."""
    log.debug('Opening : %s', url)
    subprocess.call(['open', url])

def sanitize_json(raw):
    """Sanitizes json, removes bs ])}while(1);</x>"""
    j = json.loads(raw[raw.index('{'):])
    return j

def get_posts_from_payload(j):
    return j['payload']['value']['posts']

############### MEDIUM API ###############

def search_posts(q):
    """gonna search posts here"""
    payload = {'q': q, 'format': 'json'}
    r = requests.get(SEARCH_URL, params=payload)
    log.debug(r.url)
    log.debug(r.status_code)
    if r.status_code == 200:
        j = sanitize_json(r.text)
        posts = get_posts_from_payload(j) 
        log.debug("Number of results: %d", len(posts))
    return posts;

############### WORKFLOW ###############

def add_posts(posts):
    for post in posts:
        url = '{}/{}'.format(POST_URL, post['id'])
        it = wf.add_item(
            post['title'],
            "{} words".format(post['virtuals']['wordCount']),
            autocomplete= u'{}/'.format(post['title']),
            arg=url,
            uid=post['id'],
            quicklookurl=url,
            valid=True)
        
        it.setvar('post_url', url)
        it.setvar('argv', '-p')
    
    wf.send_feedback()
    return 0


def main(wf):
    """RUN WORKFLOW"""
    from docopt import docopt
    args = docopt(__doc__, argv=wf.args, version=VERSION)

    log.debug('args : %r', args)

    # Run Script actions
    # ------------------------------------------------------------------

    done = False
    if args.get('--post'):
        open_url(os.getenv('post_url'))
        done = True

    if done:
        return

    ####################################################################
    # Script Filter
    ####################################################################

    # Updates
    # ------------------------------------------------------------------
    if wf.update_available:
        wf.add_item('A newer version is available',
                    '↩ to install update',
                    autocomplete='workflow:update',
                    icon=ICON_UPDATE)

    query = args.get('<query>')
    log.debug('query : %r', query)


    # Show popular subreddits
    # ------------------------------------------------------------------
    if query == '':
        log.debug("blah")
    else:
        posts = search_posts(query)
        add_posts(posts)


    # Parse query
    # ------------------------------------------------------------------

if __name__ == '__main__':
    wf = Workflow3(help_url=HELP_URL,
        update_settings=UPDATE_SETTINGS)
    log = wf.logger
    sys.exit(wf.run(main))
