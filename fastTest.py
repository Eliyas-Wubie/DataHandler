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
res=check_key_value(data,{"one":"abcd"},"eq",flag)
print(res)