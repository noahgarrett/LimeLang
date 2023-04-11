from resources import NumberNode, BinOpNode, UnaryOpNode, VarAssignNode, VarAccessNode, IfNode, ForNode
from resources import WhileNode, FuncDefNode, CallNode, StringNode, ListNode
from resources import TokenTypes
from resources import Context
from results import RTResult
from errors import RTError
from values import Number, Function, String, List


class Interpreter:
    def __init__(self):
        pass

    def visit(self, node: NumberNode | BinOpNode | UnaryOpNode, context: Context):
        method_name: str = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context: Context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node: NumberNode, context: Context) -> Number:
        return RTResult().success(
            Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node: StringNode, context: Context):
        return RTResult().success(
            String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node: ListNode, context: Context):
        res: RTResult = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node: VarAccessNode, context: Context):
        res: RTResult = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end, f"'{var_name}' is not defined", context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        res: RTResult = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node: BinOpNode, context: Context) -> RTResult:
        res: RTResult = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.operator_token.type == TokenTypes.TT_PLUS:
            result, error = left.added_to(right)
        elif node.operator_token.type == TokenTypes.TT_MINUS:
            result, error = left.subtracted_by(right)
        elif node.operator_token.type == TokenTypes.TT_MUL:
            result, error = left.multiplied_by(right)
        elif node.operator_token.type == TokenTypes.TT_DIV:
            result, error = left.divided_by(right)
        elif node.operator_token.type == TokenTypes.TT_POW:
            result, error = left.powered_by(right)
        elif node.operator_token.type == TokenTypes.TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.operator_token.type == TokenTypes.TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.operator_token.type == TokenTypes.TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.operator_token.type == TokenTypes.TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.operator_token.type == TokenTypes.TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.operator_token.type == TokenTypes.TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.operator_token.matches(TokenTypes.TT_KEYWORD, "and"):
            result, error = left.anded_by(right)
        elif node.operator_token.matches(TokenTypes.TT_KEYWORD, "or"):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node: UnaryOpNode, context: Context) -> RTResult:
        res: RTResult = RTResult()
        number: Number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None

        if node.operator_token.type == TokenTypes.TT_MINUS:
            number, error = number.multiplied_by(Number(-1))
        elif node.operator_token.matches(TokenTypes.TT_KEYWORD, "not"):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node: IfNode, context: Context):
        res: RTResult = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error:
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error:
                    return res
                return res.success(Number(0) if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            else_value = res.register(self.visit(expr, context))
            if res.error:
                return res
            return res.success(Number(0) if node.should_return_null else else_value)

        return res.success(Number(0))

    def visit_ForNode(self, node: ForNode, context: Context):
        res: RTResult = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error:
            return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error:
            return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error:
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error:
                return res

        return res.success(
            Number(0) if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node: WhileNode, context: Context):
        res: RTResult = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res

            if not condition.is_true():
                break

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error:
                return res

        return res.success(
            Number(0) if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_FuncDefNode(self, node: FuncDefNode, context: Context):
        res: RTResult = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_return_null).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node: CallNode, context: Context):
        res: RTResult = RTResult()
        args = []

        value_to_call: Function = res.register(self.visit(node.node_to_call, context))
        if res.error:
            return res

        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error:
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.error:
            return res

        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)

        return res.success(return_value)
