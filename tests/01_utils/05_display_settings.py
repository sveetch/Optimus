from optimus.utils import display_settings


class DummySettings(object):
    """
    Empty settings object
    """
    def __init__(self):
        pass


def test_basic(caplog):
    """
    Basic initialize without ressources to sync
    """
    conf = DummySettings()
    conf.STRING = 'ok'
    conf.INTEGER = 42
    conf.SEQ = [1, 'hello', 42]
    conf.MAP = {'hello': 'world'}
    conf.LOOSE = 'meh'

    display_settings(conf, ['STRING', 'INTEGER', 'SEQ', 'MAP', 'NOPE'])

    # Check base setting directories

    assert caplog.record_tuples == [
        (
            'optimus',
            10,
            " - Settings.STRING = ok"
        ),
        (
            'optimus',
            10,
            " - Settings.INTEGER = 42"
        ),
        (
            'optimus',
            10,
            " - Settings.SEQ = [1, 'hello', 42]"
        ),
        (
            'optimus',
            10,
            " - Settings.MAP = {'hello': 'world'}"
        ),
        (
            'optimus',
            10,
            " - Settings.NOPE = NOT SET"
        ),
    ]
