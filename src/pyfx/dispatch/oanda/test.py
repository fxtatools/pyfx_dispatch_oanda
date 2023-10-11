## test.py - test support for pyfx.dispatch.oanda development

from abc import ABCMeta
from assertpy import assert_that
from datetime import datetime
import os
from os import PathLike
from polyfactory.factories import pydantic_factory
from polyfactory.constants import TYPE_MAPPING
import numpy as np
import pandas as pd
from polyfactory.field_meta import FieldMeta
from pydantic import SecretStr
import pytest
from pytest import mark
import string
import sys
from typing_extensions import ClassVar, TypeVar, get_args, get_origin, get_original_bases
from typing import Any, Generic, Literal, Optional, Sequence, Union, Mapping
from unittest import TestCase

from .credential import Credential
from .transport import ApiObject, AbstractApiClass, TransportFieldInfo, TransportTypeInfer, ApiJsonEncoder, AbstractApiObject, JsonLiteral
from .configuration import Configuration
from .api import DefaultApi
from .parser import ModelBuilder
from .models import AccountId
from .util import get_literal_value

from .models import Order, Transaction

ABSTRACT_CLASSES: Sequence[type[ApiObject]] = frozenset({Order, Transaction})

__all__ = (
    "MockFactoryClass",
    "MockFactory",
    "ComponentTest",
    "ModelTest",
)

Timpl = TypeVar("Timpl", bound=Union[type[ApiObject], type[DefaultApi]])


class MockFactoryClass(ABCMeta):
    @staticmethod
    def __new__(cls, name: str, bases: tuple[str], dct: Mapping[str, Any]):
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

    @classmethod
    def extract_field_build_parameters(cls, field_meta: FieldMeta, build_args: dict[str, Any]) -> Any:
        args = super().extract_field_build_parameters(field_meta, build_args)
        model = cls.__model__
        if issubclass(model, AbstractApiObject):  # and AbstractApiClass in model.__bases__:
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
        return "".join(np.random.choice(tuple(string.printable), size=size))

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
        return np.random.rand()

    @classmethod
    def get_provider_map(cls) -> Mapping[type, Any]:
        map = super().get_provider_map()
        ## add custom type callbacks for the polyfactory mock provider map
        map[Configuration] = cls.gen_config
        map[pd.Timestamp] = cls.gen_timestamp
        map[SecretStr] = cls.get_secret_str
        map[Credential] = cls.get_credential
        map[AccountId] = cls.get_account_id
        # map[np.double] = cls.get_random_double
        map[float] = cls.get_random_double

        return map

    @classmethod
    def build(cls, factory_use_construct: bool = True, **kwargs: Any) -> Timpl:
        mcls = cls.__model__
        if issubclass(mcls, AbstractApiObject):
            # the model class is an abstract subclass of AbstractApiobject
            types_map = mcls.types_map
            nr_concrete_cls = len(types_map)
            rnd = np.random.randint(0, max(1, nr_concrete_cls - 1))
            designator = tuple(types_map.keys())[rnd]
            mock_cls = tuple(types_map.values())[rnd]
            kwargs[mcls.designator_key] = designator
        return super().build(factory_use_construct, **kwargs)


class ComponentTest(TestCase):
    pass


