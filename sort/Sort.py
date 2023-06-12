import random

class Sort:

    def __init__(self):
        self.A = []
        self.N = 0
        self.cmp = 0    # the number of comparisons
        self.asg = 0    # the number of asignments

    def setRandom(self, num: int):
        a = []

        for i in range(0, num):
            a.append(random.randrange(num))

        self.A = a
        self.N = len(a)
        return self
        

    def setOrdered(self, num: int):
        a = []

        for i in range(0, num):
            a.append(i)

        self.A = a
        self.N = len(a)
        return self


    def setReversed(self, num: int):
        a = []

        for i in range(0, num):
            a.append(num - i)

        self.A = a
        self.N = len(a)
        return self


    def setAlmostOrdered(self, num: int):
        a = []

        for i in range(0, num):
            if i < num * 0.6:
                a.append(i)
            else:
                a.append(random.randrange(num))

        self.A = a
        self.N = len(a)
        return self

    def setArray(self, input: list):
        self.A = input
        self.N = len(input)
        return self

    def __reset(self):
        self.cmp = 0
        self.asg = 0

    
    def BubbleSort(self):
        self.__reset()

        for j in range(self.N - 1, -1, -1):
            for i in range(0, j):
                self.cmp += 1
                if self.A[i] > self.A[i + 1]:
                    self.__swap(i, i + 1)

        return self


    def InsertionSort(self):
        self.__reset()

        for j in range(0, self.N):
            for i in range(j - 1, -1, -1):
                self.cmp += 1
                if self.A[i] <= self.A[i + 1]: 
                    break
                self.__swap(i, i + 1)

        return self


    def ShellSort(self):
        self.__reset()

        gap = self.N // 2

        while gap > 0:
            for i in range(gap, self.N):
                print(gap, i)
                for j in range(i, gap, -gap):
                    if self.A[j - gap] <= self.A[j]:
                        break
                    self.__swap(j - gap, j)

            gap //= 2



    def InsertionSort2(self):
        self.__reset()

        for j in range(0, self.N):
            for i in range(j - 1, self.__searchIndex(self.A[j], 0, j) - 1, -1):
                self.__swap(i, i + 1)

        return self


    def __searchIndex(self, value, start, end):
        i = start
        while self.A[i] < value and i < end + 1 and self.__incrementCmp():
            i += 1

        return i


    def __swap(self, x: int, y: int):
        self.asg += 3

        t = self.A[x]
        self.A[x] = self.A[y]
        self.A[y] = t


    def __incrementCmp(self, delta: int = 1) -> bool:

        self.cmp += delta

        return True

    def __str__(self) -> str:
        return str(self.A) + ' <len {num}>'.format(num=self.N)
