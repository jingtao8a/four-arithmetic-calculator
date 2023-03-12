from ..base import interpreter
from . import calkit
from . import callexer
from . import calparser

class CalcInterpreter(interpreter.Interpreter):
    def __init__(self, parser):
        super().__init__(parser)

    def visit_BinOp(self, node):
        if node.op.type == calkit.CalcToken.PLUS:
            return self.visit(node.left_node) + self.visit(node.right_node)
        elif node.op.type == calkit.CalcToken.MINUS:
            return self.visit(node.left_node) - self.visit(node.right_node)
        elif node.op.type == calkit.CalcToken.MUL:
            return self.visit(node.left_node) * self.visit(node.right_node)
        elif node.op.type == calkit.CalcToken.DIV:
            divisor = self.visit(node.right_node)
            if divisor == 0:
                self.error(calkit.CalcError.DIVISION_BY_ZERO, divisor)
            return self.visit(node.left_node) // divisor
    
    def visit_Num(self, node):
        return node.token.value
    
    def visit_UnaryOp(self, node):
        if node.op.type == calkit.CalcToken.MINUS:
            return -self.visit(node.right_node)
        elif node.op.type == calkit.CalcToken.PLUS:
            return +self.visit(node.right_node)
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
    
def calculator():
    
    while True:
        text = input('calc> ')
        try:
            lexer = callexer.CalcLexer(text)
            parser = calparser.CalcParser(lexer)
            interpreter = CalcInterpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e.message)