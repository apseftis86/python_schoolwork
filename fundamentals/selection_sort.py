def selection_sort(lst):
    for i in range(len(lst)):
        min = lst[i]
        min_idx = i
        for x in range(i, len(lst)):
            if lst[x] < min:
                min = lst[x]
                min_idx = x
        if lst[i] != min:
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
    return lst
print(selection_sort([5, 4, 3, 9, 8, 7, 6, 2, 0, 1]))
