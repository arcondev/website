#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Arcon Corporation'
SITENAME = 'Research@Arcon'
SITEURL = 'https://arconcorporation.github.io'

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Arcon Corporation', 'https://www.arcon.com/'),)

# Social widget
SOCIAL = (('Github', 'https://www.github.com/arconcorporation'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME='bootstrap'
PLUGINS = ['pelican.plugins.render_math']
