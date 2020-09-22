# encoding: utf-8

'''
🏥 Infirmary: an API for Clinical Data for the Consortium for Molecular
and Cellular Characterization of Screen-Detected Lesions.

Resources.
'''

from pyramid.security import Allow, Authenticated, Everyone


class Root(object):
    '''Default ACL or "root (top of the tree)" resources is authenticated users only can view'''
    # __acl__ = [(Allow, Authenticated, 'view')]
    def __init__(self, request):
        # principals = frozenset(request.effective_principals)
        # self.__acl__ = [(Allow, principal, 'view') for principal in principals]
        self.__acl__ = [(Allow, Authenticated, 'view')]
