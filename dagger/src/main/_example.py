import dagger
from dagger import function, object_type

@object_type
class example:
    @function
    def hello(self, name: str | None) -> str:
        if name is None:
            name = "world"
        return f"Hello, {name}"