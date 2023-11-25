"""Parser/Encoder Tests"""

from assertpy import assert_that  # type: ignore[import-untyped]
from immutables import Map
import os
from typing_extensions import ClassVar

from pyfx.dispatch.oanda.mapped_enum import MappedEnum

from pyfx.dispatch.oanda.test import PytestTest, run_tests


class TestMappedEnum(PytestTest):
    """Component Tests for MappedEnum"""

    def test_get_item(self):
        class EnumTest(MappedEnum):
            A = 1

        assert_that("A" in EnumTest._member_map_).is_true()
        assert_that(EnumTest.get("A")).is_equal_to(EnumTest.A)
        assert_that(EnumTest.get("A").value).is_equal_to(1)
        assert_that(EnumTest.get).raises(ValueError).when_called_with("B")

    def test_gen(self):
        values = (("a", 1), ("b", 2),)

        class EnumTest(MappedEnum):
            __gen__ = values

        assert_that(len(EnumTest._member_map_)).is_equal_to(2)

        for (key, val) in values:
            assert_that(key in EnumTest._member_map_).is_true()
            assert_that(EnumTest.get(key).value).is_equal_to(val)
            assert_that(EnumTest.get(key).name).is_equal_to(key)

    def test_finalize(self):
        class EnumTest(MappedEnum):
            a = 1
            b = 2
            __finalize__: ClassVar[bool] = True

        assert_that(EnumTest.__finalized__).is_true()
        assert_that(isinstance(EnumTest._member_map_, Map)).is_true()


if __name__ == "__main__":
    os.environ["TEST_PRINT_OBJECTS"] = "Defined"
    run_tests(__file__)
