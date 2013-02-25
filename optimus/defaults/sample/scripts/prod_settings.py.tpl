# -*- coding: utf-8 -*-
"""
Production settings file for project '$PROJECT_NAME'
"""
from ${PROJECT_NAME}.settings import *

DEBUG = False

# Directory where all stuff will be builded
PUBLISH_DIR = os.path.join(PROJECT_DIR, '_build/prod')
# Path where will be moved all the static files, usually this is a directory in 
# the ``PUBLISH_DIR``
STATIC_DIR = os.path.join(PROJECT_DIR, PUBLISH_DIR, 'static')
