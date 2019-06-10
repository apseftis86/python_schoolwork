def countdown(num):
    list = []
    while num >= 0:
        list.append(num)
        num -= 1
    return list

print(countdown(5))


def print_return(list):
    print(list[0])
    return list[1]

print(print_return([1, 2]))


def first_plus_length(list):
    return list[0] + len(list)

print(first_plus_length([1, 2, 3, 4, 5]))

def values_greater_than_second(list):
    if len(list) < 2:
        return False
    else:
        mylist = []
        count = 0
        greater_than = list[1]
        for x in range(0, len(list)):
            if list[x] > greater_than:
                count +=1
                mylist.append(list[x])
        print(count)
        return mylist
    

print(values_greater_than_second([5,2,3,2,1,4]))
print(values_greater_than_second([3]))


def length_and_value(size, value):
    list = [];
    for x in range(0, size):
        list.append(value)
    return list
print(length_and_value(4,7))
print(length_and_value(6,2))
