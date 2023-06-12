import sys

sys.path.append('./tester')
sys.path.append('./sort')

from Tester import Tester
from SortingTestingAdapter import SortingTestingAdapter
from Sort import Sort

reportHeader = """
    ОТЧЁТ О ТЕСТИРОВАНИИ {entityName}
    Директория тестовых данных: 
    {dirpath}

    Тип массива: {comment}
"""

reportItem = """

    {iterationName} - N {num} - {valid} - {seconds} сек - сравнений {cmp} - присваиваний {asg}
"""

reportTableItem = """

    {valid} : {num} | {seconds} | {cmp} | {asg}
"""

reportTrueDetails = """
    ----
"""

reportFalseDetails = """
    ----
    Длина массива: {input}

    Отсортированн неверно
    ----
"""
    # - ожидаемый порядок: {expected}
    # - полученный порядок: {computed}

instance = Sort()

instance.setRandom(10)
print(instance)
# instance.BubbleSort()
# instance.InsertionSort()
instance.ShellSort()
print('->', instance)
print('N:', instance.N, 'cmp:', instance.cmp, 'asg:', instance.asg)

# tester0 = Tester(SortingTestingAdapter(instance, instance.BubbleSort, maxLength = 1000))

# # To table:
# #tester0.setupReportStrings(reportHeader = reportHeader, reportItem = reportTableItem, reportTrueDetails = '', reportFalseDetails = reportFalseDetails)

# tester0.setupReportStrings(reportHeader = reportHeader, reportItem = reportItem, reportTrueDetails = reportTrueDetails, reportFalseDetails = reportFalseDetails)

# tester0.testdir('./sorting-tests/0.random', './report/0.random.report.bubble.01.txt', comment='random', printResult = False)

