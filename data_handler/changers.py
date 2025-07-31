from .util.recursors import recursor

def change_value(flags={
        "se":False,
        "cs":True,
        "findOne":False,
        "chain":False
    },data="",key="",value=""): #DONE and TESTED
    """
    Provide any nested mixture of arrays and objects and this will let you know if it contains a certain key value pair

    Parameters:
    data (data structure that contains a dict): data.
    condition (string): {"Op":"eq","Value":"this"}

    Returns: returns the value that is found
    {"verdict":True/False, "data":array of objects containing each value found that match}

    Example:
    >>> FieldCheck({"a":1,"b":2,"c":3}, {"Op":"or","Value":[{"Op":"eq","Value":"this"},{"Op":"eq","Value":"that"}]}")
    {"verdict":True, "data":[{"a":"myValue}]}
    """
    flags["mode"]="valueChange"
    res=recursor(flags,True, [], data, key, value)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

# def reformat_data():
#     pass
