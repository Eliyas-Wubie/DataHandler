import copy
import re

tracker=[]

print("-----------------------STARTING-----------------------------")

def chainHandler(keyword):
    keywrordsList=keyword.split(".")
    cleanList=[path for path in keywrordsList if not path.startswith("[")]
    word=keywrordsList[-1]
    return keywrordsList,cleanList,word

def Recursor(flags,initial=True,result=[],data="", keyword="", op="eq", tip="", temp={}):
    mode=flags.get("mode")
    if initial:
        result=[]
        temp={
            "path":None,
            "value":None,
            "parent":None
        }

    if mode=="fieldCheck": # viable flags:- chains,caseSens,findone
        dataType=type(data)
        if dataType==dict:
            # print("dict triggered", result)
            for item in list(data.keys()):
                # print("_______", item,temp)
                if flags.get("found") and flags.get("findOne"):
                    break
                if temp.get("path")!= None:
                    cleanPath=copy.deepcopy(temp.get("path")).split(".")
                    cleanPath = [path for path in cleanPath if not path.startswith("[")]

                    cleanPath=".".join(cleanPath)
                else:
                    cleanPath=""
                # print("*********2",cleanPath+item,keyword)
                if flags.get("chain"):
                    compareString=cleanPath+"."+item
                else:
                    compareString=item
                if flags.get("cs"):
                    checker=compareString==keyword
                else:
                    checker=compareString.lower()==keyword.lower()
                if checker:
                    newData=copy.deepcopy(temp)
                    newData["value"]=data.get(item)
                    if temp.get("path")==None:
                        newData["path"]=copy.deepcopy(item)
                        temp["path"]=copy.deepcopy(item)
                    else:
                        newData["path"]=copy.deepcopy(temp.get("path")+"."+item)
                        temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                    result.append(newData)
                    flags["found"]=True
                    if type(data.get(item))==dict or type(data.get(item))==list:
                        temp["parent"]=copy.deepcopy({item:data.get(item)})
                    Recursor(flags,False,result, data.get(item), keyword, op, tip, temp)
                else:
                    if temp.get("path")==None:
                        temp["path"]=copy.deepcopy(item)
                    else:
                        temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                    if type(data.get(item))==dict or type(data.get(item))==list:
                        temp["parent"]=copy.deepcopy({item:data.get(item)})
                    Recursor(flags,False,result, data.get(item), keyword, op, tip, temp)
                PathReadjust=temp.get("path").split(".")
                del PathReadjust[-1]
                newPath=".".join(PathReadjust)
                if newPath=="":
                    temp["path"]=None
                else:
                    temp["path"]=newPath
            return result               
        elif dataType==list:
            # print("list triggered", result)
            for i in range(len(data)):
                if flags.get("found") and flags.get("findOne"):
                    break    
                if temp.get("path")!=None:           
                    temp["path"]=temp.get("path")+"."+f"[{i}]"
                else:
                    temp["path"]=f"[{i}]"
                Recursor(flags,False,result, data[i], keyword, op, tip, temp)
                PathReadjust=temp.get("path").split(".")
                del PathReadjust[-1]
                newPath=".".join(PathReadjust) 
                if newPath=="":
                    newPath=None
                temp["path"]=newPath
            return result
        else:
            # print("else triggered", result)
            if initial:
                print("The data is not a dictionary or a list",data)
            return result
    
    elif mode=="valueCheck": # viable flags:- caseSens,findOne
        dataType=type(data)
        if dataType==dict:
            if initial:
                copmareData=copy.deepcopy(data)
                verdict=OperationHandler(copmareData,op,keyword)
                if verdict:
                    newData=copy.deepcopy(temp)
                    newData["value"]=data
                    newData["path"]=copy.deepcopy("main")
                    result.append(newData)
                    flags["found"]=True
                    if type(data)==dict or type(data)==list:
                        temp["parent"]=copy.deepcopy(data)
                else:
                    if type(data)==dict or type(data)==list:
                        # print("prentis now", item)
                        temp["parent"]=copy.deepcopy(data)
            for item in list(data.keys()):
                if flags.get("found") and flags.get("findOne"):
                    break
                if flags.get("cs"):
                    copmareData=copy.deepcopy(data.get(item))
                else:
                    if type(data.get(item))==str:
                        copmareData=copy.deepcopy(data.get(item).lower())
                    else:
                        copmareData=copy.deepcopy(data.get(item))
                    keyword=copy.deepcopy(keyword.lower())

                verdict=OperationHandler(copmareData,op,keyword)
                if verdict:
                    newData=copy.deepcopy(temp)
                    newData["value"]=data.get(item)
                    if temp.get("path")==None:
                        newData["path"]=copy.deepcopy(item)
                        temp["path"]=copy.deepcopy(item)
                    else:
                        newData["path"]=copy.deepcopy(temp.get("path")+"."+item)
                        temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                    result.append(newData)
                    flags["found"]=True
                    if type(data.get(item))==dict or type(data.get(item))==list:
                        # print("prentis now", item)
                        temp["parent"]=copy.deepcopy({item:data.get(item)})
                    Recursor(flags,False,result, data.get(item), keyword, op, item,temp)
                else:
                    if temp.get("path")==None:
                        temp["path"]=copy.deepcopy(item)
                    else:
                        temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                    if type(data.get(item))==dict or type(data.get(item))==list:
                        # print("prentis now", item)
                        temp["parent"]=copy.deepcopy({item:data.get(item)})
                    Recursor(flags,False,result, data.get(item), keyword, op, item,temp)
                PathReadjust=temp.get("path").split(".")
                del PathReadjust[-1]
                newPath=".".join(PathReadjust)
                if newPath=="":
                    temp["path"]=None
                else:
                    temp["path"]=newPath
            return result               
        elif dataType==list:
            # print("iterating--", data)
            for i in range(len(data)):
                if flags.get("found") and flags.get("findOne"):
                    break
                if temp.get("path")!=None:
                    temp["path"]=temp.get("path")+"."+f"[{i}]"
                else:
                    temp["path"]=f"[{i}]"

                LooPdataType=type(data[i])
                if LooPdataType==list or LooPdataType==dict:
                    Recursor(flags,False,result, data[i], keyword, op, tip,temp)
                else:
                    if flags.get("cs"):
                        copmareData=copy.deepcopy(data[i])
                    else:
                        if type(data[i])==str:
                            copmareData=copy.deepcopy(data[i].lower())
                        else:
                            copmareData=copy.deepcopy(data[i])
                        keyword=copy.deepcopy(keyword.lower())
                    verdict=OperationHandler(copmareData,"eq",keyword)
                    # print("------",tip, item)
                    if verdict:
                        if tip=="":
                            tip="main"
                        result.append({f"{tip}-listElement":keyword})
                PathReadjust=temp.get("path").split(".")
                del PathReadjust[-1]
                newPath=".".join(PathReadjust)
                if newPath=="":
                    newPath=None
                temp["path"]=newPath
            return result
        else:
            # print("handling plan data--", data)
            if initial:
                if flags.get("cs"):
                    pass
                else:
                    data=copy.deepcopy(data.lower())
                    keyword=copy.deepcopy(keyword.lower())
                verdict=OperationHandler(data,"eq",keyword)
                result.append({"main-listElement":keyword})
            return result

    elif mode=="keyValueCheck": # viable flags:- chains,caseSens,findone
        dataType=type(data)
        if dataType==dict:
            if tip=="obj":
                listOfKeys=list(data.keys())
                if flags.get("cs"):
                    if flags.get("chain"):
                        pathExtraction=list(keyword.keys())[0].split(".")
                        newKeyward=pathExtraction[-1]
                    else:
                        newKeyward=keyword
                    con=newKeyward in listOfKeys and data.get(newKeyward)==keyword.get(list(keyword.keys())[0])
                else:
                    if flags.get("chain"):
                        pathExtraction=list(keyword.keys())[0].split(".")
                        newKeyward=pathExtraction[-1]
                    else:
                        newKeyward=keyword
                    con=newKeyward in listOfKeys and data.get(newKeyward).lower()==keyword.get(list(keyword.keys())[0]).lower()
                if flags.get("chain"):
                    if temp.get("path")!=None:
                        pathExtraction=copy.deepcopy(temp.get("path").split("."))
                        pathExtraction = [path for path in pathExtraction if not path.startswith("[")]
                        
                    else:
                        pathExtraction=[]
                    pathCon=list(keyword.keys())[0]==".".join(pathExtraction)+"."+newKeyward
                    # print("======",pathCon)
                else:
                    pathCon=True
                if con and pathCon:
                    item=list(keyword.keys())[0]
                    newData=copy.deepcopy(temp)
                    newData["value"]=data.get(item)
                    if temp.get("path")==None:
                        newData["path"]=copy.deepcopy(item)
                    else:
                        newData["path"]=copy.deepcopy(temp.get("path")+"."+newKeyward)
                    result.append(newData)
                    flags["found"]=True
                    # result.append(data)
                    for item in list(data.keys()):
                        if flags.get("found") and flags.get("findOne"):
                            break
                        if temp.get("path")==None:
                            temp["path"]=copy.deepcopy(item)
                        else:
                            temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                        if type(data.get(item))==dict or type(data.get(item))==list:
                            # print("prentis now", item)
                            temp["parent"]=copy.deepcopy({item:data.get(item)})
                        Recursor(flags,False,result, data.get(item), keyword, op, tip,temp)
                        PathReadjust=temp.get("path").split(".")
                        del PathReadjust[-1]
                        newPath=".".join(PathReadjust)
                        if newPath=="":
                            temp["path"]=None
                        else:
                            temp["path"]=newPath
                else:
                    for item in list(data.keys()):
                        if flags.get("found") and flags.get("findOne"):
                            break
                        if temp.get("path")==None:
                            temp["path"]=copy.deepcopy(item)
                        else:
                            temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                        if type(data.get(item))==dict or type(data.get(item))==list:
                            # print("prentis now", item)
                            temp["parent"]=copy.deepcopy({item:data.get(item)})
                        Recursor(flags,False,result, data.get(item), keyword, op, tip,temp)
                        PathReadjust=temp.get("path").split(".")
                        del PathReadjust[-1]
                        newPath=".".join(PathReadjust)
                        if newPath=="":
                            temp["path"]=None
                        else:
                            temp["path"]=newPath
            else:
                for item in list(data.keys()):
                        if flags.get("found") and flags.get("findOne"):
                            break
                        if flags.get("cs"):
                            if flags.get("chain"):
                                pathExtraction=keyword.split(".")
                                newKeyward=pathExtraction[-1]
                            else:
                                newKeyward=keyword
                            # con=newKeyward in listOfKeys and data.get(newKeyward)==keyword.get(list(keyword.keys())[0])
                            con=item==newKeyward and op==data.get(item)
                        else:
                            if flags.get("chain"):
                                pathExtraction=keyword.split(".")
                                newKeyward=pathExtraction[-1]
                            else:
                                newKeyward=keyword
                            con=item==newKeyward and op.lower()==data.get(item).lower()
                        if flags.get("chain"):
                            if temp.get("path")!=None:
                                    pathExtraction=copy.deepcopy(temp.get("path").split("."))
                                    pathExtraction = [path for path in pathExtraction if not path.startswith("[")]
                            else:
                                pathExtraction=[]
                            pathCon=keyword==".".join(pathExtraction)+"."+newKeyward
                            print("======",pathCon)
                        else:
                            pathCon=True
                        if con and pathCon:
                            newData=copy.deepcopy(temp)
                            newData["value"]=data.get(item)
                            if temp.get("path")==None:
                                newData["path"]=copy.deepcopy(item)
                                temp["path"]=copy.deepcopy(item)
                            else:
                                newData["path"]=copy.deepcopy(temp.get("path")+"."+item)
                                temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                            result.append(newData)
                            flags["found"]=True
                            if type(data.get(item))==dict or type(data.get(item))==list:
                                # print("prentis now", item)
                                temp["parent"]=copy.deepcopy({item:data.get(item)})
                            Recursor(flags,False,result, data.get(item), keyword, op, tip, temp)
                        else:
                            if temp.get("path")==None:
                                temp["path"]=copy.deepcopy(item)
                            else:
                                temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                            if type(data.get(item))==dict or type(data.get(item))==list:
                                # print("prentis now", item)
                                temp["parent"]=copy.deepcopy({item:data.get(item)})
                            Recursor(flags,False,result, data.get(item), keyword, op, tip, temp)
                        PathReadjust=temp.get("path").split(".")
                        del PathReadjust[-1]
                        newPath=".".join(PathReadjust)
                        if newPath=="":
                            temp["path"]=None
                        else:
                            temp["path"]=newPath
            return result               
        elif dataType==list:
            # print("list triggered", result)
            for i in range(len(data)):
                if flags.get("found") and flags.get("findOne"):
                    break
                if temp.get("path")!=None:
                    temp["path"]=temp.get("path")+"."+f"[{i}]"
                else:
                    temp["path"]=f"[{i}]"
                Recursor(flags,False,result, data[i], keyword, op, tip,temp)
                PathReadjust=temp.get("path").split(".")
                del PathReadjust[-1]
                newPath=".".join(PathReadjust)
                if newPath=="":
                    newPath=None
                temp["path"]=newPath
            return result
        else:
            # print("else triggered", result)
            if initial:
                print("The data is not a dictionary or a list")
            return result

    elif mode=="multiValueCheck": # viable flags:- caseSens, findone
        dataType=type(data)        
        if dataType==dict:
            for item in list(data.keys()):
                if flags.get("found") and flags.get("findOne"):
                    break
                verdict=ConditionHandler(data.get(item),keyword,"value",flags=flags) # path se flag, cs flag and parent path, so it will take care of the logic
                if verdict:
                    newData=copy.deepcopy(temp)
                    newData.pop("prevParent")
                    newData["value"]=data.get(item)
                    if temp.get("path")==None:
                        newData["path"]=copy.deepcopy(item)
                        temp["path"]=copy.deepcopy(item)
                    else:
                        newData["path"]=copy.deepcopy(temp.get("path")+"."+item)
                        temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                    result.append(newData)
                    flags["found"]=True
                    if type(data.get(item))==dict or type(data.get(item))==list:
                        temp["prevParent"]=copy.deepcopy(temp.get("parent"))
                        temp["parent"]=copy.deepcopy({item:data.get(item)})
                    Recursor(flags,False,result, data.get(item), keyword, op, {item:data.get(item)}, temp)
                    temp["parent"]=copy.deepcopy(temp.get("prevParent"))
                else:
                    if temp.get("path")==None:
                        temp["path"]=copy.deepcopy(item)
                    else:
                        temp["path"]=copy.deepcopy(temp.get("path")+"."+item)
                    if type(data.get(item))==dict or type(data.get(item))==list:
                        temp["prevParent"]=copy.deepcopy(temp.get("parent"))
                        temp["parent"]=copy.deepcopy({item:data.get(item)})
                        # print("_____________",temp.get("prevParent"),temp.get("parent"))
                    Recursor(flags,False,result, data.get(item), keyword, op, {item:data.get(item)},temp)
                    temp["parent"]=copy.deepcopy(temp.get("prevParent"))
                PathReadjust=temp.get("path").split(".")
                del PathReadjust[-1]
                newPath=".".join(PathReadjust)
                if newPath=="":
                    temp["path"]=None
                else:
                    temp["path"]=newPath
            return result               
        elif dataType==list:
            if initial:
                temp["parent"]={"main":data}
            else:
                if type(tip)==dict:
                    key=list(tip.keys())[0]         
                temp["parent"]={key:data}
            for i in range(len(data)):
                if flags.get("found") and flags.get("findOne"):
                    break
                if tip=="":
                    temp["parent"]={f"main":data}
                LooPdataType=type(data[i])
                if LooPdataType==list or LooPdataType==dict:
                    if temp.get("path")!=None:
                        temp["path"]=temp.get("path")+"."+f"[{i}]"
                    else:
                        temp["path"]=f"[{i}]"
                    temp["prevParent"]=copy.deepcopy(temp.get("parent"))
                    temp["parent"]=copy.deepcopy({f"[{i}]":data[i]})
                    # print("_____________",temp.get("prevParent"),temp.get("parent"))
                    Recursor(flags,False,result, data[i], keyword, op, tip,temp)
                    temp["parent"]=copy.deepcopy(temp.get("prevParent"))
                    PathReadjust=temp.get("path").split(".")
                    del PathReadjust[-1]
                    newPath=".".join(PathReadjust)
                    if newPath=="":
                        newPath=None
                    temp["path"]=newPath
                else:
                    print("elements of array",data)
                    verdict=ConditionHandler(data[i],keyword,flags=flags)
                    if verdict:
                            newData=copy.deepcopy(temp)
                            newData["value"]=data[i]
                            if temp.get("path")==None:
                                newData["path"]=copy.deepcopy(f"[{i}]")
                            else:
                                newData["path"]=copy.deepcopy(temp.get("path")+"."+f"[{i}]")
                            result.append(newData) 
                            flags["found"]=True
            return result
        elif initial:
            verdict=ConditionHandler(data,keyword,flags=flags)
            print("handling plan data--", data, keyword,verdict)
            if verdict:
                newData=copy.deepcopy(temp)
                newData["value"]=data
                if temp.get("path")==None:
                    if type(tip)==dict:
                        newData["path"]=copy.deepcopy(list(tip.keys())[0])
                else:
                    newData["path"]=copy.deepcopy(temp.get("path"))
                result.append(newData) 
                flags["found"]=True
            return result

    elif mode=="multiKeyValueCheck": # viable flags:- chain, caseSens, findone and singleElement
        """
        SE verses Chaining
            can they work togather?
            No imposible, because you either have to spacify the same chain again and again in the conditions, which is unessary
            Then which to keep?
            SE.
        SE verses logical operators and/or
            can it work with and?
            yes because you can check if a single object contains all the specified field and values
            can it work with or?
            No because if you set SE and an or, then even the or will allow it to be true if only one matchs, tese single element by its deffination
            only works with and
            can i do and/or without single element?
            yes
        data managment?
            in order to monitor and/or, the and/or list of conditions must be monitored in the condition handler
            where to monitor SE, since we are checking if all conditions are met it has to be the condition handler
            but, the condition handler needs access to all of the object at once.

            These in the recursor, if we find an objct, we must pass it to the condition handler as a whole.
            then the condition handler will check all of the proporties without going deeper.
            going deeper will be handlerd by the recursor.

        """
        dataType=type(data)
        if flags.get("se"):
            if dataType==dict:
                res=ConditionHandler(data,keyword,"object",flags)
                if res.get("conditionCheck"):
                    newRes=copy.deepcopy(temp)
                    newRes["value"]=res.get("data") 
                    result.append(newRes)
                    flags["found"]=True
                temp["parent"]=data
                for item in data.keys():
                    if flags.get("found") and flags.get("findOne"):
                        break
                    if  temp["path"]!=None:
                        temp["path"]=temp.get("path")+"."+item
                    else:
                        temp["path"]=item
                    Recursor(flags,False,result,data.get(item),keyword,op,tip,temp)
                    PathReadjust=temp.get("path").split(".")
                    del PathReadjust[-1]
                    newPath=".".join(PathReadjust)
                    if newPath=="":
                        temp["path"]=None
                    else:
                        temp["path"]=newPath
                return result
            elif dataType==list:
                for i in range(len(data)):
                    if flags.get("found") and flags.get("findOne"):
                        break
                    temp["parent"]=data
                    if  temp["path"]!=None:
                        temp["path"]=temp.get("path")+"."+f"[{i}]"
                    else:
                        temp["path"]=f"[{i}]"
                    Recursor(flags,False,result,data[i],keyword,op,tip,temp)
                    PathReadjust=temp.get("path").split(".")
                    del PathReadjust[-1]
                    newPath=".".join(PathReadjust)
                    if newPath=="":
                        temp["path"]=None
                    else:
                        temp["path"]=newPath
                return result
            else:
                if initial:
                    print("The data is nither a dict nor a list")
                    return result
                else:
                    return result
        else:
            raise Exception(" The following function only works with Single Element flag, please set flag 'se' True ")
    
    elif mode=="valueChange": #viable flags:- caseSense, findOne
        dataType=type(data)
        if dataType==dict:
            for item in list(data.keys()):
                if flags.get("found") and flags.get("findOne"):
                    break
                if flags.get("cs"):
                    # if flags.get("chain"):
                    #     chain,cleanChain,word=chainHandler(keyword)
                    #     con=".".join(chain)==temp.get("path")
                    # else:
                        con=item==keyword
                else:
                    # if flags.get("chain"):
                    #     chain,cleanChain,word=chainHandler(keyword)
                    #     con=".".join(chain).lower()==temp.get("path").lower()
                    # else:
                        con=item.lower()==keyword.lower()
                print("....................",con)
                if con:
                    data[item]=op
                    result.append({item: data.get(item)})
                    flags["found"]=True
                    if temp.get("path")==None:
                        temp["path"]=item
                    else:
                        temp["path"]=temp.get("path")+"."+item
                    Recursor(flags,False,result, data.get(item), keyword, op,tip,temp)
                else:
                    if temp.get("path")==None:
                        temp["path"]=item
                    else:
                        temp["path"]=temp.get("path")+"."+item
                    Recursor(flags,False,result, data.get(item), keyword, op,tip,temp)
                PathReadjust=temp.get("path").split(".")
                del PathReadjust[-1]
                newPath=".".join(PathReadjust)
                if newPath=="":
                    temp["path"]=None
                else:
                    temp["path"]=newPath
            return [data]              
        elif dataType==list:
            for i in range(len(data)):
                if flags.get("found") and flags.get("findOne"):
                    break
                if temp.get("path")==None:
                    temp["path"]=f"[{i}]"
                else:
                    temp["path"]=temp.get("path")+"."+f"[{i}]"
                Recursor(flags,False,result, data[i], keyword, op,tip,temp)
                PathReadjust=temp.get("path").split(".")
                del PathReadjust[-1]
                newPath=".".join(PathReadjust)
                if newPath=="":
                    temp["path"]=None
                else:
                    temp["path"]=newPath
            return [data]
        else:
            if initial:
                print("The data is not a dictionary or a list")
            return [data]
    
