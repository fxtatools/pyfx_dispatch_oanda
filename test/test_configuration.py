"""Unit tests for pyfx.dispatch.oanda.configuration"""

from assertpy import assert_that  # type: ignore[import-untyped]
import random
from pydantic import ValidationError
import string
import dateutil.tz
from datetime import tzinfo
from pytest import mark

from pyfx.dispatch.oanda.test import ComponentTest, run_tests

import pyfx.dispatch.oanda.configuration as config
import pyfx.dispatch.oanda.hosts as hosts

TOKEN_INPUT: str = "".join(frozenset(string.ascii_letters + string.digits + string.punctuation + " "))


class TestConfiguration(ComponentTest):
    """Unit tests for the Configuration model"""

    def gen_random_str(self, l: int = 12):
        return "".join(random.choices(TOKEN_INPUT, k = l))

    def test_config_model(self):
        fields = config.Configuration.model_fields
        tz_field = fields['timezone']
        assert_that(isinstance(tz_field, config.ConfigFieldInfo)).is_true()

    @mark.dependency()
    def test_demo_profile(self):
        ## test initilization for a default (fxpractice) account configuration
        token = self.gen_random_str()
        demo_inst = config.Configuration(access_token=token)

        assert_that(demo_inst.access_token).is_equal_to(token)
        assert_that(demo_inst.max_connections).is_not_none()
        assert_that(isinstance(demo_inst.debug_header, str)).is_true

        assert_that(demo_inst.fxpractice).is_equal_to(True)
        assert_that(demo_inst.get_host()).is_equal_to(hosts.FxHostInfo.FXPRACTICE.value)

        ## switch to the live profile and test host info
        demo_inst.use_fxlive_profile()
        assert_that(demo_inst.fxpractice).is_equal_to(False)
        assert_that(demo_inst.get_host()).is_equal_to(hosts.FxHostInfo.FXLIVE.value)

        ## switch to original profile and test host info
        demo_inst.use_fxpractice_profile()
        assert_that(demo_inst.fxpractice).is_equal_to(True)
        assert_that(demo_inst.get_host()).is_equal_to(hosts.FxHostInfo.FXPRACTICE.value)

    def test_live_profile(self):
        ## test initialization for an fxLive (fxpractice = False) configuration
        token = self.gen_random_str()
        live_inst = config.Configuration(fxpractice=False, access_token=token)
        assert_that(live_inst.access_token).is_equal_to(token)
        assert_that(live_inst.fxpractice).is_equal_to(False)
        assert_that(live_inst.get_host()).is_equal_to(hosts.FxHostInfo.FXLIVE.value)

        ## switch to fxpractice profile and test host info
        live_inst.use_fxpractice_profile()
        assert_that(live_inst.fxpractice).is_equal_to(True)
        assert_that(live_inst.get_host()).is_equal_to(hosts.FxHostInfo.FXPRACTICE.value)

        ## switch to original profile and test host info
        live_inst.use_fxlive_profile()
        assert_that(live_inst.fxpractice).is_equal_to(False)
        assert_that(live_inst.get_host()).is_equal_to(hosts.FxHostInfo.FXLIVE.value)

    def test_failure_case(self):
        assert_that(config.Configuration).raises(ValidationError).when_called_with()
        assert_that(config.Configuration).raises(ValidationError).when_called_with(access_token=random.randint(512, 1023))

    @mark.dependency(depends_on=['test_demo_profile'])
    def test_tz(self):
        profile_tz_default = config.Configuration(access_token = self.gen_random_str())
        tz = profile_tz_default.timezone
        assert_that(isinstance(tz, tzinfo)).is_true()
        
        profile_tz_none = config.Configuration(access_token = self.gen_random_str(), timezone=None)
        tz = profile_tz_none.timezone
        assert_that(tz).is_equal_to(dateutil.tz.UTC)
        
        profile_tz_1 = config.Configuration(access_token = self.gen_random_str(), timezone="UTC-1")
        tz = profile_tz_1.timezone
        assert_that(tz).is_equal_to(dateutil.tz.gettz("UTC-1"))

        

if __name__ == '__main__':
    run_tests(__file__)
