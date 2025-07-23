from collections import counter

list_dup = [2,5,3,5,2,3,4,2,5,6,7]

def dup_with_cntr(list_dup):
    count = counter(list_dup)
    duplicates = {}

    for i,num in enumerate(list_dup):
        if count[num]>1:
            duplicates.setdefault(num,[]).append(i)
    return duplicates