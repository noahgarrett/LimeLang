from resources import Token, TokenTypes
from resources import NumberNode, BinOpNode, UnaryOpNode
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

    def factor(self):
        res: ParseResult = ParseResult()
        token = self.current_tok

        if token.type in (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS):
            """factor  : (PLUS|MINUS) factor"""
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))
        elif token.type in (TokenTypes.TT_INT, TokenTypes.TT_FLOAT):
            """factor  : INT|FLOAT"""
            res.register(self.advance())
            return res.success(NumberNode(token))
        elif token.type == TokenTypes.TT_LPAREN:
            """factor  : LPAREN expr RPAREN"""
            res.register(self.advance())
            expression = res.register(self.expression())
            if res.error:
                return res
            if self.current_tok.type == TokenTypes.TT_RPAREN:
                res.register(self.advance())
                return res.success(expression)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end, "Expected int or float"
        ))

    def term(self):
        return self.binary_operation(self.factor, (TokenTypes.TT_MUL, TokenTypes.TT_DIV))

    def expression(self):
        return self.binary_operation(self.term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS))

    #########################

    def binary_operation(self, func, ops: tuple):
        res: ParseResult = ParseResult()
        left_node = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            operator_token = self.current_tok
            res.register(self.advance())
            right_node = res.register(func())
            if res.error:
                return res
            left_node = BinOpNode(left_node, operator_token, right_node)

        return res.success(left_node)
