# -*- coding: utf-8 -*-
from optimus.exceptions import InvalidHostname


def get_host_parts(hostname, default_name='127.0.0.1', default_port=80):
    """
    Parse given hostname

    Arguments:
        hostname (str): A valid hostname containing a valid host name with
            optional port separated with a ``:``.

    Keyword Arguments:
        default_name (str): Default hostname when none is given. Default value
            is ``127.0.0.1``.
        default_port (int): Default port when none is given. Default value is
            ``80``.

    Returns:
        tuple: Host name (string) and port (integer).
    """
    name = None
    port = None
    hostparts = hostname.split(':')

    if len(hostparts) > 2:
        raise InvalidHostname("Invalid hostname format, too many ':'")
    elif len(hostparts) == 2:
        name, port = hostparts
        if not port or not name:
            raise InvalidHostname(("Invalid hostname format, address or port "
                                   "is empty"))

        try:
            port = int(port)
        except ValueError:
            raise InvalidHostname("Invalid port given: {0}".format(port))
    else:
        name = hostparts[0]

    return (name or default_name, port or default_port)
