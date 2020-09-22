# encoding: utf-8

'''
🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular
and Cellular Characterization of Screen-Detected Lesions.

This is the ``infirmary`` module, or the primary container module of the
entire ``mcl.infirmary`` package.
'''

import pkg_resources


def _read_version():
    '''In Python 3.8, we should use ``importlib.metadata`` instead. But until then,
    we keep version information in a separate ``VERSION.txt`` file. Note that this file
    cannot contain any extra comments and we assume it's text witn bytes encoded in
    utf-8.
    '''
    return pkg_resources.resource_string(__name__, 'VERSION.txt').decode('utf-8').strip()


__version__ = VERSION = _read_version()


__all__ = (
    __version__,
    VERSION,
)
