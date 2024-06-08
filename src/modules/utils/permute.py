# License GPLv3 by balestek https://github.com/balestek
from itertools import permutations


class Permute:
    def __init__(self, elements: list):
        self.name = [element.lower() for element in elements]
        self.separators = ["", "_", "-", "."]

    def gather(self, way: str = "strict" or "all") -> list:
        names = self.name
        names = [name for name in names if name]
        if len(names) == 1:
            return names
        permutations_list = []
        for i in range(1, len(names) + 1):
            for subset in permutations(names, i):
                if i == 1:
                    if way == "all":
                        permutations_list.append(subset[0])
                        permutations_list.append("_" + subset[0])
                        permutations_list.append(subset[0] + "_")
                    pass
                else:
                    for separator in self.separators:
                        perm = separator.join(subset)
                        permutations_list.append(perm)
                        if separator == "":
                            permutations_list.append("_" + perm)
                            permutations_list.append(perm + "_")
        return permutations_list
