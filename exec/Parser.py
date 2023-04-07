from resources import Token, TokenTypes
from resources import NumberNode, BinOpNode, UnaryOpNode, VarAccessNode, VarAssignNode
from resources import ParseResult
from resources import InvalidSyntaxError


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.token_index = -1

        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_tok = self.tokens[self.token_index]
        return self.current_tok

    #########################

    def parse(self):
        result = self.expression()
        if not result.error and self.current_tok.type != TokenTypes.TT_EOF:
            return result.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', or '/'"
            ))

        return result

    def atom(self):
        res: ParseResult = ParseResult()
        token = self.current_tok

        if token.type in (TokenTypes.TT_INT, TokenTypes.TT_FLOAT):
            """atom    : INT|FLOAT"""
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))
        elif token.type == TokenTypes.TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))
        elif token.type == TokenTypes.TT_LPAREN:
            """atom  : LPAREN expr RPAREN"""
            res.register_advancement()
            self.advance()
            expression = res.register(self.expression())
            if res.error:
                return res
            if self.current_tok.type == TokenTypes.TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expression)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end, "Expected int, float, identifier, '+', '-' or '('"
        ))

    def power(self):
        """power   : atom (POW factor)*"""
        return self.binary_operation(self.atom, (TokenTypes.TT_POW, ), self.factor)

    def factor(self):
        res: ParseResult = ParseResult()
        token = self.current_tok

        if token.type in (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS):
            """factor  : (PLUS|MINUS) factor"""
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def term(self):
        return self.binary_operation(self.factor, (TokenTypes.TT_MUL, TokenTypes.TT_DIV))

    def expression(self):
        res: ParseResult = ParseResult()

        if self.current_tok.matches(TokenTypes.TT_KEYWORD, "var"):
            """expr    : KEYWORD:var IDENTIFIER EQ expr"""
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenTypes.TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TokenTypes.TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.binary_operation(self.term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS)))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'var', int, float, identifier, '+', '-', or '('"
            ))

        return res.success(node)

    #########################

    def binary_operation(self, func_a, ops: tuple, func_b=None):
        if func_b is None:
            func_b = func_a

        res: ParseResult = ParseResult()
        left_node = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in ops:
            operator_token = self.current_tok
            res.register_advancement()
            self.advance()
            right_node = res.register(func_b())
            if res.error:
                return res
            left_node = BinOpNode(left_node, operator_token, right_node)

        return res.success(left_node)
