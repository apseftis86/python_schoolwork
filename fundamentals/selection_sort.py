def selection_sort(lst):
    index = 0
    min_ind = 0
    while index < len(lst):
        min = lst[index]
        min_idx = index
        for x in range(index, len(lst)):
            if lst[x] < min:
                min = lst[x]
                min_ind = x
        if lst[index] != min:
            lst[index], lst[min_ind] = lst[min_ind], lst[index]
        index += 1
    return lst 
print(selection_sort([5, 4, 2, 9, 8, 7, 6, 3, 0, 1]))
