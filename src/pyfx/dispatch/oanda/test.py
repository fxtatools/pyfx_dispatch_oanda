## test.py - test support for pyfx.dispatch.oanda development

from abc import ABC, ABCMeta
from assertpy import assert_that  # type: ignore[import-untyped]
from datetime import datetime
import os
from polyfactory.factories import pydantic_factory
from polyfactory.constants import TYPE_MAPPING
import numpy as np
import pandas as pd
from polyfactory.field_meta import FieldMeta
from pydantic import SecretStr, ValidationError
import pytest
from pytest import mark
import string
import sys
from typing_extensions import ClassVar, TypeVar, get_args, get_origin, get_original_bases
from typing import Any, Generic, Literal, Optional, Sequence, Mapping
from unittest import TestCase


from .credential import Credential
from .transport import (  # type: ignore
    ApiObject, AbstractApiClass, TransportFieldInfo,
    TransportTypeInfer, AbstractApiObject,
    TransportTypeClass, TransportFloatStr
    )
from .configuration import Configuration
from .parser import ModelBuilder
from .transport.account_id import AccountId
from .util.typeref import get_literal_value

from .models import Order, Transaction, CreateOrderRequest, Time, InstrumentName, Currency, CurrencyPair

ABSTRACT_CLASSES: frozenset[type[ApiObject]] = frozenset({Order, Transaction, CreateOrderRequest})

__all__ = (
    "assert_recursive_eq",
    "MockFactoryClass",
    "MockFactory",
    "PytestTest",
    "ComponentTest",
    "ModelTest",
    "RequestTest",
    "run_tests"
)

Timpl = TypeVar("Timpl", bound=ApiObject)


def assert_recursive_eq(inst_a, inst_b):
    acls = inst_a.__class__
    bcls = inst_b.__class__

    assert_that(issubclass(acls, bcls)).is_true()

    if issubclass(acls, ApiObject):
        fset_a: set = inst_a.__pydantic_fields_set__
        fset_b: set = inst_b.__pydantic_fields_set__
        # assert_that(fset_a).is_equal_to(fset_b)
        assert_that(fset_b.difference(fset_a)).is_equal_to(set())
        for f in fset_a:
            f_a = getattr(inst_a, f)
            f_b = getattr(inst_b, f)
            assert_recursive_eq(f_a, f_b)
    elif isinstance(inst_a, str):
        assert_that(inst_a).is_equal_to(inst_b)
    elif isinstance(inst_a, Sequence):
        len_a = len(inst_a)
        len_b = len(inst_b)
        assert_that(len_a).is_equal_to(len_b)
        for n in range(0, len_a):
            nth_a = inst_a[n]
            nth_b = inst_b[n]
            assert_recursive_eq(nth_a, nth_b)
    elif inst_a is pd.NaT:
        assert_that(inst_a is inst_b).is_true()
    else:
        assert_that(inst_a).is_equal_to(inst_b)



class MockFactoryClass(ABCMeta):
    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, Any]):
        overrides = None
        if "__model__" not in dct and "__orig_bases__" in dct:
            ## set the polyfactory.*.pydantic_factory __model__ for the derived class,
            ## using a parameter to the derived class' generic base class
            first = dct["__orig_bases__"][0]
            args = get_args(first)
            overrides = dict(__model__=args[0])
        if overrides:
            dct.update(overrides)
        return super().__new__(cls, name, bases, dct)


