from abc import ABC, abstractmethod
from enum import Enum

class NodeType(Enum):
    Program = "Program"

    # Statements
    ExpressionStatement = "ExpressionStatement"
    LetStatement = "LetStatement"
    FunctionStatement = "FunctionStatement"
    BlockStatement = "BlockStatement"
    ReturnStatement = "ReturnStatement"
    AssignStatement = "AssignStatement"
    IfStatement = "IfStatement"
    WhileStatement = "WhileStatement"
    BreakStatement = "BreakStatement"
    ContinueStatement = "ContinueStatement"
    ForStatement = "ForStatement"
    ImportStatement = "ImportStatement"

    # Expressions
    InfixExpression = "InfixExpression"
    CallExpression = "CallExpression"
    PrefixExpression = "PrefixExpression"
    PostfixExpression = "PostfixExpression"
    DotExpression = "DotExpression"

    # Literals
    IntegerLiteral = "IntegerLiteral"
    FloatLiteral = "FloatLiteral"
    IdentifierLiteral = "IdentifierLiteral"
    BooleanLiteral = "BooleanLiteral"
    StringLiteral = "StringLiteral"

    # Helper
    FunctionParameter = "FunctionParameter"


class Node(ABC):
    @abstractmethod
    def type(self) -> NodeType:
        """ Returns back the NodeType """
        pass

    @abstractmethod
    def json(self) -> dict:
        """ Returns back the JSON representation of this AST node """
        pass


class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    """ The root node for the AST """
    def __init__(self) -> None:
        self.statements: list[Statement] = []

    def type(self) -> NodeType:
        return NodeType.Program
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [{stmt.type().value: stmt.json()} for stmt in self.statements]
        }
    
# region Helpers
class FunctionParameter(Expression):
    def __init__(self, name: str, value_type: str = None) -> None:
        self.name = name
        self.value_type = value_type

    def type(self) -> NodeType:
        return NodeType.FunctionParameter
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name,
            "value_type": self.value_type
        }
# endregion

# region Statements
class ExpressionStatement(Statement):
    def __init__(self, expr: Expression = None) -> None:
        self.expr: Expression = expr

    def type(self) -> NodeType:
        return NodeType.ExpressionStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "expr": self.expr.json()
        }
    
class LetStatement(Statement):
    def __init__(self, name: Expression = None, value: Expression = None, value_type: str = None) -> None:
        self.name = name
        self.value = value
        self.value_type = value_type

    def type(self) -> NodeType:
        return NodeType.LetStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name.json(),
            "value": self.value.json(),
            "value_type": self.value_type
        }
    
class BlockStatement(Statement):
    def __init__(self, statements: list[Statement] = None) -> None:
        self.statements = statements if statements is not None else []

    def type(self) -> NodeType:
        return NodeType.BlockStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [stmt.json() for stmt in self.statements]
        }
    
class ReturnStatement(Statement):
    def __init__(self, return_value: Expression = None) -> None:
        self.return_value = return_value

    def type(self) -> NodeType:
        return NodeType.ReturnStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "return_value": self.return_value.json()
        }
    
class FunctionStatement(Statement):
    def __init__(self, parameters: list[FunctionParameter] = [], body: BlockStatement = None, name = None, return_type: str = None) -> None:
        self.parameters = parameters
        self.body = body
        self.name = name
        self.return_type = return_type

    def type(self) -> NodeType:
        return NodeType.FunctionStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name.json(),
            "return_type": self.return_type,
            "parameters": [p.json() for p in self.parameters],
            "body": self.body.json()
        }
    
class AssignStatement(Statement):
    def __init__(self, ident: Expression = None, operator: str = None, right_value: Expression = None) -> None:
        self.ident = ident
        self.operator = operator
        self.right_value = right_value

    def type(self) -> NodeType:
        return NodeType.AssignStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "ident": self.ident.json(),
            "operator": self.operator,
            "right_value": self.right_value.json()
        }
    
class IfStatement(Statement):
    def __init__(self, condition: Expression = None, consequence: BlockStatement = None, alternative: BlockStatement = None) -> None:
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def type(self) -> NodeType:
        return NodeType.IfStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "condition": self.condition.json(),
            "consequence": self.consequence.json(),
            "alternative": self.alternative.json() if self.alternative is not None else None
        }
    
