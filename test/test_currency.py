"""Unit test definition for the Currency enum implementation"""

from assertpy import assert_that  # type: ignore[import-untyped]
from pyfx.dispatch.oanda.test import ComponentTest, run_tests
import isocodes

from pyfx.dispatch.oanda.models.currency import Currency


class CurrencyTest(ComponentTest):

    def test_defs(self):
        for data in isocodes.currencies.items:
            alpha = data['alpha_3']
            digits_str = data['numeric']
            assert_that(Currency.get(alpha).digits_str).is_equal_to(digits_str)
            assert_that(alpha in Currency._member_map_).is_true()
            assert_that(Currency._member_map_[alpha]).is_equal_to(Currency.get(alpha))

            digits_int = int(digits_str)
            assert_that(digits_int in Currency._value2member_map_).is_true()
            assert_that(Currency._value2member_map_[digits_int]).is_equal_to(Currency._member_map_[alpha])


if __name__ == '__main__':
    run_tests(__file__)

    ## naive profiling support for Currency enum acccess
    from random import randint

    CURRENCY_NAMES_TUPLE = Currency._member_names_
    N_CURRENCY = len(CURRENCY_NAMES_TUPLE)
    N_CURRENCY_MINUS = N_CURRENCY - 1

    def get_random_currency_name():
        nth = randint(0, N_CURRENCY_MINUS)
        return CURRENCY_NAMES_TUPLE[nth]

    def get_random_currency_mapped():
        ## consistently faster, by an order of up to 300 ns (tesetd in ipython under uvloop)
        return Currency._member_map_[get_random_currency_name()]

    def get_random_currency_attr():
        return getattr(Currency, get_random_currency_name())