class MockFactory(pydantic_factory.ModelFactory[Timpl], Generic[Timpl], metaclass=MockFactoryClass):
    __is_base_factory__ = True
    # set common class parameters for polyfactory.*.pydantic_factory
    __randomize_collection_length__ = False
    __allow_none_optionals__ = False
    # The derived class must have a __model__, when defined.
    # This parameter will be overidden in subclasses
    __model__ = ApiObject

    random_str_chars = tuple(frozenset(string.ascii_letters + string.digits + string.punctuation) - {'\\', "`", '"', "'"})

    @classmethod
    def extract_field_build_parameters(cls, field_meta: FieldMeta, build_args: dict[str, Any]) -> Any:
        args = super().extract_field_build_parameters(field_meta, build_args)
        model = cls.__model__
        if issubclass(model, AbstractApiObject) and AbstractApiClass in model.__bases__:
            if not args:
                args = {}
            types_map = model.types_map
            nr_concrete_cls = len(types_map)
            rnd = np.random.randint(0, max(nr_concrete_cls - 1, 1))
            designator = tuple(types_map.keys())[rnd]
            args["type"] = designator
        return args

    @classmethod
    def get_random_str(cls, size: int = 24):
        return "".join(np.random.choice(cls.random_str_chars, size=size))

    @classmethod
    def get_credential(cls, size: int = 24):
        return Credential(cls.get_random_str(size))

    @classmethod
    def get_secret_str(cls):
        return SecretStr(cls.get_random_str(24))

    @classmethod
    def get_account_id(cls):
        return AccountId(cls.get_random_str(20))

    @classmethod
    def gen_config(cls):
        return Configuration(True, access_token=cls.get_credential(65))

    @classmethod
    def gen_timestamp(cls):
        return pd.to_datetime(np.random.randint(datetime.now().timestamp()), unit='s')

    @classmethod
    def get_random_double(cls):
        return np.double(np.random.rand())

    @classmethod
    def get_currency_pair(cls) -> CurrencyPair:
        symbols = tuple(Currency.__members__.keys())
        n_cur = len(symbols)
        nth_base = np.random.randint(0, n_cur)
        nth_quote = nth_base
        while nth_quote == nth_base:
            nth_quote = np.random.randint(0, n_cur)
        base_name = symbols[nth_base]
        quote_name = symbols[nth_quote]
        return CurrencyPair.from_str_pair(base_name, quote_name)

    @classmethod
    def get_provider_map(cls) -> dict[type, Any]:
        map = super().get_provider_map()
        ## add custom type callbacks for the polyfactory mock provider map
        map[Configuration] = cls.gen_config
        map[pd.Timestamp] = cls.gen_timestamp
        map[Time] = cls.gen_timestamp
        map[datetime] = cls.gen_timestamp
        map[SecretStr] = cls.get_secret_str
        map[Credential] = cls.get_credential
        map[AccountId] = cls.get_account_id
        # map[np.double] = cls.get_random_double
        map[float] = cls.get_random_double
        map[InstrumentName] = cls.get_currency_pair
        for scls in TransportFloatStr.__subclasses__():
            ## add a mapping for each TransportFloatStr implementation class
            if scls.__class__ is not TransportTypeClass:
                map[scls] = cls.get_random_double
        return map

    @classmethod
    def build(cls, factory_use_construct: bool = True, **kwargs: Any) -> Timpl:
        mcls = cls.__model__
        if issubclass(mcls, AbstractApiObject) and ABC in mcls.__bases__:
            types_map = mcls.types_map
            nr_concrete_cls = len(types_map)
            rnd = np.random.randint(0, max(1, nr_concrete_cls - 1))
            designator = tuple(types_map.keys())[rnd]
            # mock_cls = tuple(types_map.values())[rnd]
            kwargs[mcls.designator_key] = designator
        else:
            for name, fieldinfo in mcls.model_fields.items():
                # ensure non-key literal args are expressly set for
                # mock initargs, from the original literal value
                #
                # this may serve to prevent a certain false-negative
                # test failure onto 'type' fields for non-abstract
                # model classes
                origin = get_origin(fieldinfo.annotation)
                if origin and origin == Literal:
                    kwargs[name] = fieldinfo.get_default()
        return super().build(factory_use_construct, **kwargs)


class PytestTest():
    ## base class for test classes using pytest features, e.g fixtures and parameterization
    pass


class ComponentTest(PytestTest):
    ## base class for tests classes with unit test features, e.g setUp()
    pass


