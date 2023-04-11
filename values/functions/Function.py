from values import BaseFunction, Number
from results import RTResult
from resources import Context
import exec.Interpreter


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_return_null):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_return_null = should_return_null

    def __repr__(self):
        return f"<function {self.name}>"

    def execute(self, args):
        res: RTResult = RTResult()
        interpreter = exec.Interpreter()

        exec_ctx: Context = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.error:
            return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.error:
            return res

        return res.success(Number(0) if self.should_return_null else value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_return_null)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy