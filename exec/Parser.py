from resources import Token, TokenTypes
from resources import NumberNode, BinOpNode, UnaryOpNode, VarAccessNode, VarAssignNode, IfNode, ForNode, WhileNode
from resources import FuncDefNode, CallNode, StringNode, ListNode
from results import ParseResult
from errors import InvalidSyntaxError


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.token_index = -1

        self.advance()

    def advance(self):
        self.token_index += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.token_index -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if 0 <= self.token_index < len(self.tokens):
            self.current_tok = self.tokens[self.token_index]

    #########################

    def parse(self):
        result = self.statements()
        if not result.error and self.current_tok.type != TokenTypes.TT_EOF:
            return result.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', or '/'"
            ))

        return result

    def func_def(self):
        res: ParseResult = ParseResult()

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, 'fun'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'fun'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenTypes.TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TokenTypes.TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TokenTypes.TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier '('"
                ))

        res.register_advancement()
        self.advance()

        arg_name_toks = []
        if self.current_tok.type == TokenTypes.TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TokenTypes.TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TokenTypes.TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TokenTypes.TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_tok.type != TokenTypes.TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenTypes.TT_ARROW:
            res.register_advancement()
            self.advance()

            node_to_return = res.register(self.expression())
            if res.error:
                return res

            return res.success(FuncDefNode(var_name_tok, arg_name_toks, node_to_return, False))

        if self.current_tok.type != TokenTypes.TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '->' or 'NEWLINE'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, 'end'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'end'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok, arg_name_toks, body, True
        ))

    def for_expr(self):
        res: ParseResult = ParseResult()

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, 'for'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'for'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenTypes.TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected identifier"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TokenTypes.TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '='"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expression())
        if res.error:
            return res

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, "to"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'to'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expression())
        if res.error:
            return res

        if self.current_tok.matches(TokenTypes.TT_KEYWORD, 'step'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expression())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenTypes.TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_tok.matches(TokenTypes.TT_KEYWORD, "end"):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.expression())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def while_expr(self):
        res: ParseResult = ParseResult()

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, 'while'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'while'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error:
            return res

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenTypes.TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_tok.matches(TokenTypes.TT_KEYWORD, "end"):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'end'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.expression())
        if res.error:
            return res

        return res.success(WhileNode(condition, body, False))

    def if_expr(self):
        res: ParseResult = ParseResult()
        all_cases = res.register(self.if_expr_cases('if'))
        if res.error:
            return res

        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases('elif')

    def if_expr_c(self):
        res: ParseResult = ParseResult()
        else_case = None

        if self.current_tok.matches(TokenTypes.TT_KEYWORD, 'else'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TokenTypes.TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                else_case = (statements, True)

                if self.current_tok.matches(TokenTypes.TT_KEYWORD, 'end'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected 'end'"
                    ))
            else:
                expr = res.register(self.expression())
                if res.error:
                    return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        res: ParseResult = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TokenTypes.TT_KEYWORD, 'elif'):
            all_cases = res.register(self.if_expr_b())
            if res.error:
                return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error:
                return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res: ParseResult = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error:
            return res

        if not self.current_tok.matches(TokenTypes.TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))

        res.register_advancement()
        self.advance()

        if not self.current_tok.type == TokenTypes.TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, statements, True))

            if self.current_tok.matches(TokenTypes.TT_KEYWORD, 'end'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error:
                    return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.expression())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error:
                return res

            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def list_expr(self):
        res: ParseResult = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TokenTypes.TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TokenTypes.TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expression()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']', 'var', 'if', 'for', 'while', 'fun', int, float, identifier, 'not', '+', '-', '[' "
                    "or '('"
                ))

            while self.current_tok.type == TokenTypes.TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expression()))
                if res.error:
                    return res

            if self.current_tok.type != TokenTypes.TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ']'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(
            element_nodes, pos_start, self.current_tok.pos_end.copy()
        ))

    def atom(self):
        res: ParseResult = ParseResult()
        token = self.current_tok

        if token.type in (TokenTypes.TT_INT, TokenTypes.TT_FLOAT):
            """atom    : INT|FLOAT"""
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))
        elif token.type == TokenTypes.TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(token))
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
        elif token.type == TokenTypes.TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)
        elif token.matches(TokenTypes.TT_KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)
        elif token.matches(TokenTypes.TT_KEYWORD, "for"):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)
        elif token.matches(TokenTypes.TT_KEYWORD, "while"):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)
        elif token.matches(TokenTypes.TT_KEYWORD, "fun"):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected int, float, identifier, '[', '+', '-', 'if', 'for', 'while', 'fun' or '('"
        ))

    def call(self):
        res: ParseResult = ParseResult()

        atom = res.register(self.atom())
        if res.error:
            return res

        if self.current_tok.type == TokenTypes.TT_LPAREN:
            res.register_advancement()
            self.advance()

            arg_nodes = []
            if self.current_tok.type == TokenTypes.TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expression()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', 'var', 'if', 'for', 'while', 'fun', int, float, identifier, 'not', '+', '-', "
                        "or '('"
                    ))

                while self.current_tok.type == TokenTypes.TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expression()))
                    if res.error:
                        return res

                if self.current_tok.type != TokenTypes.TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()

            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def power(self):
        """power   : atom (POW factor)*"""
        return self.binary_operation(self.call, (TokenTypes.TT_POW,), self.factor)

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

    def arith_expr(self):
        return self.binary_operation(self.term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS))

    def comp_expr(self):
        res: ParseResult = ParseResult()

        if self.current_tok.matches(TokenTypes.TT_KEYWORD, "not"):
            operation_token = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(operation_token, node))

        node = res.register(self.binary_operation(self.arith_expr, (
            TokenTypes.TT_EE, TokenTypes.TT_NE, TokenTypes.TT_LT, TokenTypes.TT_GT, TokenTypes.TT_LTE,
            TokenTypes.TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected int, float, identifier, 'not', '+', '-', '[ or '(' "
            ))

        return res.success(node)

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

        node = res.register(
            self.binary_operation(self.comp_expr, ((TokenTypes.TT_KEYWORD, "and"), (TokenTypes.TT_KEYWORD, "or"))))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'var', 'if', 'for', 'while', 'fun', int, float, identifier, 'not', '+', '-', '[', or '('"
            ))

        return res.success(node)

    def statements(self):
        res: ParseResult = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TokenTypes.TT_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.expression())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True
        while True:
            newline_count = 0
            while self.current_tok.type == TokenTypes.TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1

            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break

            statement = res.try_register(self.expression())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue

            statements.append(statement)

        return res.success(ListNode(
            statements, pos_start, self.current_tok.pos_end.copy()
        ))

    #########################

    def binary_operation(self, func_a, ops: tuple, func_b=None):
        if func_b is None:
            func_b = func_a

        res: ParseResult = ParseResult()
        left_node = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            operator_token = self.current_tok
            res.register_advancement()
            self.advance()
            right_node = res.register(func_b())
            if res.error:
                return res
            left_node = BinOpNode(left_node, operator_token, right_node)

        return res.success(left_node)
