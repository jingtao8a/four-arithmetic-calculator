from . import kit

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
    
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        # 反射
        visit_method = getattr(self, method_name, self.visit_error)
        return visit_method(node)

    def visit_error(self, node):
        s = f'找不到 visit_{type(node).__name__} 方法, 需要编写 {type(node).__name__} 类的对应visit方法'
        raise kit.InterpreterError(s, type(node).__name__)
    
    def error(self, error_code, node):
        raise kit.InterpreterError(error_code, f'{error_code.value} -> {node}')