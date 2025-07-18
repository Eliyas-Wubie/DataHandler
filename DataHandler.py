from Test.Data import *


print("-----------------------STARTING-----------------------------")
print(TestD,TestAoO)

#OperationHandler()
#Recursor(data,input,operation,rtn)
#ConditionHandler()

#FieldCheck(X) # takes in data,Operation,Value,mode(findOne,FindAll)   returns verdict:t/f location:path to field
#ValueCheck(X) # takes in data,Operation,value,mode(findOne,FindAll)   returns verdict:t/f location:path to field
#MultiValueCheck() # takes in data,conditionList
#ValueChange()
#ReFormat()

def Recursor(mode,initial=True,result=[],data="", keyword="", op="eq", tip=""):
    if initial:
        result=[]
    if mode=="fieldCheck":
        dataType=type(data)
        if dataType==dict:
            print("dict triggered", result)
            for item in list(data.keys()):
                print("_______", item)
                if item==keyword:
                    result.append({item: data.get(item)})
                    Recursor(mode,False,result, data.get(item), keyword)
                else:
                    Recursor(mode,False,result, data.get(item), keyword)
            return result               
        elif dataType==list:
            print("list triggered", result)
            for item in data:
                Recursor(mode,False,result, item, keyword)
            return result
        else:
            print("else triggered", result)
            if initial:
                print("The data is not a dictionary or a list")
            return result
    
    elif mode=="valueCheck":
        dataType=type(data)
        if dataType==dict:
            print("object iteration---",list(data.keys()))
            for item in list(data.keys()):
                verdict=OperationHandler(data.get(item),op,keyword)
                if verdict:
                    result.append({item: data.get(item)})
                    Recursor(mode,False,result, data.get(item), keyword, op, item)
                else:
                    Recursor(mode,False,result, data.get(item), keyword, op, item)
            return result               
        elif dataType==list:
            print("iterating--", data)
            for item in data:
                LooPdataType=type(item)
                if LooPdataType==list or LooPdataType==dict:
                    Recursor(mode,False,result, item, keyword, op, tip)
                else:
                    verdict=OperationHandler(item,"eq",keyword)
                    print("------",tip, item)
                    if verdict:
                        if tip=="":
                            tip="main"
                        result.append({f"{tip}-listElement":keyword})
            return result
        else:
            print("handling plan data--", data)
            verdict=OperationHandler(data,"eq",keyword)
            if verdict:
                if initial:
                    result.append({"main-listElement":keyword})
                else:
                    result.append({f"{tip}-listElement":keyword})
            return result

    elif mode=="keyValueCheck":
        dataType=type(data)
        if dataType==dict:
            if tip=="obj":
                if data==keyword:
                    result.append(data)
                    for item in list(data.keys()):
                        Recursor(mode,False,result, data.get(item), keyword, op, tip)
                else:
                    for item in list(data.keys()):
                        Recursor(mode,False,result, data.get(item), keyword, op, tip)
            else:
                for item in list(data.keys()):
                        if item==keyword and op==data.get(item):
                            result.append({item: data.get(item)})
                            Recursor(mode,False,result, data.get(item), keyword, op, tip)
                        else:
                            Recursor(mode,False,result, data.get(item), keyword, op, tip)
            return result               
        elif dataType==list:
            # print("list triggered", result)
            for item in data:
                Recursor(mode,False,result, item, keyword, op, tip)
            return result
        else:
            # print("else triggered", result)
            if initial:
                print("The data is not a dictionary or a list")
            return result

    elif mode=="multiValueCheck":
        dataType=type(data)
        if dataType==dict:
            print("object iteration---",list(data.keys()))
            for item in list(data.keys()):
                verdict=ConditionHandler(data.get(item),keyword)
                if verdict:
                    result.append({item: data.get(item)})
                    Recursor(mode,False,result, data.get(item), keyword, op, {item:data.get(item)})
                else:
                    Recursor(mode,False,result, data.get(item), keyword, op, {item:data.get(item)})
            return result               
        elif dataType==list:
            print("iterating--", data)
            for item in data:
                LooPdataType=type(item)
                if LooPdataType==list or LooPdataType==dict:
                    Recursor(mode,False,result, item, keyword, op, tip)
                else:
                    verdict=ConditionHandler(item,keyword)
                    print("------",tip, item)
                    if verdict:
                        if tip=="":
                            tip="main"
                            result.append({f"{tip}-listElement":item})
                        else:
                            result.append({f"{list(tip.keys())[0]}-listElement":tip.get(list(tip.keys())[0])})
            return result
        else:
            print("handling plan data--", data)
            verdict=OperationHandler(data,"eq",keyword)
            if verdict:
                if initial:
                    result.append({"main-listElement":keyword})
                else:
                    result.append({f"{tip}-listElement":keyword})
            return result

    elif mode=="multiKeyValueCheck":
        dataType=type(data)
        if dataType==dict:
            for item in list(data.keys()):
                print("..,.,.,.,.,.,.,", item,keyword)
                fieldCheck=ConditionHandler(item,keyword,"field")
                if fieldCheck:
                    verdict=ConditionHandler(data.get(item),keyword)
                    if verdict:
                        result.append({item: data.get(item)})
                        Recursor(mode,False,result, data.get(item), keyword, op, {item:data.get(item)})
                    else:
                        Recursor(mode,False,result, data.get(item), keyword, op, {item:data.get(item)})
            return result               
        elif dataType==list:
            print("iterating--", data)
            for item in data:
                LooPdataType=type(item)
                if LooPdataType==list or LooPdataType==dict:
                    Recursor(mode,False,result, item, keyword, op, tip)
            return result
        else:
            return result

    elif mode=="valueChange":
        dataType=type(data)
        if dataType==dict:
            print("dict triggered", result)
            for item in list(data.keys()):
                print("_______", item, op)
                if item==keyword:
                    data[item]=op
                    result.append({item: data.get(item)})
                    Recursor(mode,False,result, data.get(item), keyword, op)
                else:
                    Recursor(mode,False,result, data.get(item), keyword, op)
            return [data]              
        elif dataType==list:
            print("list triggered", result)
            for item in data:
                Recursor(mode,False,result, item, keyword, op)
            return [data]
        else:
            print("else triggered", result)
            if initial:
                print("The data is not a dictionary or a list")
            return [data]
    
