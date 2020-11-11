# encoding: utf-8

'''
🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular
and Cellular Characterization of Screen-Detected Lesions.

Utilities.
'''


from .interfaces import IAppStats, IDirectory, IDatabase
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zope.interface import implementer
import ldap


@implementer(IAppStats)
class AppStats(object):
    '''App-wide statistics'''
    def __init__(self, programName):
        '''Initialize the stats with the given ``programName`` and record a starting timestamp'''
        # Get the current UTC time and drop timezone info
        ts = datetime.utcnow()
        self.start       = datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second, microsecond=0, tzinfo=None)
        self.programName = programName

    def getUptime(self):
        '''See interface docs'''
        # Get the current UTC time and drop timezone info, then return the delta from the start time
        ts = datetime.utcnow()
        ts = datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second, microsecond=0, tzinfo=None)
        return (ts - self.start).total_seconds()

    def getProgramName(self):
        '''See interface docs'''
        return self.programName

    def getOrigins(self):
        '''See interface docs'''
        return self.origins


@implementer(IDirectory)
class Directory(object):
    '''App-wide directory (LDAP) interface'''
    def __init__(self, uri):
        self.uri = uri

    def authenticate(self, username, password):
        '''See interface docs'''
        try:
            c = ldap.initialize(self.uri)
            c.bind_s(f'uid={username},ou=users,o=MCL', password)
            return True
        except ldap.INVALID_CREDENTIALS:
            return False


@implementer(IDatabase)
class Database(object):
    '''App-wide directory interface'''
    def __init__(self, uri):
        self.uri = uri

    def createSession(self):
        '''See interface docs'''
        engine = create_engine(self.uri)
        Session = sessionmaker()
        Session.configure(bind=engine)
        return Session()
