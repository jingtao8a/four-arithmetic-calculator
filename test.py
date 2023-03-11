from Compile import cfg

a = cfg.LL1CFG(file_path="./test/g6.txt")
a.deal_with_productions()
a.info()
a.print_productions()


# from Compile import utils

# l = ["+A", "-A"]
# tree = utils.TireTree(l)
# print(tree.find_common_prefixes())

# import re

# s1 = "yuxintao"

# res = re.sub('yu', '', s1)
# print(res)