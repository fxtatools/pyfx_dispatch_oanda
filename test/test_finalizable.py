"""Unit tests for Finalizble, FinalizableClass"""

from assertpy import assert_that
from typing_extensions import ClassVar

from pyfx.dispatch.oanda.test import ComponentTest, run_tests

from pyfx.dispatch.oanda.finalizable import FinalizableClass, FinalizationState


class TestFinalizable(ComponentTest):

    def test_finalizable_class(self):

        class TestMetaFinalizable(FinalizableClass):

            test_flag: bool = False

            def __finalize_instance__(self):
                self.test_flag = True
                return super().__finalize_instance__()

        class ThunkA(metaclass=TestMetaFinalizable):
            __finalize__: ClassVar[bool] = True

        assert_that(ThunkA.__finalized__).is_true()
        assert_that(ThunkA.test_flag).is_true()
        assert_that(TestMetaFinalizable.test_flag).is_false()

        class ThunkB(metaclass=TestMetaFinalizable):
            __finalize__: ClassVar[bool] = False

        assert_that(ThunkB.__finalized__).is_false()
        assert_that(ThunkB.test_flag).is_false()

        ThunkB.__finalize_instance__()
        assert_that(ThunkB.__finalized__).is_true()
        assert_that(ThunkB.test_flag).is_true()
        assert_that(TestMetaFinalizable.test_flag).is_false()

        class ThunkC(metaclass=TestMetaFinalizable):
            __finalization_state__: ClassVar[FinalizationState] = FinalizationState.NEVER

        assert_that(ThunkC.__finalized__).is_false()  # fails, cannot set the  metaclass instance var via the class definition ???
        assert_that(ThunkC.test_flag).is_false()
        ThunkC.__finalize_instance__()
        assert_that(ThunkC.__finalized__).is_false()
        assert_that(ThunkC.test_flag).is_true()

    # assert_that(dispatch.JsonTypesRepository.__finalized__).is_false()
    # dispatch.JsonTypesRepository.__finalize_instance__()
    # assert_that(dispatch.JsonTypesRepository.__finalized__).is_true()
    # for cls, typ in the_repository.types_map:
    #   if isinstance(cls, Finalizable): assert_that(cls.__finalized__).is_true()
    #   if isinstance(typ, Finalizable): assert_that(typ.__finalized__).is_true()


if __name__ == "__main__":
    run_tests(__file__)
