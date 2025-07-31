from util.recursors import recursor
tracker=[]

print("-----------------------STARTING-----------------------------")

def check_field(flags,data,fieldName=""): #DONE and TESTED
    """
    Provide any nested mixture of arrays and objects and this will let you know if it contains a certain key, available flags [chain,cs,findone]

    Parameters:
    flags (dict): dict
    data (any): data.
    fieldName (string): key to search for

    Returns: returns the key that is found
    {"verdict":True/False, "data":array of objects containing each key found that match}

    Example:
    >>> FieldCheck({"a":1,"b":2,"c":3}, "a")
    {"verdict":True, "data":[{"a":1}]}
    """
    flags["mode"]="fieldCheck"
    flags["Found"]=False
    # print("=///////////==///////////=",flags)
    res=recursor(flags,True, [], data, fieldName)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def check_value(flags,data, operator, value):  #DONE and TESTED
    """
    Provide any nested mixture of arrays and objects and this will let you know if it contains a certain value, available flags [cs,findOne]

    Parameters:
    data (data structure that contains a dict): data.
    operator (string): operator
    value (string): value to search for

    Returns: returns the value that is found
    {"verdict":True/False, "data":array of objects containing each value found that match}

    Example:
    >>> FieldCheck({"a":1,"b":2,"c":3}, "eq", "myValue")
    {"verdict":True, "data":[{"a":"myValue}]}
    """
    flags["mode"]="valueCheck"
    flags["Found"]=False
    res=recursor(flags,True, [], data, value, operator)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def check_key_value(flags,data, keyword, value=""): #DONE and TESTED
    """
    Provide any nested mixture of arrays and objects and this will let you know if it contains a certain key value pair, flags[chain,cs,findOne]

    Parameters:
    data (data structure that contains a dict): data.
    key (string): key
    value (string): value to search for

    Returns: returns the value that is found
    {"verdict":True/False, "data":array of objects containing each value found that match}

    Example:
    >>> FieldCheck({"a":1,"b":2,"c":3}, "a", "myValue")
    {"verdict":True, "data":[{"a":"myValue}]}
    """
    if type(keyword)==dict:
        flags["mode"]="keyValueCheck"
        flags["Found"]=False
        res=recursor(flags, True, [], data, keyword, value, "obj")
    else:
        flags["mode"]="keyValueCheck"
        flags["Found"]=False
        res=recursor(flags, True, [], data, keyword, value)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

# maybe i need a single field with multi Value check, only dose or, dosnt do and

def check_multi_value(flags,data, condition): #DONE and TESTED
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
    flags["mode"]="multiValueCheck"
    res=recursor(flags,True, [], data, condition)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def check_SE_multi_key_value(flags,data,condition):
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
    flags["mode"]="multiKeyValueCheck"
    res=recursor(flags,True, [], data, condition)
    # print("enddddddddd",res)
    return res
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def change_value(flags,data,key,value): #DONE and TESTED
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

def match_object(data,matcher):
    pass         

def evaluate_object(data,condition,initial=True): #DONE and TESTED
    global tracker
    if initial:
        tracker=[]
    else:
        newTracker=[]
    if condition.get("Op")=="and" or condition.get("Op")=="or":
        for item in condition.get("Value"):
            if item.get("Op")=="and" or item.get("Op")=="or":
                res=EvaluateObject(data,item,False)
                if initial:
                    tracker.append(res)
                    # print("returned",tracker)
                else:
                    newTracker.append(verdict)
            else:
                flags={
                    "chain":False,
                    "se":False,
                    "cs":True,
                    "findOne":False
                }
                res=KeyValueCheck(flags,data,item.get("field"),item.get("Value"))
                verdict=res.get("verdict")
                if initial:
                    tracker.append(verdict)
                else:
                    newTracker.append(verdict)
        if initial:
            if condition.get("Op")=="and":
                if len(tracker)==len(condition.get("Value")) and False not in tracker:
                    return True
                else:
                    return False
            elif condition.get("Op")=="or":
                print(tracker)
                if len(tracker)==len(condition.get("Value")) and True in tracker:
                    return True
                else:
                    return False
        else:
            print(newTracker)
            if condition.get("Op")=="and":
                if len(newTracker)==len(condition.get("Value")) and False not in newTracker:
                    return True
                else:
                    return False
            elif condition.get("Op")=="or":
                if len(newTracker)==len(condition.get("Value")) and True in newTracker:
                    return True
                else:
                    return False

   

