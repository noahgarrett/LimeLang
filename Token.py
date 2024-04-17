from enum import Enum
from typing import Any

class TokenType(Enum):
    # Special Tokens
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"

    # Data Types
    IDENT = "IDENT"
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"

    # Arithmetic Symbols
    PLUS = "PLUS"
    MINUS = "MINUS"
    ASTERISK = "ASTERISK"
    SLASH = "SLASH"
    POW = "POW"
    MODULUS = "MODULUS"

    # Prefix Symbols
    BANG = "BANG"
    
    # Postfix Symbols
    PLUS_PLUS = "PLUS_PLUS"
    MINUS_MINUS = "MINUS_MINUS"

    # Assignment Symbols
    EQ = "EQ"
    PLUS_EQ = "PLUS_EQ"
    MINUS_EQ = "MINUS_EQ"
    MUL_EQ = "MUL_EQ"
    DIV_EQ = "DIV_EQ"

    # Comparison Symbols
    LT = '<'
    GT = '>'
    EQ_EQ = '=='
    NOT_EQ = '!='
    LT_EQ = '<='
    GT_EQ = '>='

    # Symbols
    COLON = "COLON"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    ARROW = "ARROW"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"

    # Keywords
    LET = "LET"
    FN = "FN"
    RETURN = "RETURN"
    IF = "IF"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    WHILE = "WHILE"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    FOR = "FOR"
    IMPORT = "IMPORT"

    # Typing
    TYPE = "TYPE"


class Token:
    def __init__(self, type: TokenType, literal: Any, line_no: int, position: int) -> None:
        self.type = type
        self.literal = literal
        self.line_no = line_no
        self.position = position

    def __str__(self) -> str:
        return f"Token[{self.type} : {self.literal} : Line {self.line_no} : Position {self.position}]"
    
    def __repr__(self) -> str:
        return str(self)
    

KEYWORDS: dict[str, TokenType] = {
    "let": TokenType.LET,
    "fn": TokenType.FN,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "while": TokenType.WHILE,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "for": TokenType.FOR,
    "import": TokenType.IMPORT
}

ALT_KEYWORDS: dict[str, TokenType] = {
    "lit": TokenType.LET,
    "be": TokenType.EQ,
    "rn": TokenType.SEMICOLON,
    "bruh": TokenType.FN,
    "pause": TokenType.RETURN,
    "3--D": TokenType.ARROW,
    "sus": TokenType.IF,
    "imposter": TokenType.ELSE,
    "wee": TokenType.WHILE,
    "yeet": TokenType.BREAK,
    "anothaone": TokenType.CONTINUE,
    "dab": TokenType.FOR,
    "come": TokenType.IMPORT
}

TYPE_KEYWORDS: list[str] = ["int", "float", "bool", "str", "void"]

def lookup_ident(ident: str) -> TokenType:
    tt: TokenType | None = KEYWORDS.get(ident)
    if tt is not None:
        return tt
    
    tt: TokenType | None = ALT_KEYWORDS.get(ident)
    if tt is not None:
        return tt
    
    if ident in TYPE_KEYWORDS:
        return TokenType.TYPE
    
    return TokenType.IDENT
