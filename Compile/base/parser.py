from . import kit

class Paerser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, error_code, token):
        raise kit.ParserError(error_code=error_code, message=f'{error_code.value} -> {token}')

    def parse(self):
        raise NotImplementedError