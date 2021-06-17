#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to check if outcomes are the same."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"


import hashlib
from project_paths import DATA_PATH
path = DATA_PATH + "CIC-IDS-2017/BRO/2_Preprocessed/tcp.csv"
code = hashlib.md5(open(path, 'rb').read()).hexdigest()
print(path)
print(code)
