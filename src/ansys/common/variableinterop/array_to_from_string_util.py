"""Definition of ArrayToFromStringUtil."""

from typing import Callable

import numpy as np
from numpy.typing import NDArray


class ArrayToFromStringUtil:
    """"""

    @staticmethod
    def value_to_string(value: NDArray, stringify_action: Callable) -> str:
        """
        TODO

        Parameters
        ----------
        value
        stringify_action

        Returns
        -------

        """
        api_string: str = ""
        # Specify bounds for arrays of more than 1d:
        if value.ndim > 1:
            api_string = "bounds[" + ','.join(map(str, value.shape)) + "]{"
        api_string += ','.join(map(stringify_action, np.nditer(value)))
        if value.ndim > 1:
            api_string += "}"
        return api_string
