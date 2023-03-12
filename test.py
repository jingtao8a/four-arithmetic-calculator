# from Compile import analyzer
# import Compile

# a = Compile.analyzer.LL1Analyzer("./test/g14.txt")
# a.get_analysis_table()
# a.ll1_construct("(a,a,a)")
# print(Compile.cfg.re.match("yu", "yuxintao").group())
# from Compile import utils

# l = ["+A", "-A"]
# tree = utils.TireTree(l)
# print(tree.find_common_prefixes())

# import re

# s1 = "yuxintao"

# res = re.sub('yu', '', s1)
# print(res)
# from Compile.parser import kit

# a = kit.Logger()
# a.debug()
# a.log("hello")

# from Compile.parser import kit

# class me(kit.ErrorCode):
#     a = 1
#     b = 2
#     c = 3

# me.info()

# from Compile.calculator import calinterpreter, calkit

# # calkit.calc_logger.debug()
# calinterpreter.calculator()

# from Compile.base import kit
# print(kit.ErrorCode.UNEXPECTED_TOKEN)


import Compile

Compile.calculator.calinterpreter.calculator()