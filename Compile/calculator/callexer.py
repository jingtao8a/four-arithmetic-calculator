from ..base import lexer
from . import calkit
from ..base import kit


class CalcLexer(lexer.Lexer):
    def __init__(self, text):
        super().__init__(text)
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        '''获取整数'''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            
            if self.current_char.isdigit():
                token = kit.Token(calkit.CalcToken.INTEGER, self.integer(), self.line_number, self.column_number)
                calkit.calc_logger.log(token)
                return token

            try:
                token = kit.Token(calkit.CalcToken(self.current_char), self.current_char, self.line_number, self.column_number)
                self.advance()
                calkit.calc_logger.log(token)
                return token
            except ValueError:
                self.error()
        calkit.calc_logger.log("end")
        return kit.Token(calkit.CalcToken.EOF, None, None, None)
    
