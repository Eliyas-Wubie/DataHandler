"""
data types and data structures
    num-int,float,double
    string-string,chr
    bool-bool
    dict my_dict = {"name": "John", "age": 25, "city": "New York"}
    set my_set = {1, 2, 3, 4, 5}
    list my_list = [1, 2, 3, "apple", True]
    tuple my_tuple = (1, 2, 3, "apple", True)
    queue from collections import deque      x=deque([1, 2, 3])
operations
    eq - all data structure
    match - string,list,tuple,set,dict
    gt - for num
    lt - for num
    gte - num
    lte - num
    Or
    And
conditionList format
    {
        Op:and,
        value:[
            {
                Op:eq,
                Value:"thisValue",
            },
            {
                Op:match,
                value:"thisMatchValue"
            },
            {
                Op:or,
                value:[
                    {},{}
                ]
                
            }
        ]
    }
Logic
Recursively Check each field, and Valie of the data structure depending on data type. and perform the operation by passing the Key/Value operaition and passwd argument(keyword). - this would take care of FieldCheck(), ValueCheck(), and ValueChange() needed logic
    Mode Handler (findOne,FindAll) (singleValue check, MultiValueCheck), usecase(fieldCheck, ValueCheck, ValueChange, reformat)(replace,checkOnly)
    TypeDependent Recursive Checker
    Operation Handler
    Condition Array Handler
    Result and State Manager
Reformater will have a recursive through new format, and recurively look for specified field and assign the value    
"""

#OperationHandler()
#Recursor(data,input,operation,rtn)
#ConditionHandler()

#FieldCheck() # takes in data,Operation,Value,mode(findOne,FindAll)   returns verdict:t/f location:path to field
#ValueCheck() # takes in data,Operation,value,mode(findOne,FindAll)   returns verdict:t/f location:path to field
#MultiValueCheck() # takes in data,conditionList
#ValueChange()
#ReFormat()