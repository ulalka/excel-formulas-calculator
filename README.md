# excel-formula-calculator
Library for the evaluation of excel formulas

# Quick start
1. Inherit from efc.interface.BaseExcelInterface in your excel file class and implement methods. This class will be used to get data from excel files using any library you want.
2. Import from efc get_calculator and call it to get lambda function with arguments "**formula**, **ws_name**, **source**". This function will be calculate your formulas.
    * basestring **formula** - excel formula
    * basestring **ws_name** - excel worksheet, where the formula exists
    * BaseExcelInterface **source** - excel document, where the formula exists
