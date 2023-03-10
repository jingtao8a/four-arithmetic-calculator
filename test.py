from Compile import cfg

a = cfg.LL1CFG(file_path="./test/g13.txt")
a.parse()
a.info()
a.print_productions()


# from Compile import utils

# l = ["code", "coder", "coding", "codable", "codec", "codecs", "coded",
#         "codeless", "codependence", "codependency", "codependent",
#         "codependents", "codes", "codesign", "codesigned", "codeveloped",
#         "codeveloper", "codex", "codify", "codiscovered", "codrive"]
# tree = utils.TireTree(l)
# print(tree.find_common_prefixes())

# import re

# s1 = "yuxintao"

# res = re.sub('yu', '', s1)
# print(res)