import enum
import logging

class Logger(object):

    def __init__(self) -> None:
        # 创建一个名为 "my_logger" 的 Logger 对象
        self.logger = logging.getLogger("CompileCore logger")
        self.logger.setLevel(logging.INFO)

        # 创建一个将日志记录到终端的 StreamHandler 对象
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 添加处理器到 Logger 对象
        self.logger.addHandler(console_handler)

    def debug(self):
        self.logger.setLevel(logging.DEBUG)

    def log(self, info):
        self.logger.debug(info)


class TokenType(enum.Enum):

    @classmethod
    def info(cls):
        #显示所有的token类型
        max_length = 0
        for member in cls:
            max_length = max(max_length, len(member.name))
        for member in cls:
            print(f'{member.name:<{max_length}}  {member.value}')

class Token:
    def __init__(self, type, value, line_number, column_number):
        self.type = type
        self.value = value
        self.line_number = line_number
        self.column_number = column_number

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)}, position={self.line_number}:{self.column_number})'
    
    def __repr__(self):
        return self.__str__()

class ErrorCode(TokenType):
    pass

class Error(Exception):
    def __init__(self, error_code=None, message=None):
        self.error_code = error_code
        self.message = f'{self.__class__.__name__}: {message}'

class LexerError(Error):
    
    def __init__(self, error_code=None, message=None):
        super().__init__(error_code, message)

class ParserError(Error):
    
    def __init__(self, error_code=None, message=None):
        super().__init__(error_code, message)

class InterpreterError(Error):
    
     def __init__(self, error_code=None, message=None):
        super().__init__(error_code, message)

