from resources import Token


class NumberNode:
    def __init__(self, token: Token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"


class VarAccessNode:
    def __init__(self, var_name_tok: Token):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarAssignNode:
    def __init__(self, var_name_tok: Token, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


class BinOpNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token: Token = operator_token
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.operator_token}, {self.right_node})"


class UnaryOpNode:
    def __init__(self, operator_token, node):
        self.operator_token: Token = operator_token
        self.node = node

        self.pos_start = self.operator_token.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.operator_token}, {self.node})"
