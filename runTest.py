from data_handler_ela.checkers import *
from data_handler_ela.changers import *
from Test.Data import *



alert={
        "@timestamp": "2025-07-07T14:16:53.250398Z",
        "agent": {
        "name": "DESKTOP-T9SEU1K",
        "type": "filebeat",
        "version": "8.14.1",
        "ephemeral_id": "3b43dcfe-c1cd-4885-9cd9-f6439b99f501",
        "id": "8e99d055-0cb2-455d-9bb9-c1d5180da4ef"
        },
                "log": {
                "offset": 167030961,
                "file": {
                    "idxlo": "288",
                    "idxhi": "4587520",
                    "vol": "1353783529",
                    "path": "C:\\ProgramData\\edrsvc\\log\\output_events\\2025-06-30.log"
                }
                },
                "ALRID": "ALR-00TEST",
                "@version": "1",
                "input": {
                "type": "filestream"
                },
                "tags": [
                "beats_input_codec_plain_applied"
                ],
                "esafeedr": {
                "processes":  [
        {
          "creationTime": 1751896789841,
          "imagePath": "C:\\Windows\\System32\\winlogon.exe",
          "esfVerdict": 1,
          "verdict": 1,
          "pid": 616,
          "id": 12427280131478346000,
          "imageHash": "dca8efc69ea511e7c3e31178fb2cb1c604b6905c",
          "userName": "SYSTEM@NT AUTHORITY"
        },
        {
          "creationTime": 1751896817334,
          "imagePath": "C:\\Windows\\System32\\userinit.exe",
          "esfVerdict": 1,
          "verdict": 1,
          "pid": 5968,
          "id": 11429772018531113000,
          "imageHash": "081729b1fdae100a8efabd58e08f8423e1617dbc",
          "userName": "Snort@DESKTOP-T9SEU1K"
        },
        {
          "creationTime": 1751896817396,
          "imagePath": "C:\\Windows\\explorer.exe",
          "esfVerdict": 1,
          "verdict": 1,
          "pid": 5992,
          "id": 1669283301608117800,
          "imageHash": "b2aac41ac6918a16b3e686c83aa4949600be982c",
          "userName": "Snort@DESKTOP-T9SEU1K"
        },
        {
          "creationTime": 1751897736270,
          "imagePath": "C:\\Users\\Snort\\Downloads\\Test\\main.exe",
          "esfVerdict": 2,
          "verdict": 2,
          "pid": 468,
          "id": 5683020368336209000,
          "imageHash": "f1769281831a5f515e2b1cc9ba3c9ebc99de1a04C",
          "userName": "Snort@DESKTOP-T9SEU1K"
        },
        {
          "creationTime": 1751897736888,
          "imagePath": "C:\\Users\\Snort\\Downloads\\Test\\main.exe",
          "esfVerdict": 2,
          "verdict": 2,
          "pid": 4584,
          "id": 12354855325878936000,
          "imageHash": "f1769281831a5f515e2b1cc9ba3c9ebc99de1a04",
          "userName": "Snort@DESKTOP-T9SEU1K"
        },
      ],
                "time": 1751267366499,
                "type": "RF1.1111197897897",
                "eventType": "f885ad4e67f54ee2ad9a50c2dd0c2a51",
                "customerId": "",
                "baseType": 1,
                "baseEventType": 1,
                "version": "1.1",
                "deviceName": "DESKTOP-T9SEU1K",
                "endpointId": "1262beb7604041e889c5d1f7737eee89",
                "sessionUser": "Snort@DESKTOP-T9SEU1K"
                },
                "ecs": {
                "version": "8.0.0"
                },
                "host": {
                "hostname": "desktop-t9seu1k",
                "architecture": "x86_64",
                "ip": [
                    "fe80::d8ff:5060:f230:9168",
                    "169.254.83.107",
                    "::ece5:7854:26f:c7cc",
                    "::4454:950:7326:5bbc",
                    "fe80::f4b:c424:f21:1bec",
                    "192.168.1.124"
                ],
                "id": "efeaa575-b950-4b36-89ea-e260fb5b6f37",
                "name": "desktop-t9seu1k",
                "mac": [
                    "00-0C-29-92-64-FF"
                ],
                "os": {
                    "build": "19045.5965",
                    "kernel": "10.0.19041.5965 (WinBuild.160101.0800)",
                    "version": "10.0",
                    "name": "Windows 10 Pro",
                    "platform": "windows",
                    "family": "windows",
                    "type": "windows"
                }
                },
                "event": {
                "organization": {
                    "name": "snort"
                },
                "application": {
                    "name": "esafeedr"
                },
                "id": "315b63fa-d2f7-4ae9-ad69-006b8febdcf3",
                "incident": {
                    "name": ""
                },
                "origional": {
                    "id": "f31ec3bb-8ba0-4bd7-b8db-d312582a591e"
                },
                "status": "Cloned Event"
                },
                "ticket": {
                "mttr": {
                    "end_time": "0"
                },
                "remark": "",
                "reopen": {
                    "mttr": {
                    "end_time": "0"
                    },
                    "updated": {
                    "time": "0"
                    },
                    "created": {
                    "time": "0"
                    }
                },
                "assigner": {
                    "id": "0"
                },
                "engineer": {
                    "assigned": {
                    "updated_time": "0",
                    "time": "0",
                    "status": "Unassigned"
                    },
                    "id": "0"
                },
                "updated": {
                    "time": "0"
                },
                "status": "Backlog",
                "created": {
                    "time": "0"
                }
                }
            }
    
flag={
    "chain":False,             # n
    "se":False,                # n
    "cs":True,                 # w
    "findOne":False            # w
}
conArray={
    "Op":"or",
    "Value":[
        {
            "field":"type",
            "Op":"eq",
            "Value":"filebeatx"
        },        
        {
            "field":"esfVerdict",
            "Op":"eq",
            "Value":2
        },
        {
            "Op":"and",
            "Value":[
                    {
                        "field":"@version",
                        "Op":"eq",
                        "Value":"1"
                    },
                        {
                        "field":"@version",
                        "Op":"eq",
                        "Value":"2"
                    }
            ]
        }
    
    ]
}


conArray2={
    "Op":"or",
    "Value":[
        {
            "field":"t9",
            "Op":"eq",
            "Value":"abcd"
        }
    
    ]
}

res=change_value(TestAoO,"t9","XXXX",flags=flag)

print(res)