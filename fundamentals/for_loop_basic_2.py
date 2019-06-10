def biggie_size(list):
    for x in range(0, len(list)):
        if list[x] > 0:
            list[x] = 'big'
    return list

print(biggie_size([-1, 3, 5, -5]))


def count_positives(list):
    count = 0
    for x in range(0, len(list)):
        if list[x] >=1:
            count += 1
    list[int(len(list)) - 1] = count
    return list

print(count_positives([-1,1,1,1]))
print(count_positives([1,6,-4,-2,-7,-2]))


def sum_total(list):
    final_sum = 0
    for x in range(0, len(list)):
        final_sum += list[x]
    return final_sum

print(sum_total([1,2,3,4]))
print(sum_total([6,3,-2]))


def average(list):
    sum = 0
    for x in range(0, len(list)):
        sum += list[x]
    return sum / len(list)
    #for python2.7 needed to add float(len(list))

print(average([1,2,3,4]))

def length(list):
    return len(list)

print(length([37,2,1,-9]))
print(length([]))


def minimum(list):
    if len(list) == 0:
       return False
    else: 
        min = list[0]
        for x in range(0, len(list)):
            if list[x] < min:
                min = list[x]
        return min

print(minimum([37,2,1,-9]))
print(minimum([]))

def maximum(list):
    if len(list) == 0:
       return False
    else: 
        max = list[0]
        for x in range(0, len(list)):
            if list[x] > max:
                max = list[x]
        return max
print(maximum([37,2,1,-9]))
print(maximum([]))


def ultimate_analysis(list):
    sumTotal = 0
    min = list[0]
    max = list[0]
    for x in range(0, len(list)):
        sumTotal += list[x]
        if list[x] > max:
            max = list[x]
        elif list[x] < min:
            min = list[x]
    obj = {'sumTotal': sumTotal, 'average': sumTotal / len(list), 'minimum': min, 'maximum': max, 'length': len(list)}
    return obj

print(ultimate_analysis([37,2,1,-9]))

def reverse_list(list):
    myrange = int(len(list) / 2)
    for x in range(myrange):
        temp = list[x]
        list[x] = list[len(list)-1-x]
        list[len(list)-1-x] = temp
    return list

print(reverse_list([37,2,1,-9]))