class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: BlockStatement = None) -> None:
        self.condition = condition
        self.body = body if body is not None else []

    def type(self) -> NodeType:
        return NodeType.WhileStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "condition": self.condition.json(),
            "body": self.body.json()
        }
    
class BreakStatement(Statement):
    def __init__(self) -> None:
        pass

    def type(self) -> NodeType:
        return NodeType.BreakStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value
        }
    
class ContinueStatement(Statement):
    def __init__(self) -> None:
        pass

    def type(self) -> NodeType:
        return NodeType.ContinueStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value
        }
    
class ForStatement(Statement):
    def __init__(self, var_declaration: LetStatement = None, condition: Expression = None, action: AssignStatement = None, body: BlockStatement = None) -> None:
        self.var_declaration = var_declaration
        self.condition = condition
        self.action = action
        self.body = body

    def type(self) -> NodeType:
        return NodeType.ForStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "var_declaration": self.var_declaration.json(),
            "condition": self.condition.json(),
            "action": self.action.json(),
            "body": self.body.json()
        }
    
class ImportStatement(Statement):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def type(self) -> NodeType:
        return NodeType.ImportStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "file_path": self.file_path
        }
# endregion
    
# region Expressions
class InfixExpression(Expression):
    def __init__(self, left_node: Expression, operator: str, right_node: Expression = None):
        self.left_node: Expression = left_node
        self.operator: str = operator
        self.right_node: Expression = right_node

    def type(self) -> NodeType:
        return NodeType.InfixExpression
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "left_node": self.left_node.json(),
            "operator": self.operator,
            "right_node": self.right_node.json()
        }

class CallExpression(Expression):
    def __init__(self, function: Expression = None, arguments: list[Expression] = None) -> None:
        self.function = function # IdentifierLiteral
        self.arguments = arguments

    def type(self) -> NodeType:
        return NodeType.CallExpression
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "function": self.function.json(),
            "arguments": [arg.json() for arg in self.arguments]
        }
    
class PrefixExpression(Expression):
    def __init__(self, operator: str, right_node: Expression = None) -> None:
        self.operator = operator
        self.right_node = right_node

    def type(self) -> NodeType:
        return NodeType.PrefixExpression
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "operator": self.operator,
            "right_node": self.right_node.json()
        }
    
class PostfixExpression(Expression):
    def __init__(self, left_node: Expression, operator: str) -> None:
        self.left_node = left_node
        self.operator = operator

    def type(self) -> NodeType:
        return NodeType.PostfixExpression
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "left_node": self.left_node.json(),
            "operator": self.operator
        }
    
# class DotExpression(Expression):
#     def __init__(self, left_node: Expression, right_node: Expression) -> None:
#         self.left_node = left_node
#         self.right_node = right_node

#     def type(self) -> NodeType:
#         return NodeType.DotExpression
    
#     def json(self) -> dict:
#         return {
#             "type": self.type().value,
#             "left_node": self.left_node.json(),
#             "right_node": self.right_node.json()
#         }
# endregion

# region Literals
class IntegerLiteral(Expression):
    def __init__(self, value: int = None) -> None:
        self.value: int = value
    
    def type(self) -> NodeType:
        return NodeType.IntegerLiteral
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
    
class FloatLiteral(Expression):
    def __init__(self, value: float = None) -> None:
        self.value: float = value
    
    def type(self) -> NodeType:
        return NodeType.FloatLiteral
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
    
class IdentifierLiteral(Expression):
    def __init__(self, value: str = None) -> None:
        self.value: str = value
    
    def type(self) -> NodeType:
        return NodeType.IdentifierLiteral
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
    
class BooleanLiteral(Expression):
    def __init__(self, value: bool = None) -> None:
        self.value: bool = value
    
    def type(self) -> NodeType:
        return NodeType.BooleanLiteral
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
    
class StringLiteral(Expression):
    def __init__(self, value: str = None) -> None:
        self.value: str = value
    
    def type(self) -> NodeType:
        return NodeType.StringLiteral
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
# endregion

