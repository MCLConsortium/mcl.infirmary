# encoding: utf-8

'''
🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular
and Cellular Characterization of Screen-Detected Lesions.

Main entrypoint.
'''

from .resources import Root
from .utils import AppStats, Directory, Database
from .interfaces import IDirectory
from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from zope.component import getGlobalSiteManager, provideUtility, getUtility
import logging, os, argparse, sys

_logger = logging.getLogger(__name__)

_ldapServer = 'ldaps://edrn-ds.jpl.nasa.gov'
_dbURI = 'postgresql://mcl:mcl@localhost/clinical_data'


def _checkCredentials(username, password, request):
    directory = getUtility(IDirectory)
    if directory.authenticate(username, password):
        return []  # This empty list indicates the user is logged in
    else:
        return None


def _parseArgs():
    '''Parse the command line arguments and return a namespace'''
    parser = argparse.ArgumentParser(
        description='🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions',
    )

    # Handle logging
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-d', '--debug', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO,
        help='🔊 Log debugging messages; handy for developers'
    )
    group.add_argument(
        '-q', '--quiet', action='store_const', dest='loglevel', const=logging.WARNING,
        help="🤫 Don't log info messages; just warnings and critical notes"
    )

    # LDAP arguments. Note that to be truly flexible we should allow for user filter template,
    # search scope, time limits, and other stuff but this is just for the Consortium for
    # Molecular and Cellular Characterization of Screen-Detected Lesions.
    parser.add_argument(
        '-H', '--ldap-server', default=os.environ.get('LDAP_SERVER', _ldapServer),
        help='🖥 LDAP server URI (%(default)s)'
    )

    parser.add_argument(
        '-w', '--database', default=os.environ.get('DATABASE', _dbURI),
        help='📀 Database server URI (%(default)s)'
    )

    return parser.parse_args()


def main():
    args = _parseArgs()
    logging.basicConfig(level=args.loglevel)
    config = Configurator(registry=getGlobalSiteManager(), root_factory=Root)
    config.setup_registry()
    config.set_authentication_policy(BasicAuthAuthenticationPolicy(_checkCredentials))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_route('ping', '/ping')
    config.add_route('hello', '/hello/{name}', factory=Root)
    config.add_route('clinicalCores', '/clinicalCores', factory=Root)
    config.add_route('clinicalCore', '/clinicalCores/{participant_ID}', factory=Root)
    config.add_route('organs', '/organs', factory=Root)
    config.add_route('organ', '/organs/{identifier}', factory=Root)
    config.add_route('specimens', '/specimens', factory=Root)
    config.add_route('specimen', '/specimens/{specimen_ID}', factory=Root)
    config.add_route('genomics', '/genomics', factory=Root)
    config.add_route('genomic', '/genomics/{specimen_ID}', factory=Root)
    config.add_route('images', '/images', factory=Root)
    config.add_route('image', '/images/{identifier}', factory=Root)
    config.scan()
    appStats = AppStats(sys.argv[0])
    provideUtility(appStats)
    directory = Directory(args.ldap_server)
    provideUtility(directory)
    database = Database(args.database)
    provideUtility(database)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    _logger.debug('🏃‍♀️ Starting server')
    server.serve_forever()


if __name__ == '__main__':
    main()
