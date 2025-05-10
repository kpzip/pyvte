from typing import Any


class Context:

    def __init__(self, defined_values: dict[str, Any] | None = None):
        if defined_values is None:
            defined_values = {}
        self.defined_values = defined_values


class ReturnValues(Context):

    def __init__(self, value: Any):
        super().__init__()
        self.value = value
