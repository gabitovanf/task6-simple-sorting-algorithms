import pandas as pd

from export_report.CompileReportsToXlsl import CompileReportsToXlsl

compiler = CompileReportsToXlsl(
    row_and_col_names_mask = ((0, 1), (-1, None)), 
    sheetname_mask = (1, 2),
)

compiler.readReports([
    # 'report/ResultsSingleArray.txt',
    # 'report/ResultsVectorArray.txt',
    # 'report/ResultsFactorArray.txt',
    # 'report/ResultsMatrixArray.txt', 
    # 'report/ResultsListArrayAdapter.txt'
])

compiler.writeDataFramesToXlsx('report-sheets.xlsx')

