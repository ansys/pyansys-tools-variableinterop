from typing import Any, Dict, Iterable, Type, Union

from ansys.tools.variableinterop.array_metadata import BooleanArrayMetadata, IntegerArrayMetadata, RealArrayMetadata, StringArrayMetadata
from ansys.tools.variableinterop.array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from ansys.tools.variableinterop.common_variable_metadata import CommonVariableMetadata
from ansys.tools.variableinterop.exceptions import VariableTypeUnknownError
from ansys.tools.variableinterop.file_array_metadata import FileArrayMetadata
from ansys.tools.variableinterop.file_array_value import FileArrayValue
from ansys.tools.variableinterop.file_metadata import FileMetadata
from ansys.tools.variableinterop.file_value import EMPTY_FILE, FileValue
from ansys.tools.variableinterop.ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
from ansys.tools.variableinterop.scalar_metadata import BooleanMetadata, IntegerMetadata, RealMetadata, StringMetadata
from ansys.tools.variableinterop.scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from ansys.tools.variableinterop.variable_type import VariableType
from ansys.tools.variableinterop.variable_value import IVariableValue

_class_map: dict[VariableType, Type] = {
        VariableType.STRING: StringValue,
        VariableType.REAL: RealValue,
        VariableType.INTEGER: IntegerValue,
        VariableType.BOOLEAN: BooleanValue,
        VariableType.FILE: FileValue,
        VariableType.STRING_ARRAY: StringArrayValue,
        VariableType.REAL_ARRAY: RealArrayValue,
        VariableType.INTEGER_ARRAY: IntegerArrayValue,
        VariableType.BOOLEAN_ARRAY: BooleanArrayValue,
        VariableType.FILE_ARRAY: FileArrayValue,
    }

_map_class: dict[Type, VariableType] = {t: vt for (vt, t) in _class_map.items() }

class VariableFactory:

    @staticmethod
    def associated_type_name(type: VariableType) -> str:
        """Get the name of the associated ``IVariableValue`` type."""
        if type == VariableType.UNKNOWN:
            return "unknown"
        return VariableFactory.associated_type(type).__name__

    @staticmethod
    def associated_type(type: VariableType) -> Type:
        """Get the associated ``IVariableValue`` type."""

        if Type == VariableType.UNKNOWN:
            raise VariableTypeUnknownError()

        return _class_map[type]

    @staticmethod
    def from_type(t: Type) -> VariableType:
        return _map_class.get(t, VariableType.UNKNOWN)

    @staticmethod
    def from_string(s: str) -> VariableType:
        """
        Get the ``VariableType`` value from a string.

        Parameters
        ----------
        s : str
            String to convert to a ``VariableType`` value.

        Returns
        -------
        VariableType
            Result.
        """

        class __IterableKeyDict(Dict[Union[Iterable, str], Any]):
            """Provides a dictionary that can initialize with iterable keys and give
            each value its own entry."""

            def __init__(self, d_: Dict[Union[Iterable, str], VariableType]):
                def __br():
                    """Break down initializer dictionary to tuple subkeys."""
                    for k, v in d_.items():
                        if isinstance(k, str):
                            yield k, v
                        else:
                            for subkey in k:
                                yield subkey, v

                super().__init__(__br())

        __valtype_strings: Dict[Union[Iterable, str], VariableType] = __IterableKeyDict(
            {
                ("int", "integer", "long"): VariableType.INTEGER,
                ("real", "double", "float"): VariableType.REAL,
                ("bool", "boolean"): VariableType.BOOLEAN,
                ("str", "string"): VariableType.STRING,
                "file": VariableType.FILE,
                ("int[]", "integer[]", "long[]"): VariableType.INTEGER_ARRAY,
                ("real[]", "double[]", "float[]"): VariableType.REAL_ARRAY,
                ("bool[]", "boolean[]"): VariableType.BOOLEAN_ARRAY,
                ("str[]", "string[]"): VariableType.STRING_ARRAY,
                "file[]": VariableType.FILE_ARRAY,
            }
        )

        try:
            return __valtype_strings[s.strip().lower()]
        except KeyError:
            return VariableType.UNKNOWN

    @staticmethod
    def get_default_value(type: VariableType) -> IVariableValue:
        """
        Construct the default value for this type.

        Returns
        -------
        IVariableValue
            New value object whose type matches this type.
        """

        class __DefaultValueVisitor(IVariableTypePseudoVisitor[IVariableValue]):
            """Provides the visitor that returns a default value for each type."""

            def visit_unknown(self) -> IVariableValue:
                raise VariableTypeUnknownError

            def visit_int(self) -> IVariableValue:
                return IntegerValue(0)

            def visit_real(self) -> IVariableValue:
                return RealValue()

            def visit_boolean(self) -> IVariableValue:
                return BooleanValue()

            def visit_string(self) -> IVariableValue:
                return StringValue()

            def visit_file(self) -> IVariableValue:
                return EMPTY_FILE

            def visit_int_array(self) -> IVariableValue:
                return IntegerArrayValue()

            def visit_real_array(self) -> IVariableValue:
                return RealArrayValue()

            def visit_bool_array(self) -> IVariableValue:
                return BooleanArrayValue()

            def visit_string_array(self) -> IVariableValue:
                return StringArrayValue()

            def visit_file_array(self) -> IVariableValue:
                return FileArrayValue()

        visitor = __DefaultValueVisitor()
        return vartype_accept(visitor, type)


    @staticmethod
    def construct_variable_metadata(type: VariableType) -> CommonVariableMetadata:
        """
        Construct the default metadata for this type.

        Returns
        -------
        CommonVariableMetadata
            New metadata object whose type matches this type.
        """

        class __DefaultMetadataVisitor(IVariableTypePseudoVisitor[CommonVariableMetadata]):
            """Provides the visitor that returns a default metadata for each type."""

            def visit_unknown(self) -> CommonVariableMetadata:
                raise VariableTypeUnknownError

            def visit_int(self) -> CommonVariableMetadata:
                return IntegerMetadata()

            def visit_real(self) -> CommonVariableMetadata:
                return RealMetadata()

            def visit_boolean(self) -> CommonVariableMetadata:
                return BooleanMetadata()

            def visit_string(self) -> CommonVariableMetadata:
                return StringMetadata()

            def visit_file(self) -> CommonVariableMetadata:
                return FileMetadata()

            def visit_int_array(self) -> CommonVariableMetadata:
                return IntegerArrayMetadata()

            def visit_real_array(self) -> CommonVariableMetadata:
                return RealArrayMetadata()

            def visit_bool_array(self) -> CommonVariableMetadata:
                return BooleanArrayMetadata()

            def visit_string_array(self) -> CommonVariableMetadata:
                return StringArrayMetadata()

            def visit_file_array(self) -> CommonVariableMetadata:
                return FileArrayMetadata()

        visitor = __DefaultMetadataVisitor()
        return vartype_accept(visitor, type)
