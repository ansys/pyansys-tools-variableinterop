
from abc import ABC
from functools import cached_property
from typing import Any, Optional, Type
from ansys.tools.variableinterop.api.exceptions import IncompatibleTypesError
from ansys.tools.variableinterop.api.itype_library import ITypeInformation, ITypeLibrary, TypesRequired


class AbstractInitializerTypeLibrary(ITypeLibrary, ABC):

    @cached_property
    def type_to_typeinfo(self) -> dict[Type, ITypeInformation]:
        return {t.value_type:t for (t) in self.allowed_types}

    def runtime_convert(self, source: Any, source_type: Type, dest_type: Type) -> Any:
        source_ti: Optional[ITypeInformation] = self.type_to_typeinfo.get(source_type)
        dest_ti: Optional[ITypeInformation] = self.type_to_typeinfo.get(dest_type)

        if source_ti is None or dest_ti is None:
            if source_ti is None:
                source_name: Optional[str] = TypesRequired.get(source_type)
                if source_name is None:
                    raise IncompatibleTypesError(source_type.__name__, dest_type.__name__)
                source_ti = self.get_type(source_name)
            if dest_ti is None:
                dest_name: Optional[str] = TypesRequired.get(dest_type)
                if dest_name is None:
                    raise IncompatibleTypesError(source_type.__name__, dest_type.__name__)
                dest_ti = self.get_type(dest_name)
            if source_ti.canonical_name != dest_ti.canonical_name:
                raise IncompatibleTypesError(source_type.__name__, dest_type.__name__)                
        elif not self.is_linking_allowed(source_ti.canonical_name, dest_ti.canonical_name).allowed:
            raise IncompatibleTypesError(source_type.__name__, dest_type.__name__)
        
        return dest_type(source)  
