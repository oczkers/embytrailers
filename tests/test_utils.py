#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for embytrailers.utils"""

import unittest
# import responses

from embytrailers import utils
# from embytrailers.exceptions import EmbytrailersError


# if version_info[0] == 2:  # utf8 for python2
#     from codecs import open


class EmbytrailersUtilsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        utils.download

    # TODO: responses
