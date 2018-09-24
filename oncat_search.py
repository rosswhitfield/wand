#!/usr/bin/env python2
import os
import sys
import pyoncat
import getpass
import numpy as np

CLIENT_ID = '9e736eae-f90c-4513-89cf-53607eee5165'
CLIENT_SECRET = None


class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None
    def set_token(self, token):
        self._token = token
    def get_token(self):
        return self._token


token_store = InMemoryTokenStore()

oncat = pyoncat.ONCat(
    'https://oncat.ornl.gov',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    token_getter=token_store.get_token,
    token_setter=token_store.set_token,
    flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW
)

if token_store.get_token() is None:
    username = getpass.getuser()
    password = getpass.getpass()
    oncat.login(username, password)

datafile = oncat.Datafile.retrieve(
    '/HFIR/HB2C/IPTS-20492/nexus/HB2C_139418.nxs.h5',
    facility="HFIR",
    instrument="HB2C",
    experiment="IPTS-20492",
    projection=['metadata.entry.title']
)

print(datafile)

datafiles = oncat.Datafile.list(
    facility="HFIR",
    instrument="HB2C",
    experiment="IPTS-20492",
    projection=['indexed.run_number', 'metadata.entry.title']
)

for datafile in datafiles:
    print('{} - {}'.format(datafile.indexed['run_number'],
                           datafile.metadata['entry']['title']))

titles = set(datafile.metadata['entry']['title'] for datafile in datafiles)
