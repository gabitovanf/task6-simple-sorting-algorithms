import sys
import time

sys.path.append('./tester')
sys.path.append('./sort')

from TestingInstanceInterface import TestingInstanceInterface, compareFloat, getNumDigits
from Sort import Sort

class SortingTestingAdapter(TestingInstanceInterface):
    def __init__(self, instance, method, maxLength: int = 1000000):
        self.instance = instance
        self.method = method
        self.maxLength = maxLength

    def compute(self, *input):
        try:
            firstInputVal = input[0]
            firstInputVal = int(firstInputVal)

            if firstInputVal > self.maxLength: return False

            print('Start with', input[0])

            secondInputVal = input[1]
            secondInputVal = list(map(lambda x: int(x), secondInputVal
                .strip()
                .split(' ')))

            # Pass array
            self.instance.setArray(secondInputVal)

            # Sort
            computed = self.method()

            print('End with', computed.N, computed.cmp, computed.asg)
        
            return computed

        except ValueError as e:
            computed = 'Invalid input data'
            print(e)

        except AttributeError as e:
            computed = 'Instance or class passed is invalid: it must contain a method .getNumSorting(inputValue:int)'
            print(e)

        except Exception as e:
            code = e.__class__.__name__
            computed = f"Exception occured: {code} {e}"
            print(e)

        # print('End with', computed)
        
        return computed

    def validate(self, *input, output:str = '') -> dict:
        starttime = time.time()
        computed = self.compute(*input)
        secondsPassed = time.time() - starttime

        cmp = None
        asg = None
        num = None

        input0 = None
        if len(input) > 0: 
            input0 = int(input[0])

        if isinstance(computed, Sort):
            num = computed.N
            cmp = computed.cmp
            asg = computed.asg
            computed = str(computed.A)[1:-1].replace(',', '')

        return ({ 
            "valid": computed == output, 
            "computed": computed, 
            "expected": output, 
            "seconds": secondsPassed,
            "input": input0,
            "num": num,
            "cmp": cmp,
            "asg": asg
        })

    def getEntityName(self) -> str:
        return '{cls}.{method}'.format(cls=self.instance.__class__.__name__, method=self.method.__name__)

        