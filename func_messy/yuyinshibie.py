import urllib.parse, urllib.request
import time
import json
import hashlib
import base64
from aip import AipSpeech

# 百度
app_id = 'xxxxxxxxx'
api_key = 'xxxxxxxxx'
sceret_key = 'xxxxxxxxx'
client = AipSpeech(app_id, api_key, sceret_key)

# 讯飞
url = 'http://api.xfyun.cn/v1/service/v1/iat'
api_key = 'xxxxxxxxx'
x_appid = 'xxxxxxxxx'
 
def shibie(file):
	f = open(file, 'rb')
	file_content = f.read()
	base64_audio = base64.b64encode(file_content)
	body = urllib.parse.urlencode({'audio': base64_audio})
	param = {"engine_type": "sms16k", "aue": "raw"}
	x_time = int(int(round(time.time() * 1000)) / 1000)
	x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
	x_checksum_content = api_key + str(x_time) + str(x_param, 'utf-8')
	x_checksum = hashlib.md5(x_checksum_content.encode('utf-8')).hexdigest()
	x_header = {'X-Appid': x_appid,
				'X-CurTime': x_time,
				'X-Param': x_param,
				'X-CheckSum': x_checksum}

	req = urllib.request.Request(url = url, data = body.encode('utf-8'), headers = x_header, method = 'POST')
	result = urllib.request.urlopen(req)
	result = result.read().decode('utf-8')
	result = json.loads(result)
	return result
	
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
	
def baidu(file):
	result = client.asr(get_file_content(file), 'wav', 16000, {'lan': 'zh',})
	return result
