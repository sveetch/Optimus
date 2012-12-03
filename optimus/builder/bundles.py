# -*- coding: utf-8 -*-
"""
Common bundles to use with webassets
"""
from webassets import Bundle

COMMON_BUNDLES = {
    'css_screen_common': Bundle(
        'css/screen.css',
        filters='yui_css',
        output='css/screen.min.css'
    ),
    'css_ie_common': Bundle(
        'css/ie.css',
        filters='yui_css',
        output='css/ie.min.css'
    ),
    'js_ie_common': Bundle(
        'js/modernizr.custom.js',
        'js/respond.src.js',
        filters='yui_js',
        output='js/ie.min.js'
    ),
    'js_jquery': Bundle(
        'js/jquery/jquery-1.7.1.js',
        filters='yui_js',
        output='js/jquery.min.js'
    ),
}
