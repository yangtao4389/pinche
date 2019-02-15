import importlib
def str_to_function(function_string):
    '''
    :param function_string: 比方想引入函数 from common.client import decode_url  那么可以直接传 common.client.decode_url  
    :return: 
    '''
    # function_string = 'mypackage.mymodule.myfunc'
    mod_name, func_name = function_string.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    return func