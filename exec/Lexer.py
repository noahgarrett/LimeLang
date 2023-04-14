from resources import Token, TokenTypes, Position
from errors import IllegalCharError, Error, ExpectedCharError
import string

DIGITS: str = "0123456789"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

KEYWORDS: list[str] = [
    "var",
    "and",
    "or",
    "not",
    "if",
    "then",
    "elif",
    "else",
    "for",
    "to",
    "step",
    "foreach",
    "in",
    "while",
    "fun",
    "end",
    "return",
    "continue",
    "break",
    "from",
    "import"
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

    def reverse(self, amount=1):
        self.pos.reverse(amount)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self) -> tuple[list[Token], Error | None]:
        tokens: list[Token] = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == "#":
                self.skip_comment()
            elif self.current_char in '\n':
                tokens.append(Token(TokenTypes.TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                token, error = self.make_string()
                if error:
                    return [], error
                tokens.append(token)
            elif self.current_char == "+":
                tokens.append(Token(TokenTypes.TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(self.make_minus_or_arrow())
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
            elif self.current_char == "[":
                tokens.append(Token(TokenTypes.TT_LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "]":
                tokens.append(Token(TokenTypes.TT_RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "{":
                tokens.append(Token(TokenTypes.TT_LBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "}":
                tokens.append(Token(TokenTypes.TT_RBRACE, pos_start=self.pos))
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
            elif self.current_char == ",":
                tokens.append(Token(TokenTypes.TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == ":":
                tokens.append(Token(TokenTypes.TT_COLON, pos_start=self.pos))
                self.advance()
            elif self.current_char == ";":
                tokens.append(Token(TokenTypes.TT_SEMI, pos_start=self.pos))
                self.advance()
            # elif self.current_char == ".":
            #     tokens.append(Token(TokenTypes.TT_DOT, pos_start=self.pos))
            #     self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                print(f"Character = '{char}'")
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

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        is_multi_line = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        advance_count = 0
        if self.current_char == '"':
            self.advance()
            advance_count += 1
            if self.current_char == '"':
                self.advance()
                advance_count += 1
                is_multi_line = True
            else:
                self.reverse(advance_count)

        if is_multi_line:
            while self.current_char is not None and self.current_char != '"':
                string += self.current_char
                self.advance()

            ending_count = 0
            for i in range(3):
                if self.current_char == '"':
                    ending_count += 1
                    self.advance()
            if not ending_count == 3:
                return None, ExpectedCharError(pos_start, self.pos, 'Expected """ closing the multi-string')
        else:
            while self.current_char is not None and (self.current_char != '"' or escape_character):
                if escape_character:
                    string += escape_characters.get(self.current_char, self.current_char)
                else:
                    if self.current_char == '\\':
                        escape_character = True
                    else:
                        string += self.current_char

                self.advance()
                escape_character = False

        self.advance()
        return Token(TokenTypes.TT_STRING if not is_multi_line else TokenTypes.TT_MULTI_STRING, string, pos_start, self.pos), None

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + "_.":
            id_str += self.current_char
            self.advance()

        tok_type = TokenTypes.TT_KEYWORD if id_str in KEYWORDS else TokenTypes.TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_minus_or_arrow(self):
        tok_type = TokenTypes.TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '>':
            self.advance()
            tok_type = TokenTypes.TT_ARROW

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

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

    def skip_comment(self):
        self.advance()

        while self.current_char != '\n':
            self.advance()

        self.advance()
