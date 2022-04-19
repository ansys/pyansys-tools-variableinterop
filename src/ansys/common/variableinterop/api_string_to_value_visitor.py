"""
Provides a variable type pseudo-visitor that parses values from strings.

The pseudo-visitor is constructed with the string to parse, then accepted
by the appropriate variable type. When visiting, it attempts to parse
the string into the visited type. See the pseudo-visitor interface
definition for more information as to why this pattern is beneficial
compared to bare switch statements.
"""
import json

from ansys.common.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
import ansys.common.variableinterop.file_scope as file_scope
import ansys.common.variableinterop.ivariable_type_pseudovisitor as pv_interface
from ansys.common.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
import ansys.common.variableinterop.variable_value as var_value


class APIStringToValueVisitor(pv_interface.IVariableTypePseudoVisitor):
    """
    A pseudo-visitor for the variable type enum that produces variable values from strings.

    The actual type generated is determined by the type that accepts this visitor.
    """

    def __init__(self, source: str, fscope: file_scope.FileScope):
        """
        Create a new instance of this class.

        Parameters
        ----------
        source the string from which values should be parsed
        """
        self._source: str = source
        self._scope: file_scope.FileScope = fscope

    def visit_unknown(self):
        """
        Visit the UNKNOWN variable type.

        Given that variables of type Unknown cannot actually be produced,
        this method always raises.

        Returns
        -------
        Never returns; always raises NotImplementedError

        Raises
        ------
        NotImplementedError always

        """
        raise NotImplementedError("Cannot create values with unknown type.")

    def visit_int(self) -> IntegerValue:
        """
        Produce an IntegerValue from the API string format.

        Returns
        -------
        An IntegerValue with a value determined by the specified string.
        """
        return IntegerValue.from_api_string(self._source)

    def visit_real(self) -> RealValue:
        """
        Produce a RealValue from the API string format.

        Returns
        -------
        A RealValue with a value determined by the specified string.
        """
        return RealValue.from_api_string(self._source)

    def visit_boolean(self) -> BooleanValue:
        """
        Produce a BooleanValue from the API string format.

        Returns
        -------
        A BooleanValue with a value determined by the specified string.
        """
        return BooleanValue.from_api_string(self._source)

    def visit_string(self) -> StringValue:
        """
        Produce a StringValue from the API string format.

        Returns
        -------
        A StringValue with a value determined by the specified string.
        """
        return StringValue.from_api_string(self._source)

    def visit_file(self) -> var_value.IVariableValue:
        """
        Produce a FileValue from the API string format.

        Returns
        -------
        A FileValue with a value determined by the specified string.
        """
        # TODO: implement this as part of file support PBI.
        # Note that doing so will also require extending this
        # class to take a file store (see C# implementation for details).
        if self._scope is None:
            raise NotImplementedError("Deserializing a file value requires a file scope.")
        else:
            return self._scope.from_api_object(json.loads(self._source))

    def visit_int_array(self) -> IntegerArrayValue:
        """
        Produce an IntegerArrayValue from the API string format.

        Returns
        -------
        An IntegerArrayValue with a value determined by the specified string.
        """
        return IntegerArrayValue.from_api_string(self._source)

    def visit_real_array(self) -> RealArrayValue:
        """
        Produce a RealArrayValue from the API string format.

        Returns
        -------
        A RealArrayValue with a value determined by the specified string.
        """
        return RealArrayValue.from_api_string(self._source)

    def visit_bool_array(self) -> BooleanArrayValue:
        """
        Produce a BooleanArrayValue from the API string format.

        Returns
        -------
        A BooleanArrayValue with a value determined by the specified string.
        """
        return BooleanArrayValue.from_api_string(self._source)

    def visit_string_array(self) -> StringArrayValue:
        """
        Produce a StringArrayValue from the API string format.

        Returns
        -------
        A StringArrayValue with a value determined by the specified string.
        """
        return StringArrayValue.from_api_string(self._source)

    def visit_file_array(self) -> var_value.IVariableValue:
        """
        Produce a FileArrayValue from the API string format.

        Returns
        -------
        A FileArrayValue with a value determined by the specified string.
        """
        # TODO: implement this as part of array support PBI.
        raise NotImplementedError
