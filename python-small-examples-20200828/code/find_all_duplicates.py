from collections import Counter


def find_all_duplicates(lst):
    c = Counter(lst)
    return list(filter(lambda k: c[k] > 1, c))


print(find_all_duplicates([1, 2, 2, 3, 3, 3]))  # [2,3]
