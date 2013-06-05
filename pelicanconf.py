#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'J. Bradford Dillon'
SITENAME = u'Just call me Brad'
TAGLINE = u'Husband, father, iOS Developer at Double Encore, amateur yo-yoer, occasional game tinkerer, audiobook enthusiast. You can just call me Brad.'
SITEURL = 'http://jbradforddillon.github.io'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Double Encore', 'http://doubleencore.com/'),
          ('Twitter', 'http://twitter.com/jbradforddillon'))

# Social widget
SOCIAL = ()

# Logo
USER_LOGO_URL = 'http://jbradforddillon.com/wp/wp-content/uploads/2012/08/Avatar-300x300.jpeg'

DEFAULT_PAGINATION = False

THEME = 'themes/svbhack'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PINBOARD_TOKEN = "jbradforddillon:BE694F811952E55D4B20"
PINBOARD_URL = "https://pinboard.in/u:jbradforddillon/t:%23/"
PINBOARD_COUNT = 5
PINBOARD_TAG = '#'

PLUGIN_PATH = '../pelican-pinboard'
PLUGINS = ['pelicanboard']