class ModelTest(ComponentTest, Generic[Timpl]):
    __factory__: ClassVar[type[MockFactory[Timpl]]]  # = MockFactory[ApiObject]

    json_encoder: ApiJsonEncoder

    def setUp(self):
        self.json_encoder = ApiJsonEncoder()
        for mcls in ABSTRACT_CLASSES:
            # for each abstract model class, bind a randomly selected
            # concrete class to represent the abstract class in mocks
            #
            # - TBD between gen => parse
            types_map = mcls.types_map
            nr_concrete_cls = len(types_map)
            rnd = np.random.randint(0, max(1, nr_concrete_cls - 1))
            ccls = tuple(types_map.values())[rnd]
            TYPE_MAPPING[mcls] = ccls

    # def tearDown(self):
    #     pass

    @classmethod
    def assert_recursive_eq(cls, inst_a, inst_b):
        acls = inst_a.__class__

        # ? TBD testing compatible types  @ test_data-model and main tests
        assert_that(issubclass(acls, inst_b.__class__)).is_true()

        if issubclass(acls, ApiObject):
            fset_a = inst_a.__pydantic_fields_set__
            fset_b = inst_b.__pydantic_fields_set__
            assert_that(fset_a).is_equal_to(fset_b)
            for f in fset_a:
                f_a = getattr(inst_a, f)
                f_b = getattr(inst_b, f)
                cls.assert_recursive_eq(f_a, f_b)
        elif isinstance(inst_a, str):
            assert_that(inst_a).is_equal_to(inst_b)
        elif isinstance(inst_a, Sequence):
            len_a = len(inst_a)
            len_b = len(inst_b)
            assert_that(len_a).is_equal_to(len_b)
            for n in range(0, len_a):
                nth_a = inst_a[n]
                nth_b = inst_b[n]
                cls.assert_recursive_eq(nth_a, nth_b)
        else:
            assert_that(inst_a).is_equal_to(inst_b)

    @classmethod
    def get_model_class(cls) -> type[ApiObject]:
        factory_cls: MockFactory = cls.__factory__
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
        if to_mock:
            model_cls = to_mock
        else:
            if cls.__class__ is ModelTest:
                return
            model_cls = cls.get_model_class()

        mock_initargs = {}
        if isinstance(model_cls, AbstractApiClass):
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
                ## not an abstract class - no default args to add
                pass
        if to_mock:
            ## not as yet tested - see previous
            class MockTest(ModelTest[to_mock]):
                class Factory(MockFactory[to_mock]):
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
        assert_that(hasattr(model_cls, "api_fields")).is_true()
        fields = model_cls.model_fields
        field_names = model_cls.api_fields
        for name, info in fields.items():
            assert_that(isinstance(info, TransportFieldInfo)).is_true()
            info: TransportFieldInfo
            # test metadata for the field info object
            assert_that(info.field_name).is_equal_to(name)
            assert_that(issubclass(model_cls, info.defining_class)).is_true()
            # ensure that a concrete transport type was inferred during ApiObject
            # class initialization
            assert_that(issubclass(info.transport_type, TransportTypeInfer)).is_false()
            # test name<->info mapping in the model class
            assert_that(name in field_names).is_true()
            assert_that(field_names[name] is info).is_true()
            alias = info.alias
            if alias:
                assert_that(alias in field_names).is_true()
                assert_that(field_names[alias] is info).is_true()

    @mark.dependency(depends_on="test_model_cls_fields")
    def test_mapping_transform(self):
        # raise ValueError("THUNK", os.environ) => ... PYTEST_CURRENT_TEST ...
        cls = self.__class__
        if cls is ModelTest:
            return

        inst = self.__class__.gen_mock()
        assert_that(inst).is_equal_to(inst)

        dct = inst.to_dict()
        assert_that(isinstance(dct, Mapping)).is_true()

        dct_inst = inst.__class__.from_dict(dct)
        assert_that(dct_inst.__class__ is inst.__class__).is_true()
        self.__class__.assert_recursive_eq(inst, dct_inst)

    @mark.dependency(depends_on="test_model_cls_fields")
    def test_json_transform(self):
        cls = self.__class__
        if cls is ModelTest:
            return

        encoder = self.json_encoder

        inst = self.__class__.gen_mock()
        assert_that(inst).is_equal_to(inst)

        j_str: str = inst.to_json_str(encoder)
        assert_that(isinstance(j_str, str)).is_true()

        ## yajl parser expects bytes input, thus calling encode() on the str ...
        j_inst = ModelBuilder.from_text(inst.__class__, j_str.encode())
        assert_that(j_inst.__class__ is inst.__class__).is_true()
        ## test equiv ...
        self.__class__.assert_recursive_eq(inst, j_inst)


def run_tests(*files: Sequence[PathLike]):
    ## general assumption: if run_tests is called, it's usually for interactive
    ## test debugging, thus adding --pdb to args
    if "NO_PDB" in os.environ:
        argv = list(files)
    else:
        argv = ["--pdb", *files]
    stdout = sys.stdout
    stderr = sys.stderr
    stdin = sys.stdin
    try:
        pytest.main(argv)
    finally:
        sys.stdout = stdout
        sys.stderr = stderr
        sys.stdin = stdin
