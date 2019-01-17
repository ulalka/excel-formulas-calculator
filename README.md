# Quick start
1. Inherit from efc.interface.BaseExcelInterface in your excel file class and implement methods. This class will be used to get data from excel file using any library you want.
2. Import from efc get_calculator and call it to get lambda function with arguments "**formula**, **ws_name**, **source**". This function will be calculate your formulas.
    * basestring **formula** - excel formula
    * basestring **ws_name** - excel worksheet, where the formula exists
    * BaseExcelInterface **source** - excel document, where the formula exists

# Functionality
  * Arithmetic: ```-, +, *, /, ^, ()```
  * Comparison: ```<>, >, >=, <, <=, =```
  * String concatenation: ```&```
  * Functions: ```SUM, MOD, IF, IF_ERROR, LEFT, RIGHT, MAX, MIN, ISBLANK```
  * All variations of the spelling of the cell and range addresses
