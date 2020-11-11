# encoding: utf-8

'''
🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular
and Cellular Characterization of Screen-Detected Lesions.

Interface definitions.
'''

from zope.interface import Interface


class IAppStats(Interface):
    '''Application statistics'''

    def getUptime():
        '''Tell how many seconds we've been running'''

    def getProgramName():
        '''Get my invocation program name, typically argv[0]'''

    def getAllowedOrigins():
        '''Return a sequence of allowed origin URLs for CORS'''


class IDirectory(Interface):
    '''Directory interface'''

    def authenticate(username, password):
        '''Return true if ``username`` is validated by ``password`` in the directory'''


class IDatabase(Interface):
    '''Database interface'''

    def createSession():
        '''Return a SQL session to the database'''