class ModelTest(ComponentTest, TestCase, Generic[Timpl]):
    ## base class for API class tests
    __factory__: ClassVar[type[MockFactory]]

    def setUp(self):
        for mcls in ABSTRACT_CLASSES:
            assert AbstractApiObject in mcls.__bases__, "Not an abstract API class"

            # for each abstract model class, bind a randomly selected
            # concrete class to represent the abstract class in mocks
            #
            # - TBD between gen => parse
            types_map = mcls.types_map
            nr_concrete_cls = len(types_map)
            rnd = np.random.randint(0, max(1, nr_concrete_cls - 1))
            ccls = tuple(types_map.values())[rnd]
            # assert AbstractApiObject in ccls.__mro__, "Not an abstract implementation class"
            assert mcls in ccls.__mro__, "Not an abstract implementation class"
            TYPE_MAPPING[mcls] = ccls

    # def tearDown(self):
    #     pass

    @classmethod
    def get_model_class(cls) -> type[ApiObject]:
        factory_cls: type[MockFactory] = cls.__factory__
        # using generic type parameters, determine the model class
        # applied for the test class' mock factory
        for base in get_original_bases(factory_cls):
            origin = get_origin(base)
            if issubclass(origin, MockFactory):
                args = get_args(base)
                if args:
                    first_arg = args[0]
                    if issubclass(first_arg, ApiObject):
                        return first_arg
        raise AssertionError("Unable to determine model class")

    @classmethod
    def gen_mock(cls, to_mock: Optional[type[ApiObject]] = None):
        is_mapped: bool = False
        if to_mock:
            model_cls = to_mock
        elif cls.__class__ is ModelTest:
            return
        else:
            base_cls = cls.get_model_class()
            if base_cls in TYPE_MAPPING:
                ## base_cls is an abstract model class - see TYPE_MAPPING hacks, above
                model_cls = TYPE_MAPPING[base_cls]  # type: ignore
                is_mapped = True
            else:
                model_cls = cls.get_model_class()

        mock_initargs = dict()
        if ABC in model_cls.__bases__:
            fields = model_cls.model_fields
            key_field = model_cls.designator_key
            if key_field in fields:
                field_info = fields[key_field]
                annot = field_info.annotation
                if get_origin(annot) == Literal:
                    ## set the key field to its required value, in args for the mock
                    # raise ValueError("Break %s %s %s" %  (key_field, get_args(annot)[0], model_cls.__name__))
                    mock_initargs[key_field] = get_literal_value(annot)
                else:
                    raise ValueError("key_field does not provide a Literal annotation", key_field, annot, model_cls)
            else:
                raise Exception("Abstract key field not found for implementation class", key_field, model_cls)

        if to_mock or is_mapped:
            mock_base = to_mock or model_cls
            ## generate an ephemeral mock class
            class MockTest(ModelTest[mock_base]):
                class Factory(MockFactory[mock_base]):
                    pass
                __factory__ = Factory
            return MockTest.__factory__.build(True, **mock_initargs)
        else:
            return cls.__factory__.build(True, **mock_initargs)

    @mark.dependency()
    def test_model_cls_fields(self):
        test_cls = self.__class__
        if test_cls is ModelTest:
            return
        model_cls = self.__class__.get_model_class()
        # validity tests for the model class
        # alo test field definitions in the model class
        assert_that(model_cls).is_not_none()
        assert_that(issubclass(model_cls, ApiObject)).is_true()
        assert_that(hasattr(model_cls, "model_fields")).is_true()
        assert_that(hasattr(model_cls, "json_fields")).is_true()
        fields = model_cls.model_fields
        json_fields = model_cls.json_fields
        for name, info in fields.items():
            assert_that(isinstance(info, TransportFieldInfo)).is_true()
            info: TransportFieldInfo
            # test metadata for the field info object
            assert_that(info.name).is_equal_to(name)
            assert_that(issubclass(model_cls, info.defining_class)).is_true()
            # ensure that a concrete transport type was inferred during ApiObject
            # class initialization
            assert_that(issubclass(info.transport_type, TransportTypeInfer)).is_false()
            # test json name<->info mapping in the model class
            json_name = info.alias or name
            assert_that(json_name in json_fields).is_true()
            assert_that(json_fields[json_name] is info).is_true()

    @mark.dependency(depends_on="test_model_cls_fields")
    def test_mapping_transform(self):
        cls = self.__class__
        if cls is ModelTest:
            return

        inst: Timpl = self.__class__.gen_mock()
        assert_recursive_eq(inst, inst)

        dct = inst.to_dict()
        assert_that(isinstance(dct, Mapping)).is_true()

        dct_inst = inst.__class__.from_dict(dct)
        assert_that(dct_inst.__class__ is inst.__class__).is_true()
        assert_recursive_eq(inst, dct_inst)

    @mark.dependency(depends_on="test_model_cls_fields")
    def test_json_transform(self):
        cls = self.__class__
        if cls is ModelTest:
            return

        inst: Timpl = self.__class__.gen_mock()
        assert_recursive_eq(inst, inst)

        icls = inst.__class__

        if  issubclass(icls, AbstractApiObject):
            key = icls.designator_key
            assert_that(hasattr(inst, key)).is_true()

        j_str: str = inst.to_json_str()
        assert_that(isinstance(j_str, str)).is_true()

        ## yajl parser expects bytes input, thus calling encode() on the str ...
        try:
            j_inst = ModelBuilder.from_text(inst.__class__, j_str.encode())
        except ValidationError as exc:
            ## this section can receive a breakpoint for interactive debugging
            ##
            ## ensuring the backtrace will be somehow avaialble in the bugger ...
            import traceback
            _ = sys.exc_info()
            raise exc
        assert_that(j_inst.__class__ is inst.__class__).is_true()
        ## test equiv ...
        assert_recursive_eq(inst, j_inst)


def run_tests(*files: str):
    ## general assumption: if run_tests is called, it's usually for interactive
    ## test debugging, thus adding --pdb to args
    argv = []
    if "NO_PDB" not in os.environ:
        argv.append("--pdb")
    argv.extend(files)
    stdout = sys.stdout
    stderr = sys.stderr
    stdin = sys.stdin
    try:
        pytest.main(argv)
    finally:
        sys.stdout = stdout
        sys.stderr = stderr
        sys.stdin = stdin
