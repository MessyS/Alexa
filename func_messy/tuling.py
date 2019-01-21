import requests
import json
import time


def robot(content):
    api = r'http://openapi.tuling123.com/openapi/api/v2'
    userid = int(time.time())
    data = {
        "perception": {
            "inputText": {
                "text": content
                         }
                      },
        "userInfo": {
                    "apiKey": "xxxxxxxxxx",
                    "userId": userid,
                    }
    }
    
    jsondata = json.dumps(data)
    response = requests.post(api, data=jsondata,verify=True)
    robot_res = json.loads(response.content.decode('utf-8'))
    return robot_res["results"][0]['values']['text']
