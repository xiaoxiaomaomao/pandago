#!/usr/bin/python
import unittest
import test_SessionGroup

def suite():
    sessionSuite = unittest.makeSuite(test_SessionGroup.test_SessionGroup,"test")
    return unittest.TestSuite((sessionSuite))


