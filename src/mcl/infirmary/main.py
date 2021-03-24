# encoding: utf-8

'''
🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular
and Cellular Characterization of Screen-Detected Lesions.

Main entrypoint.
'''

from . import VERSION
from .interfaces import IDirectory
from .resources import Root
from .utils import AppStats, Directory, Database
from pyramid.events import NewRequest
from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from zope.component import getGlobalSiteManager, provideUtility, getUtility
import logging, os, argparse, sys

_logger     = logging.getLogger(__name__)
_ldapServer = 'ldaps://edrn-ds.jpl.nasa.gov'
_dbURI      = 'postgresql://mcl:mcl@localhost/clinical_data'
_origins    = [
    'https://labcas-dev.jpl.nasa.gov/',
    'https://mcl-labcas.jpl.nasa.gov/',
    'https://mcl-new.jpl.nasa.gov/',
    'https://mcl.jpl.nasa.gov',
    'https://mcl.nci.nih.gov',
]


def _checkCredentials(username, password, request):
    '''See if the given ``username`` and ``password`` check out. The ``request`` is ignored.'''
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

    # Basics
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument('-p', '--port', default=8080, type=int, help='Listen port (%(default)d)')

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


def cors_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)


def main():
    '''Start the infirmary server'''
    args = _parseArgs()
    logging.basicConfig(level=args.loglevel)
    _logger.info('🏥 Infirmary version %s', VERSION)
    config = Configurator(registry=getGlobalSiteManager(), root_factory=Root)
    config.setup_registry()
    config.set_authentication_policy(BasicAuthAuthenticationPolicy(_checkCredentials))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_route('home', '/')
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
    config.add_subscriber(cors_callback, NewRequest)
    config.scan()
    provideUtility(AppStats(sys.argv[0]))
    provideUtility(Directory(args.ldap_server))
    provideUtility(Database(args.database))
    app = config.make_wsgi_app()
    _logger.debug('🏃‍♀️ Starting server on port %d', args.port)
    server = make_server('0.0.0.0', args.port, app)
    server.serve_forever()


if __name__ == '__main__':
    main()
