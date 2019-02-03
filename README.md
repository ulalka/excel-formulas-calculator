# Quick start
1. Inherit from efc.interface.BaseExcelInterface in your excel file class and implement methods. This class will be used to get data from excel file using any library you want.
2. Import from efc get_calculator and call it to get function with arguments "**formula**, **ws_name**, **source**". This function will be calculate your formulas.
    * basestring **formula** - excel formula
    * basestring **ws_name** - excel worksheet name, where the formula exists
    * BaseExcelInterface **source** - excel document, where the formula exists

# Functionality
  * Arithmetic: ```-, +, *, /, ^, ()```
  * Comparison: ```<>, >, >=, <, <=, =```
  * String concatenation: ```&```
  * Functions: ```ABS, COUNT, COUNTIF, COUNTBLANK, IF, IFERROR, ISBLANK, FLOOR, LEFT, MAX, MIN, MOD, OFFSET, OR, RIGHT, ROUND, ROUNDDOWN, SUM```
  * All variations of the spelling of the cell and range addresses
