def insertion_sort(some_list):
    for x in range(1, len(some_list)):
        count = x
        while count >= 1:
            if some_list[count] < some_list[count-1]:
                some_list[count-1], some_list[count] =  some_list[count],  some_list[count-1]
                count -= 1
            else: 
                break
    return some_list
print(insertion_sort([6, 5, 4, 1, 8, 7, 2 , 3]))