def OperationHandler(data, op, value, flags={}):
    # print("___________",flags)
    if op=="eq":
        if flags.get("cs"):
            return data==value
        else:
            if type(data)==str:
                data=data.lower()
            if type(value)==str:
                value=value.lower()
            return data==value
    elif op=="match":
        if type(data)==str and type(value)==str:
            matcher = fr".*{re.escape(value)}.*"
            if re.fullmatch(matcher, data):
                return True
            else:
                return False
        elif type(data)==dict and type(value)==dict:
            collector=[]
            for k,v in value.items():
                if k in data.keys():
                    if v==data.get(k):
                        collector.append(True)
                    else:
                        collector.append(False)
                else:
                    collector.append(False)
            if len(collector)==len(list(value.keys())) and False not in collector:
                return True
            else:
                return False
        
        elif type(data)==list and type(value)==list:
            pass
        else:
            return False
    elif op=="gt":
        if isinstance(data, (int, float)) and isinstance(data, (int, float)):
            return data>value
        else:
            return False
    elif op=="lt":
        if isinstance(data, (int, float)) and isinstance(data, (int, float)):
            return data<value
        else:
            return False
    elif op=="gte":
        if isinstance(data, (int, float)) and isinstance(data, (int, float)):
            return data>=value
        else:
            return False
    elif op=="lte":
        if isinstance(data, (int, float)) and isinstance(data, (int, float)):
            return data<=value
        else:
            return False

