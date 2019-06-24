class MathDojo:
    def __init__(self):
        self.result = 0
    def add(self, num, *nums):
        self.result += num
        for extra_num in nums:
            self.result += extra_num
        return self

    def subtract(self, num, *nums):
        self.result  -= num
        for extra_num in nums:
            self.result -= extra_num
        return self


md = MathDojo()
md2 = MathDojo()
md3 = MathDojo()
x = md.add(2).add(2,5,10).subtract(3,2).result
y = md2.add(9).add(20,5,10).add(38,2).result
z = md3.subtract(-2).subtract(28,5,10).subtract(3,2).result
print(x, y, z)