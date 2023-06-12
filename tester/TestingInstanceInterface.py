import time

class TestingInstanceInterface:
    def compute(self, *input) -> str:
        print(input, type(input))
        pass

    def validate(self, *input, output:str = '') -> dict:
        starttime = time.time()
        computed = self.compute(*input)
        secondsPassed = time.time() - starttime

        return ({ 
            "valid": computed == output, 
            "computed": computed, 
            "expected": output, 
            "seconds": secondsPassed,
            "input": list(input)
        })

    def getEntityName(self) -> str:
        pass

def getNumDigits(a:float) -> int:
        b = abs(a)
        if b < 1: b += 1
        
        strings = str(b).split('.')
        floatDigitsStr = ''
        if len(strings) > 1:
            floatDigitsStr = strings[1]

        return len(floatDigitsStr)

def compareFloat(computed:float, output:str, deviation = None) -> bool:
    outputFloat = float(output)

    digits = getNumDigits(outputFloat)

    computedRound = round(computed, digits)

    useDeviation = deviation

    if useDeviation == None:
        useDeviation = float('0.' + ('0' * (digits - 1)) + '2')

    return abs(outputFloat - computedRound) < useDeviation


