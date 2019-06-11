# The “Basic 13”
# These are Coding Dojo’s foundation “Basic 13” algorithm challenges. Can you finish these in less than two minutes each?   


# Print 1-255
# Print1To255()
# Print all the integers from 1 to 255.

def Print1To255():
    for x in range(1, 256):
        print(x)
Print1To255()

# Print Ints and Sum 0-255
# PrintIntsAndSum0To255()
# Print integers from 0 to 255, and with each integer print the sum so far. 
def PrintIntsAndSum0To255():
    running_sum = 0
    for x in range(0, 256):
        running_sum += x
        print(x, running_sum)

PrintIntsAndSum0To255()

# Find and Print Max
# PrintMaxOfArray(arr)
# Given an array, find and print its largest element.

def PrintMaxOfArray(arr):
    max = arr[0]
    for x in range(0, len(arr)):
        if arr[x] > max:
            max = arr[x]
    return max
print(PrintMaxOfArray([2, 4, 8, 3]))
# Array with Odds
# ReturnOddsArray1To255()
# Create an array with all the odd integers between 1 and 255 (inclusive).  

def ReturnOddsArray1To255():
    arr = []
    for x in range(1, 256, 2):
        arr.append(x)
    return arr
print(ReturnOddsArray1To255())

# Greater than Y
# ReturnArrayCountGreaterThanY(arr, y)
# Given an array and a value Y, count and print the number of array values greater than Y. 
def ReturnArrayCountGreaterThanY(arr, y):
    count = 0
    for x in range(0, len(arr)):
        if arr[x] > y:
            count += 1
    print(count)

ReturnArrayCountGreaterThanY([1, 2, 3, 4, 5], 2)


# Max, Min, Average
# PrintMaxMinAverageArrayVals(arr)
# Given an array, print the max, min and average values for that array.
def PrintMaxMinAverageArrayVals(arr):
    max = arr[0]
    min = arr[0]
    sum = 0
    for x in range(0, len(arr)):
        sum += arr[x]
        if arr[x] > max:
            max = arr[x]
        elif arr[x] < min:
            min = arr[x]
    print(max, min, sum / len(arr))


PrintMaxMinAverageArrayVals([1, 2, 3, 4])

# Swap String For Array Negative Values
# SwapStringForArrayNegativeVals(arr)
# Given an array of numbers, replace any negative values with the string 'Dojo'.


def SwapStringForArrayNegativeVals(arr):

    for x in range(0, len(arr)):
        if arr[x] < 0:
            arr[x] = 'Dojo'
    return arr


print(SwapStringForArrayNegativeVals([-1, 3, 4, -5]))
# Print Odds 1-255
# PrintOdds1To255()
# Print all odd integers from 1 to 255. 

def PrintOdds1To255():
    for x in range(1, 256, 2):
        print(x)


PrintOdds1To255()
# Iterate and Print Array
# PrintArrayVals(arr)
# Iterate through a given array, printing each value. 

def PrintArrayVals(arr):
    for x in range(0, len(arr)):
        print(arr[x])


PrintArrayVals(['We', 'are', 'printing'])

# Get and Print Average
# PrintAverageOfArray(arr)
# Analyze an array’s values and print the average. 

def printAverageOfArray(arr):
    sum = 0
    for x in range(0, len(arr)):
        sum += arr[x]
    print(sum / len(arr))


printAverageOfArray([1, 2, 3, 4, 5])
# Square the Values
# SquareArrayVals(arr)
# Square each value in a given array, returning that same array with changed values. 

def SquareArrayVals(arr):
    for x in range(0, len(arr)):
        arr[x] = pow(arr[x], 2)
    return arr

print(SquareArrayVals([2, 4, 5]))


# Zero Out Negative Numbers
# ZeroOutArrayNegativeVals(arr)
# Return the given array, after setting any negative values to zero. 

def ZeroOutArrayNegativeVals(arr):

    for x in range(0, len(arr)):
        if arr[x] < 0:
            arr[x] = 0
    return arr


print(ZeroOutArrayNegativeVals([-1, 3, 4, -5]))
# Shift Array Values
# ShiftArrayValsLeft(arr)
# Given an array, move all values forward (to the left) by one index, dropping the first value and leaving a 0 (zero) value at the end of the array.


def ShiftArrayValsLeft(arr):
    for x in range(0, len(arr)-1):
        arr[x] = arr[x+1]
    arr[len(arr)-1] = 0
    return arr


print(ShiftArrayValsLeft([1, 2, 3, 4, 5]))