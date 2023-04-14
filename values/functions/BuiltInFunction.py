from values import BaseFunction, Number, String, List, Dict
from results import RTResult
from errors import RTError
from resources import Context
import os


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        return f'<built-in function {self.name}>'

    def execute(self, args):
        res: RTResult = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.error:
            return res

        return_value = res.register(method(exec_ctx))
        if res.error:
            return res

        return res.success(return_value)

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    # Built-In Functions
    def execute_exec(self, exec_ctx: Context):
        local_env = {}
        code = exec_ctx.symbol_table.get("python_code").value
        exec(code, globals(), local_env)

        # Convert python dict to Lime dict
        env_str = str(local_env)
        env_str.replace("'", "")

        return RTResult().success(Dict(local_env))

    execute_exec.arg_names = ['python_code']

    def execute_print(self, exec_ctx: Context):
        print(str(exec_ctx.symbol_table.get("value")))
        return RTResult().success(Number(0))

    execute_print.arg_names = ['value']

    def execute_print_ret(self, exec_ctx: Context):
        return RTResult().success(String(str(exec_ctx.symbol_table.get("value"))))

    execute_print_ret.arg_names = ['value']

    def execute_input(self, exec_ctx: Context):
        text = input()
        return RTResult().success(String(text))

    execute_input.arg_names = []

    def execute_int_input(self, exec_ctx: Context):
        number = None
        while number is None:
            text = input()
            try:
                number = int(text)
            except ValueError:
                print(f"'{text}' must be an integer")
        return RTResult().success(Number(number))

    execute_int_input.arg_names = []

    def execute_clear(self, exec_ctx: Context):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Number(0))

    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx: Context):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number(1) if is_number else Number(0))

    execute_is_number.arg_names = ['value']

    def execute_is_string(self, exec_ctx: Context):
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number(1) if is_string else Number(0))

    execute_is_string.arg_names = ['value']

    def execute_is_list(self, exec_ctx: Context):
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number(1) if is_list else Number(0))

    execute_is_list.arg_names = ['value']

    def execute_is_function(self, exec_ctx: Context):
        is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number(1) if is_function else Number(0))

    execute_is_function.arg_names = ['value']

    def execute_append(self, exec_ctx: Context):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be a list",
                exec_ctx
            ))

        list_.elements.append(value)
        return RTResult().success(Number(0))

    execute_append.arg_names = ['list', 'value']

    def execute_pop(self, exec_ctx: Context):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be a list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be a number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))

        return RTResult().success(element)

    execute_pop.arg_names = ['list', 'index']

    def execute_extend(self, exec_ctx: Context):
        listA = exec_ctx.symbol_table.get('listA')
        listB = exec_ctx.symbol_table.get('listB')

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be a list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be a list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(Number(0))

    execute_extend.arg_names = ['listA', 'listB']

    def execute_len(self, exec_ctx: Context):
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a list",
                exec_ctx
            ))

        return RTResult().success(Number(len(list_.elements)))

    execute_len.arg_names = ["list"]

