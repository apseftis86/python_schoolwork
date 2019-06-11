# basic
for x in range(0, 151):
    print(x);

# multiples of 5
count = 5
while count <= 1000:
    print(count)
    count +=5

# counting dojo way
for x in range(1, 101):
    if x % 5 == 0:
        if x % 10 == 0:
            print('coding dojo')
        else: 
            print('coding')
    else:
        print(x)  


# whoa that suckers huge
sum = 0
for x in range(1, 500000, 2):
    sum = sum + x
print(sum)

# countdown by fours
for x in range(2018, 0, -4):
    print(x)

# flexible counters
lowNum = 2
highNum = 9
mult = 3
while lowNum <= highNum:
    if lowNum % mult == 0:
        print(lowNum)
        lowNum += 1
    else:
        lowNum += 1

