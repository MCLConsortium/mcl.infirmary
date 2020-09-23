# encoding: utf-8

'''
🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular
and Cellular Characterization of Screen-Detected Lesions.

Views.
'''


from . import VERSION
from mcl.sickbay import VERSION as SICKBAY_VERSION
from .interfaces import IAppStats, IDatabase
from mcl.sickbay.model import ClinicalCore, Organ, Biospecimen, Genomics, Imaging
from mcl.sickbay.json import ClinicalCoreEncoder, ORGAN_ENCODERS, BiospecimenEncoder, GENOMICS_ENCODERS, ImagingEncoder
from pyramid.httpexceptions import HTTPUnauthorized, HTTPForbidden, HTTPNotFound
from pyramid.security import forget
from pyramid.view import forbidden_view_config
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound
from zope.component import getUtility


class PingView(object):
    '''This view tests the health of the server and returns some basic information like
    uptime, component version information, etc.
    '''
    def __init__(self, request):
        self.request = request

    @view_config(route_name='ping', renderer='json')
    def __call__(self):
        '''Return a JSON dict with the uptime, program invocation name, version, and the
        version of the ``mcl.sickbay`` component being used.
        '''
        stats = getUtility(IAppStats)
        return {
            'uptime': stats.getUptime(),
            'program': stats.getProgramName(),
            'version': VERSION,
            'sickbay': SICKBAY_VERSION,
        }


class ProtectedGreetingView(object):
    '''Used primarily for testing authenticated requests but without impacting any database.
    This endpoint just returns a simple JSON payload but requires the `view` permission.
    '''
    def __init__(self, request):
        self.request = request

    @view_config(route_name='hello', renderer='json', permission='view')
    def __call__(self):
        '''👋'''
        return {'greeting': '🌊 do the wave, %(name)s' % self.request.matchdict}


class HTTPBasicChallengeView(object):
    '''This view presents a basic authentication challenge to requests that need it'''
    def __init__(self, request):
        self.request = request

    @forbidden_view_config()
    def __call__(self):
        if self.request.authenticated_userid is None:
            response = HTTPUnauthorized()
            response.headers.update(forget(self.request))
        else:
            response = HTTPForbidden()
        return response


class _DatabaseView(object):
    '''This is an abstract view that not just tucks away the HTTP request but also
    starts a session with the database. Subclass views can then take advantage of the
    session that's ready and raring to go.
    '''
    def __init__(self, request):
        self.request, self.session = request, getUtility(IDatabase).createSession()


class ClinicalCoresView(_DatabaseView):
    '''API endpoints for clinical cores'''

    @view_config(route_name='clinicalCores', renderer='json', permission='view')
    def all(self):
        '''Return a JSON sequence of *all* the clinical cores and all their associated data'''
        e = ClinicalCoreEncoder()
        return [e.default(i) for i in self.session.query(ClinicalCore)]

    @view_config(route_name='clinicalCore', renderer='json', permission='view')
    def one(self):
        '''Return a JSON dict of a single, identified clinical core'''
        try:
            i = self.request.matchdict['participant_ID']
            cc = self.session.query(ClinicalCore).filter(ClinicalCore.participant_ID == i).one()
            return ClinicalCoreEncoder().default(cc)
        except NoResultFound:
            raise HTTPNotFound()


class OrgansView(_DatabaseView):
    '''API endpoints for organs'''

    @view_config(route_name='organs', renderer='json', permission='view')
    def all(self):
        '''Return a JSON sequence of every organ in the system'''
        return [ORGAN_ENCODERS[i.__class__]().default(i) for i in self.session.query(Organ)]

    @view_config(route_name='organ', renderer='json', permission='view')
    def one(self):
        '''Return a JSON dict of the single, identified organ'''
        try:
            i = int(self.request.matchdict['identifier'])
            organ = self.session.query(Organ).filter(Organ.identifier == i).one()
            return ORGAN_ENCODERS[organ.__class__]().default(organ)
        except NoResultFound:
            raise HTTPNotFound()


class SpecimensView(_DatabaseView):
    '''API endpoints for specimens'''

    @view_config(route_name='specimens', renderer='json', permission='view')
    def all(self):
        '''Return a JSON sequence of every biospecimen in the database'''
        e = BiospecimenEncoder()
        return [e.default(i) for i in self.session.query(Biospecimen)]

    @view_config(route_name='specimen', renderer='json', permission='view')
    def one(self):
        '''Return a JSON dict of the single, identified biospecimen'''
        try:
            i = self.request.matchdict['specimen_ID']
            specimen = self.session.query(Biospecimen).filter(Biospecimen.specimen_ID == i).one()
            return BiospecimenEncoder().default(specimen)
        except NoResultFound:
            raise HTTPNotFound()


class GenomicsView(_DatabaseView):
    '''API endpoints for genomics'''

    @view_config(route_name='genomics', renderer='json', permission='view')
    def all(self):
        '''Return a JSON sequence of every genomic bit of data in the system'''
        return [GENOMICS_ENCODERS[i.__class__]().default(i) for i in self.session.query(Genomics)]

    @view_config(route_name='genomic', renderer='json', permission='view')
    def one(self):
        '''Return a JSON dict of the single identified genomics item in the database'''
        try:
            i = self.request.matchdict['specimen_ID']
            genomic = self.session.query(Genomics).filter(Genomics.specimen_ID == i).one()
            return GENOMICS_ENCODERS[genomic.__class__]().default(genomic)
        except NoResultFound:
            raise HTTPNotFound()


class ImagesView(_DatabaseView):
    '''API endpoints for imaging'''

    @view_config(route_name='images', renderer='json', permission='view')
    def all(self):
        '''Return a JSON sequence of every bit of imaging info in the database'''
        e = ImagingEncoder()
        return [e.default(i) for i in self.session.query(Imaging)]

    @view_config(route_name='image', renderer='json', permission='view')
    def one(self):
        '''Return a JSON dict of the single, identified bit of imaging info'''
        try:
            i = int(self.request.matchdict['identifier'])
            image = self.session.query(Imaging).filter(Imaging.identifier == i).one()
            return ImagingEncoder().default(image)
        except NoResultFound:
            raise HTTPNotFound()
