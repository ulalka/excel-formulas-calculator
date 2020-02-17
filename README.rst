Quick start
~~~~~~~~~~~~~
#. Inherit from efc.interface.BaseExcelInterface in your excel file class and implement methods. This class will be used to get data from excel file using any library you want.
#. Import from efc get_calculator and call it to get function with arguments "**formula**, **ws_name**, **source**". This function will be calculate your formulas.

Functionality
~~~~~~~~~~~~~
* Arithmetic: ``-, +, *, /, ^, ()``
* Comparison: ``<>, >, >=, <, <=, =``
* String concatenation: ``&``
* Functions: ``ABS, AND, AVERAGE, AVERAGEIFS, CONCATENATE, COUNT, COUNTA, COUNTIF, COUNTIFS, COUNTBLANK, IF, IFERROR, INDEX, ISBLANK, FLOOR, LARGE, LEFT, MAX, MATCH, MID, MIN, MOD, OFFSET, OR, SMALL, SUBSTITUTE, RIGHT, ROUND, ROUNDDOWN, SUM, SUMIF, SUMIFS, VLOOKUP``
* All variations of the spelling of the cell and range addresses (linked docs will be skipped)
* Formula cell offset - this can be useful when calculating shared formulas
