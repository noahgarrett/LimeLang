from Token import Token, TokenType, lookup_ident
from typing import Any

class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source

        self.position: int = -1
        self.read_position: int = 0
        self.line_no: int = 1

        self.current_char: str | None = None

        self.__read_char()

    def __read_char(self) -> None:
        """ Reads the next char in the source input file """
        if self.read_position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def __peek_char(self) -> str | None:
        """ Peeks to the upcoming char without advancing the lexer position """
        if self.read_position >= len(self.source):
            return None
        
        return self.source[self.read_position]
    
    def __skip_whitespace(self) -> None:
        """ Skips whitespace and other ignored characters """
        while self.current_char in [' ', '\t', '\n', '\r']:
            # Advance the line number if this is a line break
            if self.current_char == '\n':
                self.line_no += 1
            
            self.__read_char()

    def __new_token(self, tt: TokenType, literal: Any) -> Token:
        """ Creates and returns a new token from specified values """
        return Token(type=tt, literal=literal, line_no=self.line_no, position=self.position)
    
    def __is_digit(self, ch: str) -> bool:
        """ Checks if the character is a digit """
        return '0' <= ch and ch <= '9'
    
    def __is_letter(self, ch: str) -> bool:
        return 'a' <= ch and ch <= 'z' or 'A' <= ch and ch <= 'Z' or ch == '_'
    
    def __read_number(self) -> Token:
        """ Reads a number from the input file and returns a Token """
        start_pos: int = self.position
        dot_count: int = 0

        output: str = ""
        while self.__is_digit(self.current_char) or self.current_char == '.':
            if self.current_char == '.':
                dot_count += 1
            
            if dot_count > 1:
                print(f"Too many decimals in number on line {self.line_no}, position {self.position}")
                return self.__new_token(TokenType.ILLEGAL, self.source[start_pos:self.position])
            
            output += self.source[self.position]
            self.__read_char()

            if self.current_char is None:
                break

        if dot_count == 0:
            return self.__new_token(TokenType.INT, int(output))
        else:
            return self.__new_token(TokenType.FLOAT, float(output))
        
    def __read_identifier(self) -> str:
        position = self.position
        while self.current_char is not None and (self.__is_letter(self.current_char) or self.current_char.isalnum()):
            self.__read_char()
        
        return self.source[position:self.position]
    
    def __read_string(self) -> str:
        position: int = self.position + 1
        while True:
            self.__read_char()
            if self.current_char == '"' or self.current_char is None:
                break
        return self.source[position:self.position]
    
    def next_token(self) -> list[Token]:
        """
            Main function for executing the Lexer
        """
        tok: Token = None

        # Skip the whitespace and ignored characters
        self.__skip_whitespace()

        match self.current_char:
            case '+':
                # Handle +=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.PLUS_EQ, ch + self.current_char)
                # Handle ++
                elif self.__peek_char() == '+':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.PLUS_PLUS, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.PLUS, self.current_char)
            case '-':
                # Handle ->
                if self.__peek_char() == '>':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.ARROW, ch + self.current_char)
                # Handle --
                elif self.__peek_char() == '-':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.MINUS_MINUS, ch + self.current_char)
                # Handle -=
                elif self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.MINUS_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.MINUS, self.current_char)
            case '*':
                # Handle *=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.MUL_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.ASTERISK, self.current_char)
            case '/':
                # Handle /=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.DIV_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.SLASH, self.current_char)
            case '^':
                tok = self.__new_token(TokenType.POW, self.current_char)
            case '%':
                tok = self.__new_token(TokenType.MODULUS, self.current_char)
            case '<':
                # Handle <=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.LT_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.LT, self.current_char)
            case '>':
                # Handle >=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.GT_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.GT, self.current_char)
            case '=':
                # Handle ==
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.EQ_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.EQ, self.current_char)
            case '!':
                # Handle !=
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.NOT_EQ, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.BANG, self.current_char)
            case ':':
                tok = self.__new_token(TokenType.COLON, self.current_char)
            case ';':
                tok = self.__new_token(TokenType.SEMICOLON, self.current_char)
            case ',':
                tok = self.__new_token(TokenType.COMMA, self.current_char)
            case '(':
                tok = self.__new_token(TokenType.LPAREN, self.current_char)
            case ')':
                tok = self.__new_token(TokenType.RPAREN, self.current_char)
            case '{':
                tok = self.__new_token(TokenType.LBRACE, self.current_char)
            case '}':
                tok = self.__new_token(TokenType.RBRACE, self.current_char)
            case '"':
                tok = self.__new_token(TokenType.STRING, self.__read_string())
            case None:
                tok = self.__new_token(TokenType.EOF, "")
            case _:
                if self.__is_letter(self.current_char):
                    literal: str = self.__read_identifier()
                    tt: TokenType = lookup_ident(literal)
                    tok = self.__new_token(tt=tt, literal=literal)
                    return tok
                elif self.__is_digit(self.current_char):
                    tok = self.__read_number()
                    return tok
                else:
                    tok = self.__new_token(TokenType.ILLEGAL, self.current_char)

        self.__read_char()
        return tok
