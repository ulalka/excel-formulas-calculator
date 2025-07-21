# Excel-formulas-calculator

[![ci-badge]][ci]
[![pypi-badge]][pypi]
[![py-version-badge]][pypi]

Excel-formulas-calculator (EFC) is a high-level Py23 library that allows you to calculate Excel formulas on any OS.

## Openpyxl interface
```python
from openpyxl import load_workbook
from efc.interfaces.iopenpyxl import OpenpyxlInterface

wb = load_workbook('test.xlsx')
interface = OpenpyxlInterface(wb=wb, use_cache=True)

# e.g. A1 stores formula '=1 + 2', then result = 3
result = interface.calc_cell('A1', 'Worksheet1')

# EFC does not change the source document
print(wb['Worksheet1']['A1'].value)  # prints '=1 + 2'

# If you need to replace a formula in a workbook with a value, 
# you need to do this
wb['Worksheet1']['A1'].value = interface.calc_cell('A1', 'Worksheet1')
print(wb['Worksheet1']['A1'].value)  # prints '3'

# The EFC does not track changes to values in the workbook. 
# If the use_cache=True option is used, the calculated formulas 
# are not recalculated again when they are accessed.
# e.g. A2 = 2, A3 = 1, A4 = A2 + A3
print(interface.calc_cell('A4', 'Worksheet1'))  # prints '3'
wb['Worksheet1']['A2'].value = 1234
print(interface.calc_cell('A4', 'Worksheet1'))  # prints '3'

# If you have made changes to the workbook, then you need to reset 
# the cache to get up-to-date results
interface.clear_cache()
print(interface.calc_cell('A4', 'Worksheet1'))  # prints '1235'

# You can disable caching of results, 
# but then when you run a large number of related formulas, 
# the calculation speed will decrease significantly
```


## Custom interface
1. Inherit from efc.interface.BaseExcelInterface in your excel file class and implement abstract methods. This class will be used to get data from excel file using any library you want.
2. Use calc_cell to calculate cell's formula.

### Functionality

* Arithmetic: ``-, +, *, /, ^, ()``
* Comparison: ``<>, >, >=, <, <=, =``
* String concatenation: ``&``
* Functions: `ABS, AND, AVERAGE, AVERAGEIFS, COLUMN, CONCATENATE, COUNT, COUNTA, COUNTIF, COUNTIFS, COUNTBLANK, 
  FLOOR, IF, IFS, IFERROR, INDEX, ISBLANK, ISERROR, HLOOKUP, LARGE, LEN, LEFT, LOWER, MATCH, MAX, MID, MIN, MOD, NOT,
  OFFSET, OR, RIGHT, ROUND, ROUNDDOWN, ROW, SEARCH, SMALL, SUBSTITUTE, SUM, SUMIF, SUMIFS, SUMPRODUCT, TRIM, VLOOKUP, YEARFRAC, 
  UNIQUE, UPPER`
* All variations of the spelling of the cell and range addresses (linked docs will be skipped)
* Formula cell offset - this can be useful when calculating shared formulas

[ci-badge]: https://github.com/ulalka/excel-formulas-calculator/actions/workflows/python-package.yml/badge.svg?branch=master
[ci]: https://github.com/ulalka/excel-formulas-calculator/actions/workflows/python-package.yml
[pypi-badge]: https://img.shields.io/pypi/v/excel-formulas-calculator
[pypi]: https://pypi.org/project/excel-formulas-calculator/
[py-version-badge]: https://img.shields.io/pypi/pyversions/excel-formulas-calculator
