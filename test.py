from Compile import analyzer

a = analyzer.LL1Analyzer("./test/g14.txt")
a.get_analysis_table()
a.ll1_construct("(a,a)")

# from Compile import utils

# l = ["+A", "-A"]
# tree = utils.TireTree(l)
# print(tree.find_common_prefixes())

# import re

# s1 = "yuxintao"

# res = re.sub('yu', '', s1)
# print(res)