def ConditionHandler(data, condition, mode="value", flags={}): # wrong implementation, field and value need to be checked at the same time
    verdict=[]
    # print("mode",mode)
    if mode=="object":
        if condition.get("Op")=="and" or condition.get("Op")=="or":
            collector=[]
            for item in condition.get("Value"):
                subcollector=[]
                # what if item.get("Op") is and/or
                if item.get("Op")!="and" and item.get("Op")!="or":
                    for k,v in data.items():
                        res=ConditionHandler({k:v},item,"key:value",flags)
                        subcollector.append(res)
                    if True in subcollector:
                        collector.append(True)
                    else:
                        collector.append(False)
                else:
                    res=ConditionHandler(data,item,"object",flags)
                    collector.append(res)
                print("item and result",item,collector)
                
            if condition.get("Op")=="and":
                print("condition handler and")
                if False in collector:
                    return {"conditionCheck":False,"data":None}
                else:
                    return {"conditionCheck":True,"data":data}

            elif condition.get("Op")=="or":
                print("condition handler or")
                if True in collector:
                    return {"conditionCheck":True,"data":data}
                else:
                    return {"conditionCheck":False,"data":None}
        else:
            print("not and or or")
            verdict=OperationHandler(data,condition.get("Op"),condition.get("Value"),flags)
            return verdict
    elif mode=="key:value":
        if flags.get("cs"):
            verdict=OperationHandler(data,condition.get("Op"),{condition.get("field"):condition.get("Value")},flags)
        else:
            dataKey=list(data.keys())[0]
            dataValue=list(data.values())[0]
            conKey=copy.deepcopy(condition.get("field"))
            conValue=copy.deepcopy(condition.get("Value"))
            if type(dataKey)==str:
                dataKey=dataKey.lower()
            if type(dataValue)==str:
                dataValue=dataValue.lower()
            if type(conKey)==str:
                conKey=conKey.lower()
            if type(conValue)==str:
                conValue=conValue.lower()
            verdict=OperationHandler({dataKey:dataValue},condition.get("Op"),{conKey:conValue},flags)
        return verdict
    elif mode=="value" or mode=="field":
        # print("--------condition check")
        verdict=[]
        if condition.get("Op")=="and" or condition.get("Op")=="or":
            resCollection=[]
            for item in condition.get("Value"):
                res=ConditionHandler(data,item,mode,flags)
                resCollection.append(res)
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
                verdict=OperationHandler(data,condition.get("Op"),condition.get("Value"),flags)
                return verdict
            elif mode=="field":
                verdict=OperationHandler(data,condition.get("Op"),condition.get("field"),flags)
                return verdict
        # if condition.get("Op")=="and" or condition.get("Op")=="or":
        #     resCollection=[]
        #     numOfConditions=len(condition.get("Value"))
        #     for item in condition.get("Value"):
        #         resCollection.append(ConditionHandler(data,item,mode,flags))
        #     if condition.get("Op")=="and":
        #         if flags.get("se"):
        #             if False in resCollection:
        #                 return False
        #             elif numOfConditions==len(resCollection):
        #                 return True
        #             else:
        #                 return False
        #         else:
        #             if False in resCollection:
        #                 return False
        #             else:
        #                 return True
        #     elif condition.get("Op")=="or":
        #         if True in resCollection:
        #             return True
        #         else:
        #             return False
        # else:
        #     if mode=="value": 
        #         verdict=OperationHandler(data,condition.get("Op"),condition.get("Value"),flags)
        #         return verdict
        #     elif mode=="field":
        #         verdict=OperationHandler(data,condition.get("Op"),condition.get("field",flags))
        #         return verdict
    else:
        print("condition mode ELSE trigered !!!!!!!!!!!!!!!!!!!!!!!!!!")

