from ..base import kit

calc_logger = kit.Logger()


class CalcToken(kit.TokenType):
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    LPAREN = '('
    RPAREN = ')'
    INTEGER = 'INTEGER'
    EOF = 'EOF'

class CalcError(kit.ErrorCode):
    UNEXPECTED_TOKEN     = 'Unexpected token'
    DIVISION_BY_ZERO     = 'Division by zero'