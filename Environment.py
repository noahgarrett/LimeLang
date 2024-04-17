from llvmlite import ir

class Environment:
    """ Symbol Table """
    def __init__(self, records: dict[str, tuple[ir.Value, ir.Type]] = None, parent = None, name: str = "global") -> None:
        self.records: dict[str, tuple] = records if records else {}
        self.parent: Environment | None = parent
        self.name: str = name

    def define(self, name: str, value: ir.Value, _type: ir.Type) -> str:
        self.records[name] = (value, _type)
        return value
    
    def lookup(self, name: str) -> tuple[ir.Value, ir.Type]:
        return self.__resolve(name)
    
    def __resolve(self, name: str) -> tuple[ir.Value, ir.Type]:
        if name in self.records:
            return self.records[name]
        elif self.parent:
            return self.parent.__resolve(name)
        else:
            return None
            # raise RuntimeError(f"Undefined variable '{name}' in `{self.name}`'s scope.")
