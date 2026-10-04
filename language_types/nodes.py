from enum import Enum, auto

class NodeTypes(Enum):
    BINOP = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    ASSIGNMENT = auto()
    REASSIGNMENT = auto()
    LOOP = auto()
    IF = auto()
    ELSE = auto()
    ARRAY = auto()
    INDEX = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    FUNCTION = auto()
    FUNCTION_CALL = auto()
    JUMPBACK = auto()

class ASTNode:
    def __init__(self, node_type, value, left, right):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right