def OperationHandler(data, op, value):
    if op=="eq":
        return data==value
    elif op=="match":
        pass
    elif op=="gt":
        pass
    elif op=="lt":
        pass
    elif op=="gte":
        pass
    elif op=="lte":
        pass

def ConditionHandler(data, condition, mode="value"):
    verdict=[]
    if condition.get("Op")=="and" or condition.get("Op")=="or":
        resCollection=[]
        print(".............",condition.get("Value"))
        for item in condition.get("Value"):
            resCollection.append(ConditionHandler(data,item,mode))
        if condition.get("Op")=="and":
            if False in resCollection:
                return False
            else:
                return True
        elif condition.get("Op")=="or":
            if True in resCollection:
                return True
            else:
                return False
    else:
        if mode=="value":
            verdict=OperationHandler(data,condition.get("Op"),condition.get("Value"))
            return verdict
        elif mode=="field":
            verdict=OperationHandler(data,condition.get("Op"),condition.get("field"))
            return verdict

def FieldCheck(data,fieldName=""):
    res=Recursor("fieldCheck",True, [], data, fieldName)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def ValueCheck(data, operator, value):
    res=Recursor("valueCheck",True, [], data, value, operator)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def KeyValueCheck(data, keyword, value=""):
    if type(keyword)==dict:
        res=Recursor("keyValueCheck",True, [], data, keyword, value, "obj")
    else:
        res=Recursor("keyValueCheck",True, [], data, keyword, value)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def MultiValueCheck(data, condition):
    res=Recursor("multiValueCheck",True, [], data, condition)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def MultiKeyValueCheck(data,condition):
    res=Recursor("multiKeyValueCheck",True, [], data, condition)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def ValueChange(data,key,value):
    res=Recursor("valueChange",True, [], data, key, value)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def Reform():
    pass
# res=KeyValueCheck(TestAoO,{"t1":["abc", "haha"]})
# res=ConditionHandler("thisValue",TestCon)
res=ValueChange(TestAoO,"t1","lala")
print("********",res)
print("-----------------------DONE-----------------------------")