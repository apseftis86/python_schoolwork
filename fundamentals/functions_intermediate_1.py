import random
def randInt(min=0, max=100):
    if max - min < 0:
        return False
    range = max - min
    num = random.random() * range +  min
    return round(num)
print(randInt()) 		    # should print a random integer between 0 to 100
print(randInt(max=50)) 	    # should print a random integer between 0 to 50
print(randInt(min=50)) 	    # should print a random integer between 50 to 100
print(randInt(min=50, max=500))    # should print a random integer between 50 and 500
print(randInt(min=100, max=5)) #should return false
print(randInt(min=10, max=-19)) #should return false
print(randInt(min=-10, max=19)) #should print a random integer between -10 and 19
