#!/usr/bin/python
import unittest
from SessionFactory import *
class test_SessionFactory(unittest.TestCase):

    def test_Session(self):
        factory = SessionFactory()
        sessionImp = factory.createSession("test");
        assert  isinstance(sessionImp,SessionTestImp.SessionTestImp) == 1


