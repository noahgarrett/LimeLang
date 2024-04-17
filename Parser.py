from Lexer import Lexer
from Token import Token, TokenType
from typing import Callable
from enum import Enum, auto

from AST import Statement, Expression, Program
from AST import ExpressionStatement, LetStatement, FunctionStatement, ReturnStatement, BlockStatement, AssignStatement, IfStatement, WhileStatement, BreakStatement, ContinueStatement, ForStatement, ImportStatement
from AST import InfixExpression, CallExpression, PrefixExpression, PostfixExpression
from AST import IntegerLiteral, FloatLiteral, IdentifierLiteral, BooleanLiteral, StringLiteral
from AST import FunctionParameter

# Precedence Types
class PrecedenceType(Enum):
    P_LOWEST = 0
    P_EQUALS = auto()
    P_LESSGREATER = auto()
    P_SUM = auto()
    P_PRODUCT = auto()
    P_EXPONENT = auto()
    P_PREFIX = auto()
    P_CALL = auto()
    P_INDEX = auto()

# Precedence Mapping
PRECEDENCES: dict[TokenType, int] = {
    TokenType.PLUS: PrecedenceType.P_SUM,
    TokenType.MINUS: PrecedenceType.P_SUM,
    TokenType.SLASH: PrecedenceType.P_PRODUCT,
    TokenType.ASTERISK: PrecedenceType.P_PRODUCT,
    TokenType.MODULUS: PrecedenceType.P_PRODUCT,
    TokenType.POW: PrecedenceType.P_EXPONENT,
    
    # Episode 8 NEW
    TokenType.EQ_EQ: PrecedenceType.P_EQUALS,
    TokenType.NOT_EQ: PrecedenceType.P_EQUALS,
    TokenType.LT: PrecedenceType.P_LESSGREATER,
    TokenType.GT: PrecedenceType.P_LESSGREATER,
    TokenType.LT_EQ: PrecedenceType.P_LESSGREATER,
    TokenType.GT_EQ: PrecedenceType.P_LESSGREATER,

    # Episode 9 NEW
    TokenType.LPAREN: PrecedenceType.P_CALL,

    # Episode 18 NEW
    TokenType.PLUS_PLUS: PrecedenceType.P_INDEX,
    TokenType.MINUS_MINUS: PrecedenceType.P_INDEX,

    # Episode 19 NEW
    # TokenType.DOT: PrecedenceType.P_CALL
}

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer
        
        # Just a list of errors caught during parsing
        self.errors: list[str] = []

        self.current_token: Token = None
        self.peek_token: Token = None

        self.prefix_parse_fns: dict[TokenType, Callable] = {
            TokenType.IDENT: self.__parse_identifier,
            TokenType.INT: self.__parse_int_literal,
            TokenType.FLOAT: self.__parse_float_literal,
            TokenType.LPAREN: self.__parse_grouped_expression,

            # Episode 8 NEW
            TokenType.IF: self.__parse_if_statement,
            TokenType.TRUE: self.__parse_boolean,
            TokenType.FALSE: self.__parse_boolean,

            # Episode 11 NEW
            TokenType.STRING: self.__parse_string_literal,

            # Episode 15 NEW
            TokenType.MINUS: self.__parse_prefix_expression,
            TokenType.BANG: self.__parse_prefix_expression,
        }
        self.infix_parse_fns: dict[TokenType, Callable] = {
            TokenType.PLUS: self.__parse_infix_expression,
            TokenType.MINUS: self.__parse_infix_expression,
            TokenType.SLASH: self.__parse_infix_expression,
            TokenType.ASTERISK: self.__parse_infix_expression,
            TokenType.POW: self.__parse_infix_expression,
            TokenType.MODULUS: self.__parse_infix_expression,

            # Episode 8 NEW
            TokenType.EQ_EQ: self.__parse_infix_expression,
            TokenType.NOT_EQ: self.__parse_infix_expression,
            TokenType.LT: self.__parse_infix_expression,
            TokenType.GT: self.__parse_infix_expression,
            TokenType.LT_EQ: self.__parse_infix_expression,
            TokenType.GT_EQ: self.__parse_infix_expression,

            # Episode 9 NEW
            TokenType.LPAREN: self.__parse_call_expression,

            # Episode 18 NEW
            TokenType.PLUS_PLUS: self.__parse_postfix_expression,
            TokenType.MINUS_MINUS: self.__parse_postfix_expression,

            # Episode 19 NEW
            # TokenType.DOT: self.__parse_dot_expression
        }

        # Populate the current_token and peek_token
        self.__next_token()
        self.__next_token()
    
    # region Parser Helpers
    def __next_token(self) -> None:
        """ Advances the lexer to retrieve the next token """
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def __current_token_is(self, tt: TokenType) -> bool:
        return self.current_token.type == tt

    def __peek_token_is(self, tt: TokenType) -> bool:
        """ Peeks one token ahead and checks the type """
        return self.peek_token.type == tt
    
    def __peek_token_is_assignment(self) -> bool:
        assignment_operators: list[TokenType] = [
            TokenType.EQ,
            TokenType.PLUS_EQ,
            TokenType.MINUS_EQ,
            TokenType.MUL_EQ,
            TokenType.DIV_EQ
        ]
        return self.peek_token.type in assignment_operators
    
    def __expect_peek(self, tt: TokenType) -> bool:
        if self.__peek_token_is(tt):
            self.__next_token()
            return True
        else:
            self.__peek_error(tt)
            return False
    
    def __current_precedence(self) -> PrecedenceType:
        prec: int | None = PRECEDENCES.get(self.current_token.type)
        if prec is None:
            return PrecedenceType.P_LOWEST
        return prec
    
    def __peek_precedence(self) -> PrecedenceType:
        prec: int | None = PRECEDENCES.get(self.peek_token.type)
        if prec is None:
            return PrecedenceType.P_LOWEST
        return prec
    
    def __peek_error(self, tt: TokenType) -> None:
        self.errors.append(f"Expected next token to be {tt}, got {self.peek_token.type} instead.")

    def __no_prefix_parse_fn_error(self, tt: TokenType):
        self.errors.append(f"No Prefix Parse Function for {tt} found")
    # endregion
    
    def parse_program(self) -> None:
        """ Main execution entry to the Parser """
        program: Program = Program()

        while self.current_token.type != TokenType.EOF:
            stmt: Statement = self.__parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            
            self.__next_token()

        return program

    # region Statament Methods
    def __parse_statement(self) -> Statement:
        if self.current_token.type == TokenType.IDENT and self.__peek_token_is_assignment():
            return self.__parse_assignment_statement()

        match self.current_token.type:
            case TokenType.LET:
                return self.__parse_let_statement()
            case TokenType.FN:
                return self.__parse_function_statement()
            case TokenType.RETURN:
                return self.__parse_return_statement()
            case TokenType.WHILE:
                return self.__parse_while_statement()
            case TokenType.BREAK:
                return self.__parse_break_statement()
            case TokenType.CONTINUE:
                return self.__parse_continue_statement()
            case TokenType.FOR:
                return self.__parse_for_statement()
            case TokenType.IMPORT:
                return self.__parse_import_statement()
            case _:
                return self.__parse_expression_statement()
    
    def __parse_expression_statement(self) -> ExpressionStatement:
        expr = self.__parse_expression(PrecedenceType.P_LOWEST)

        if self.__peek_token_is(TokenType.SEMICOLON):
            self.__next_token()

        stmt: ExpressionStatement = ExpressionStatement(expr=expr)

        return stmt
    
    def __parse_let_statement(self) -> LetStatement:
        stmt: LetStatement = LetStatement()

        # let a: int = 10;

        if not self.__expect_peek(TokenType.IDENT):
            return None
        
        stmt.name = IdentifierLiteral(value=self.current_token.literal)

        if not self.__expect_peek(TokenType.COLON):
            return None
        
        if not self.__expect_peek(TokenType.TYPE):
            return None
        
        stmt.value_type = self.current_token.literal

        if not self.__expect_peek(TokenType.EQ):
            return None
        
        self.__next_token()

        stmt.value = self.__parse_expression(PrecedenceType.P_LOWEST)

        while not self.__current_token_is(TokenType.SEMICOLON) and not self.__current_token_is(TokenType.EOF):
            self.__next_token()

        return stmt
    
    def __parse_function_statement(self) -> FunctionStatement:
        stmt: FunctionStatement = FunctionStatement()

        # fn name() -> int { return 10; }

        if not self.__expect_peek(TokenType.IDENT):
            return None
        
        stmt.name = IdentifierLiteral(value=self.current_token.literal)

        if not self.__expect_peek(TokenType.LPAREN):
            return None
        
        stmt.parameters = self.__parse_function_parameters()

        if not self.__expect_peek(TokenType.ARROW):
            return None
        
        self.__next_token()

        stmt.return_type = self.current_token.literal

        if not self.__expect_peek(TokenType.LBRACE):
            return None
        
        stmt.body = self.__parse_block_statement()

        return stmt
    
    def __parse_function_parameters(self) -> list[FunctionParameter]:
        params: list[FunctionParameter] = []

        if self.__peek_token_is(TokenType.RPAREN):
            self.__next_token()
            return params
        
        self.__next_token()

        first_param: FunctionParameter = FunctionParameter(name=self.current_token.literal)

        if not self.__expect_peek(TokenType.COLON):
            return None
        
        self.__next_token()

        first_param.value_type = self.current_token.literal
        params.append(first_param)

        while self.__peek_token_is(TokenType.COMMA):
            self.__next_token()
            self.__next_token()

            param: FunctionParameter = FunctionParameter(name=self.current_token.literal)

            if not self.__expect_peek(TokenType.COLON):
                return None
            
            self.__next_token()

            param.value_type = self.current_token.literal

            params.append(param)

        if not self.__expect_peek(TokenType.RPAREN):
            return None
        
        return params

    def __parse_block_statement(self) -> BlockStatement:
        block_stmt: BlockStatement = BlockStatement()

        self.__next_token()

        while not self.__current_token_is(TokenType.RBRACE) and not self.__current_token_is(TokenType.EOF):
            stmt: Statement = self.__parse_statement()
            if stmt is not None:
                block_stmt.statements.append(stmt)

            self.__next_token()

        return block_stmt

    def __parse_return_statement(self) -> ReturnStatement:
        stmt: ReturnStatement = ReturnStatement()

        self.__next_token()

        stmt.return_value = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.SEMICOLON):
            return None
        
        return stmt
    
    def __parse_assignment_statement(self) -> AssignStatement:
        stmt: AssignStatement = AssignStatement()

        stmt.ident = IdentifierLiteral(value=self.current_token.literal)

        self.__next_token() # skips the 'IDENT'
        
        stmt.operator = self.current_token.literal
        self.__next_token() # skips the operator

        stmt.right_value = self.__parse_expression(PrecedenceType.P_LOWEST)

        self.__next_token()

        return stmt
    
    def __parse_if_statement(self) -> IfStatement:
        condition: Expression = None
        consequence: BlockStatement = None
        alternative: BlockStatement = None

        self.__next_token()

        condition = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.LBRACE):
            return None
        
        consequence = self.__parse_block_statement()

        if self.__peek_token_is(TokenType.ELSE):
            self.__next_token()

            if not self.__expect_peek(TokenType.LBRACE):
                return None
            
            alternative = self.__parse_block_statement()

        return IfStatement(condition=condition, consequence=consequence, alternative=alternative)
    
    def __parse_while_statement(self) -> WhileStatement:
        condition: Expression = None
        body: BlockStatement = None

        self.__next_token()  # Skip WHILE

        condition = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.LBRACE):
            return None
        
        body = self.__parse_block_statement()

        return WhileStatement(condition=condition, body=body)
    
    def __parse_break_statement(self) -> BreakStatement:
        self.__next_token()
        return BreakStatement()
    
    def __parse_continue_statement(self) -> ContinueStatement:
        self.__next_token()
        return ContinueStatement()
    
    def __parse_for_statement(self) -> ForStatement:
        """ for (let i: int = 0; i < 10; i = i + 1) { } """
        stmt: ForStatement = ForStatement()

        if not self.__expect_peek(TokenType.LPAREN):
            return None
        
        if not self.__expect_peek(TokenType.LET):
            return None

        stmt.var_declaration = self.__parse_let_statement()

        self.__next_token()  # Skip ;

        stmt.condition = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.SEMICOLON):
            return None
        
        self.__next_token() # Skip ;

        stmt.action = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.RPAREN):
            return None

        if not self.__expect_peek(TokenType.LBRACE):
            return None
        
        stmt.body = self.__parse_block_statement()

        return stmt
    
    def __parse_import_statement(self) -> ImportStatement:
        if not self.__expect_peek(TokenType.STRING):
            return None
        
        stmt = ImportStatement(file_path=self.current_token.literal)
        
        if not self.__expect_peek(TokenType.SEMICOLON):
            return None
        
        return stmt
    # endregion

    # region Expression Methods
    def __parse_expression(self, precedence: PrecedenceType) -> Expression:
        prefix_fn: Callable | None = self.prefix_parse_fns.get(self.current_token.type)
        if prefix_fn is None:
            self.__no_prefix_parse_fn_error(self.current_token.type)
            return None
        
        left_expr: Expression = prefix_fn()
        while not self.__peek_token_is(TokenType.SEMICOLON) and precedence.value < self.__peek_precedence().value:
            infix_fn: Callable | None = self.infix_parse_fns.get(self.peek_token.type)
            if infix_fn is None:
                return left_expr
            
            self.__next_token()

            left_expr = infix_fn(left_expr)
        
        return left_expr
    
    def __parse_infix_expression(self, left_node: Expression) -> Expression:
        """ Parses and returns a normal InfixExpression """
        infix_expr: InfixExpression = InfixExpression(left_node=left_node, operator=self.current_token.literal)

        precedence = self.__current_precedence()

        self.__next_token()

        infix_expr.right_node = self.__parse_expression(precedence)

        return infix_expr
    
    def __parse_postfix_expression(self, left_node: Expression) -> PostfixExpression:
        return PostfixExpression(left_node=left_node, operator=self.current_token.literal)
    
    # def __parse_dot_expression(self, left_node: Expression) -> DotExpression:
    #     precedence = self.__current_precedence()
    #     self.__next_token()  # Skip `.`

    #     right_node: Expression = self.__parse_expression(precedence)

    #     return DotExpression(left_node=left_node, right_node=right_node)
    
    def __parse_grouped_expression(self) -> Expression:
        self.__next_token()

        expr: Expression = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.RPAREN):
            return None
        
        return expr
    
    def __parse_call_expression(self, function: Expression) -> CallExpression:
        expr: CallExpression = CallExpression(function=function)
        expr.arguments = self.__parse_expression_list(TokenType.RPAREN)

        return expr
    
    def __parse_expression_list(self, end: TokenType) -> list[Expression]:
        e_list: list[Expression] = []

        if self.__peek_token_is(end):
            self.__next_token()
            return e_list
        
        self.__next_token()
        
        e_list.append(self.__parse_expression(PrecedenceType.P_LOWEST))

        while self.__peek_token_is(TokenType.COMMA):
            self.__next_token()
            self.__next_token()

            e_list.append(self.__parse_expression(PrecedenceType.P_LOWEST))

        if not self.__expect_peek(end):
            return None
        
        return e_list
    # endregion

    # region Prefix Methods
    def __parse_identifier(self) -> IdentifierLiteral:
        return IdentifierLiteral(value=self.current_token.literal)

    def __parse_int_literal(self) -> IntegerLiteral:
        """ Parses an IntegerLiteral Node from the current token """
        int_lit: IntegerLiteral = IntegerLiteral()

        try:
            int_lit.value = int(self.current_token.literal)
        except:
            self.errors.append(f"Could not parse `{self.current_token.literal}` as an integer.")
            return None
        
        return int_lit
    
    def __parse_float_literal(self) -> FloatLiteral:
        """ Parses an FloatLiteral Node from the current token """
        float_lit: FloatLiteral = FloatLiteral()

        try:
            float_lit.value = float(self.current_token.literal)
        except:
            self.errors.append(f"Could not parse `{self.current_token.literal}` as an float.")
            return None
        
        return float_lit
    
    def __parse_boolean(self) -> BooleanLiteral:
        return BooleanLiteral(value=self.__current_token_is(TokenType.TRUE))
    
    def __parse_string_literal(self) -> StringLiteral:
        return StringLiteral(value=self.current_token.literal)
    
    def __parse_prefix_expression(self) -> PrefixExpression:
        prefix_expr: PrefixExpression = PrefixExpression(operator=self.current_token.literal)

        self.__next_token()

        prefix_expr.right_node = self.__parse_expression(PrecedenceType.P_PREFIX)

        return prefix_expr
    # endregion
