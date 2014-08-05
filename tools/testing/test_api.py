#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools.test.APIExerciser import APIExerciser
from nose.tools import nottest


class TestApi:

    def __init__(self):
        self.api = APIExerciser(None, True, "TestUser", "pwhere")

    def test_login(self):
        assert self.api.api.login("crapp", "wrong pw") is False

    #takes really long, only test when needed
    @nottest
    def test_random(self):
        for _ in xrange(0, 100):
            self.api.testAPI()
