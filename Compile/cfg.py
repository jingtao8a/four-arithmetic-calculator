from . import utils
import re
class CFG:
    def __init__(self, file_path:str):
        self.epsilon = 'ε'
        self.begin_symbol = None
        self.productions = dict()
        self.file_path = file_path
    
    def get_productions_from_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            file_content = f.read().split('\n')
        if len(file_content) == 0:
            raise ValueError("file is empty")
        
        for line in file_content:
            production = line.split('->')
            if len(production) != 2:
                raise ValueError(f"production does not match the standard : {production}")
            
            production_head = production[0].strip()
            if len(production_head) != 1:
                raise ValueError(f"production_head must be one character : {production_head}")

            if self.begin_symbol is None:
                self.begin_symbol = production_head
            
            if self.productions.get(production_head) is None:
                self.productions[production_head] = []
            
            production_bodys = production[1].split('|')
            for production_body in production_bodys:
                if production_body in self.productions[production_head]:
                    raise ValueError(f"production {production_body} repeat")
                self.productions[production_head].append(production_body.strip())

    def print_productions(self):
        print("productions:")
        for production_head, production_bodys in self.productions.items():
            for production_body in production_bodys:
                print(f"{production_head} -> {production_body}")

class LL1CFG(CFG):
    def __init__(self, file_path:str):
        super().__init__(file_path)
        self.non_terminal_symbols = set()
        self.terminal_symbols = set()
        self.first_set = None 
        self.follow_set = None
        self.select_set = None

    def deal_with_productions(self):
        self.get_productions_from_file()
        self.non_terminal_symbols = set(self.productions.keys())
        for production_bodys in self.productions.values():
            for production_body in production_bodys:
                for char in production_body:
                    if char not in self.non_terminal_symbols:
                        self.terminal_symbols.add(char)
        
        self.__eliminate_indirect_left_recursion()
        self.__eliminate_direct_left_recursion()
        self.__eliminate_left_public_factor()

    def info(self):
        print("non terminal symbols:")
        for i in self.non_terminal_symbols:
            print(i)
        
        print("terminal symbols:")
        for i in self.terminal_symbols:
            print(i)


    def __eliminate_indirect_left_recursion(self):
        sequence = [ele for ele in reversed(list(self.productions.keys()))]
        length = len(sequence)
        for i in range(0, length):
            for j in range(0, i):
                ch = sequence[j]
                production_bodys = self.productions[sequence[i]]
                new_production_bodys = []
                for production_body in production_bodys:
                    if production_body[0] == ch:
                        new_production_bodys = new_production_bodys + self.__contact_list_of_str_and_str(self.productions[sequence[j]], production_body[1:])
                    else:
                        new_production_bodys.append(production_body)
                self.productions[sequence[i]] = new_production_bodys
        
        self.__simplified_productions()    
    
    def __contact_list_of_str_and_str(self, list_of_str: list[str] , suffix: str):
        new_list = []
        for i in list_of_str:
            if self.epsilon in i:
                if len(suffix) != 0:
                    new_list.append(suffix)
                else:
                    new_list.append(self.epsilon)
                continue   
            
            new_list.append(''.join([i, suffix]))
        return new_list
    
    def __dfs(self, sign_dict, symbol):
        if sign_dict[symbol] == True:
            return
        sign_dict[symbol] = True
        production_bodys = self.productions[symbol]
        for production_body in production_bodys:
            for i in production_body:
                if i in self.non_terminal_symbols:
                    self.__dfs(sign_dict, i)

    def __simplified_productions(self):
        sign_dict = dict()
        for i in self.non_terminal_symbols:
            sign_dict[i] = False
        self.__dfs(sign_dict, self.begin_symbol)
        for key, value in sign_dict.items():
            if value == False:
                self.productions.pop(key)
                self.non_terminal_symbols.discard(key)
        
        
    def __eliminate_direct_left_recursion(self):
        sequence = list(self.productions.keys())
        for production_head in sequence:
            production_bodys = self.productions[production_head]
            for production_body in production_bodys:
                if production_body[0] == production_head:
                    #发现直接左递归
                    new_symbol = self.__register_new_symbol()
                    self.terminal_symbols.add(self.epsilon)
                    self.productions[new_symbol] =[self.epsilon]
                    new_production_bodys = []
                    for body in production_bodys:
                        if body[0] == production_head:
                            self.productions[new_symbol].append(self.__contact_str_and_str(body[1:], new_symbol))
                        else:
                            new_production_bodys.append(self.__contact_str_and_str(body, new_symbol))
                    self.productions[production_head] = new_production_bodys
                    break

    def __contact_str_and_str(self, prefix: str, suffix: str):
        if self.epsilon in prefix or self.epsilon in suffix:
            return self.epsilon
        return "".join([prefix, suffix])

    def __register_new_symbol(self):    
        for i in range(ord('A'), ord('Z') + 1):
            new_symbol = chr(i)
            if new_symbol not in self.non_terminal_symbols and \
                new_symbol not in self.terminal_symbols:

                self.non_terminal_symbols.add(new_symbol)
                
                return new_symbol
        
        for i in range(ord('a'), ord('z') + 1):
            new_symbol = chr(i) 
            if new_symbol not in self.non_terminal_symbols and \
                new_symbol not in self.terminal_symbols:

                self.non_terminal_symbols.add(new_symbol)
                return new_symbol
        
        raise ValueError("not have unused character")
    
    def __eliminate_left_public_factor(self):
        sequence = list(self.productions.keys())
        flag = False
        for production_head in sequence:
            production_bodys = self.productions[production_head]
            if len(production_bodys) == 1:
                continue
            
            tree = utils.TireTree(production_bodys)
            common_prefix = tree.find_common_prefixes()
            if common_prefix == []:
                continue
            flag = True
            new_production_bodys = set()
            for prefix in common_prefix:
                ch = self.__register_new_symbol()
                self.productions[ch] = []
                length = len(prefix)
                for production_body in production_bodys:
                    if re.match(prefix, production_body):
                        self.productions[ch].append(production_body[length:] if len(production_body) > length else self.epsilon)
                        new_production_bodys.add(self.__contact_str_and_str(prefix, ch))
                    else:
                        new_production_bodys.add(production_body)
            
            self.productions[production_head] = list(new_production_bodys)

        if flag:
            self.__eliminate_left_public_factor()