from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    VAR = auto()
    IDENTIFIER = auto()
    EQUALS = auto()
    NEWLINE = auto()
    LOOP = auto()
    END = auto()
    IF = auto()
    ELSE = auto()
    TRUE = auto()
    FALSE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    FUNCTION = auto()
    PRINT = auto()
    AND = auto()
    OR = auto()
    LEFT_PARENTHESES = auto()
    RIGHT_PARENTHESES = auto()
    JUMPBACK = auto()


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

