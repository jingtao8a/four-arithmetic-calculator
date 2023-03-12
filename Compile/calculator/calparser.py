from ..base import parser
from . import calkit

'''
递归下降分析
同时构建语义分析树
'''
class AST:
    pass

class Num(AST):
    def __init__(self, token):
        self.token = token

class BinOp(AST):
    def __init__(self, left_node, op, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.op = op

class UnaryOp(AST):
    def __init__(self, op, right_node):
        self.op = op
        self.right_node = right_node

class CalcParser(parser.Paerser):
    def __init__(self, lexer):
        super().__init__(lexer)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(calkit.CalcError.UNEXPECTED_TOKEN, self.current_token)
    '''
    文法:
    大写为非终结符 小写为终结符
    expr -> term | term PLUS term | term MINUS term
    term -> factor | factor MUL factor | factor DIV factor
    factor -> INTEGER | LPAREN expr RPAREN | MINUS factor | PLUS factor


    or

    expr -> term ((PLUS|MINUS) term)* 
    term -> factor ((MUL|DIV) factor)*
    factor -> INTEGER | LPAREN expr RPAREN | MINUS factor | PLUS factor
    '''
    def factor(self):
        if self.current_token.type == calkit.CalcToken.INTEGER:
            token = self.current_token
            self.eat(calkit.CalcToken.INTEGER)
            return Num(token)
        elif self.current_token.type == calkit.CalcToken.LPAREN:
            self.eat(calkit.CalcToken.LPAREN)
            node = self.expr()
            self.eat(calkit.CalcToken.RPAREN)
            return node
        elif self.current_token.type == calkit.CalcToken.MINUS:
            token = self.current_token
            self.eat(calkit.CalcToken.MINUS)
            return UnaryOp(token, self.factor())
        elif self.current_token.type == calkit.CalcToken.PLUS:
            token = self.current_token
            self.eat(calkit.CalcToken.PLUS)
            return UnaryOp(token, self.factor())
        else:
            self.error(calkit.CalcError.UNEXPECTED_TOKEN)

    def term(self):
        node = self.factor()
        while self.current_token.type in (calkit.CalcToken.MUL, calkit.CalcToken.DIV):
            token = self.current_token
            if token.type == calkit.CalcToken.MUL:
                calkit.calc_logger.log("eat mul in term")
                self.eat(calkit.CalcToken.MUL)
            else:
                calkit.calc_logger.log("eat div in term")
                self.eat(calkit.CalcToken.DIV)
            node = BinOp(node, token, self.factor())
        
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (calkit.CalcToken.PLUS, calkit.CalcToken.MINUS):
            token = self.current_token
            if token.type == calkit.CalcToken.PLUS:
                calkit.calc_logger.log("eat plus in expr")
                self.eat(calkit.CalcToken.PLUS)
            else:
                calkit.calc_logger.log("eat MINUS in expr")
                self.eat(calkit.CalcToken.MINUS)
            node = BinOp(node, token, self.term())
        return node
        

    def parse(self):
        tree = self.expr()
        if self.current_token.type == calkit.CalcToken.EOF:
            return tree
        else:
            self.error(calkit.CalcError.UNEXPECTED_TOKEN, self.current_token)
