
def _f() -> None: pass


def null() -> None: pass


class function:
    # TODO not defined in builtins!
    Any = object()
    CodeType = type(_f.__code__)

    __name__: str
    __module__: str
    __code__: CodeType
    __qualname__: str
    __annotations__: dict[str, Any]
