from values import Value


class Dict(Value):
    def __init__(self, dict_):
        super().__init__()
        self.dict = dict_

    def __repr__(self):
        return str(self.dict)

    def copy(self):
        copy = Dict(self.dict)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
