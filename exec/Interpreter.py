from resources import NumberNode, BinOpNode, UnaryOpNode
from resources import Number
from resources import TokenTypes
from resources import RTResult
from resources import Context


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

    def visit_BinOpNode(self, node: BinOpNode, context: Context) -> RTResult:
        res: RTResult = RTResult()
        left: Number = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right: Number = res.register(self.visit(node.right_node, context))
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

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
