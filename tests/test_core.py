#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for embytrailers.core"""

import unittest
# import responses

from embytrailers import core
# from embytrailers.exceptions import EmbytrailersError


# if version_info[0] == 2:  # utf8 for python2
#     from codecs import open


class EmbytrailersTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        core.Core
