# coding: utf-8

"""Unit tests for pyfx.dispatch.oanda.configuration"""

from assertpy import assert_that
import random
import unittest
from pydantic import ValidationError

import pyfx.dispatch.oanda.configuration as config
import pyfx.dispatch.oanda.hosts as hosts


class TestConfiguration(unittest.TestCase):
    """Unit tests for the Configuration model"""

    @classmethod
    def gen_secret(cls):
        ## generate a random string, such that may not map
        ## to a conventional keyboard
        return random.randbytes(12).decode("iso-8859-1")

    @classmethod
    def test_demo(cls):
        ## test initilization for a default (fxpractice) account configuration
        token = cls.gen_secret()
        demo_inst = config.Configuration(access_token=token)

        assert_that(demo_inst.access_token).is_equal_to(token)
        assert_that(demo_inst.max_connections).is_not_none()
        assert_that(isinstance(demo_inst.debug_header, str)).is_true

        assert_that(demo_inst.fxpractice).is_equal_to(True)
        assert_that(demo_inst.get_host()).is_equal_to(hosts.FxHostInfo.fxPractice.value)

        ## switch to the live profile and test host info
        demo_inst.use_fxlive_profile()
        assert_that(demo_inst.fxpractice).is_equal_to(False)
        assert_that(demo_inst.get_host()).is_equal_to(hosts.FxHostInfo.fxLive.value)

        ## switch to original profile and test host info
        demo_inst.use_fxpractice_profile()
        assert_that(demo_inst.fxpractice).is_equal_to(True)
        assert_that(demo_inst.get_host()).is_equal_to(hosts.FxHostInfo.fxPractice.value)

    @classmethod
    def test_live(cls):
        ## test for initialization with an fxLive (fxpractice = False) configuration
        token = cls.gen_secret()
        live_inst = config.Configuration(fxpractice=False, access_token=token)
        assert_that(live_inst.access_token).is_equal_to(token)
        assert_that(live_inst.fxpractice).is_equal_to(False)
        assert_that(live_inst.get_host()).is_equal_to(hosts.FxHostInfo.fxLive.value)

        ## switch to fxpractice profile and test host info
        live_inst.use_fxpractice_profile()
        assert_that(live_inst.fxpractice).is_equal_to(True)
        assert_that(live_inst.get_host()).is_equal_to(hosts.FxHostInfo.fxPractice.value)

        ## switch to original profile and test host info
        live_inst.use_fxlive_profile()
        assert_that(live_inst.fxpractice).is_equal_to(False)
        assert_that(live_inst.get_host()).is_equal_to(hosts.FxHostInfo.fxLive.value)

    @classmethod
    def test_failure_case(cls):
        assert_that(config.Configuration).raises(ValidationError).when_called_with()
        assert_that(config.Configuration).raises(ValidationError).when_called_with(token=random.randint(0, 10))


if __name__ == '__main__':
    unittest.main()
