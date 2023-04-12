from values import BaseFunction
from results import RTResult
from errors import RTError
from resources import Context
import os


class PalletFunction(BaseFunction):
    def __init__(self, name, pallet_class):
        super().__init__(name)
        self.pallet_class = pallet_class

    def __repr__(self):
        return f'<pallet function {self.name}>'

    def execute(self, args):
        res: RTResult = RTResult()

        values = self.name.split(".")
        if len(values) == 2:
            method = getattr(self.pallet_class, values[1], None)

            res.register(self.check_args(method.arg_names, args))
            if res.error:
                return res

            return_value = res.register(method(args))
            if res.error:
                return res

            return res.success(return_value)

    def copy(self):
        copy = PalletFunction(self.name, self.pallet_class)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
