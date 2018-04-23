from __future__ import absolute_import
from webassets.filter import Filter


__all__ = ('RCSSMin',)


class RCSSMin(Filter):
    """
    Minifies CSS using 'rcssmin' library.

    Requires the ``rcssmin`` package (https://github.com/ndparker/rcssmin).

    This is a simple webassets filter that has been merged but not
    released yet, so we ship it until new package release since 'cssmin' is
    totally outdated and doesn't work with Python 3.
    """

    name = 'rcssmin'

    def output(self, _in, out, **kw):
        import rcssmin
        out.write(rcssmin.cssmin(_in.read()))
