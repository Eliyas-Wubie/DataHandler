from data_handler_ela.checkers import *

data={
    "one":"abcd",
    "two":2
}
flag={
    "cs":False,
    "findOne":False,
    "chain":False
}
cond={
    "Op":"or",
    "Value":[
        {
            "Op":"match",
            "field":"one",
            "Value":"abc"
        }
    ]
}
res=evaluate_object(data,cond)
print(res)