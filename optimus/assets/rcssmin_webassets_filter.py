from __future__ import absolute_import
from webassets.filter import Filter


__all__ = ('RCSSMin',)


class RCSSMin(Filter):
    """Minifies CSS.

    Requires the ``rcssmin`` package (https://github.com/ndparker/rcssmin).
    Alike 'cssmin' it is a port of the YUI CSS compression algorithm but aiming
    for speed instead of maximum compression.
    """

    name = 'rcssmin'

    def output(self, _in, out, **kw):
        import rcssmin
        out.write(rcssmin.cssmin(_in.read()))