def FieldCheck(flags,data,fieldName=""): #DONE and TESTED
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
    res=Recursor(flags,True, [], data, fieldName)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def ValueCheck(flags,data, operator, value):  #DONE and TESTED
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
    res=Recursor(flags,True, [], data, value, operator)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def KeyValueCheck(flags,data, keyword, value=""): #DONE and TESTED
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
        res=Recursor(flags, True, [], data, keyword, value, "obj")
    else:
        flags["mode"]="keyValueCheck"
        flags["Found"]=False
        res=Recursor(flags, True, [], data, keyword, value)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

# maybe i need a single field with multi Value check, only dose or, dosnt do and

def MultiValueCheck(flags,data, condition): #DONE and TESTED
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
    res=Recursor(flags,True, [], data, condition)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def MultiKeyValueCheck(flags,data,condition):
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
    res=Recursor(flags,True, [], data, condition)
    # print("enddddddddd",res)
    return res
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def ValueChange(flags,data,key,value): #DONE and TESTED
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
    res=Recursor(flags,True, [], data, key, value)
    if len(res)!=0:
        return {"verdict":True, "data":res}
    else:
        return {"verdict":False, "data":None}

def MatchObject(data,matcher):
    pass         

def EvaluateObject(data,condition,initial=True): #DONE and TESTED
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

   

