from resources import Token, TokenTypes, Position
from resources import IllegalCharError, Error, ExpectedCharError
import string

DIGITS: str = "0123456789"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

KEYWORDS: list[str] = [
    "var",
    "and",
    "or",
    "not"
]


class Lexer:
    def __init__(self, filename: str, text: str):
        self.filename = filename
        self.text: str = text
        self.pos: Position = Position(-1, 0, 0, filename, text)
        self.current_char: str | None = None

        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self) -> tuple[list[Token], Error | None]:
        tokens: list[Token] = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == "+":
                tokens.append(Token(TokenTypes.TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TokenTypes.TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TokenTypes.TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TokenTypes.TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(TokenTypes.TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TokenTypes.TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TokenTypes.TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == "!":
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)
            elif self.current_char == "=":
                tokens.append(self.make_equals())
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")

        tokens.append(Token(TokenTypes.TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self) -> Token:
        num_str: str = ""
        dot_count: int = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break

                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char

            self.advance()

        if dot_count == 0:
            return Token(TokenTypes.TT_INT, int(num_str), pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TokenTypes.TT_FLOAT, float(num_str), pos_start=pos_start, pos_end=self.pos)

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + "_":
            id_str += self.current_char
            self.advance()

        tok_type = TokenTypes.TT_KEYWORD if id_str in KEYWORDS else TokenTypes.TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TokenTypes.TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals(self):
        token_type = TokenTypes.TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = TokenTypes.TT_EE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        token_type = TokenTypes.TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = TokenTypes.TT_LTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        token_type = TokenTypes.TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = TokenTypes.TT_GTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)
