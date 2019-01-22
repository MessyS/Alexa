import base64
import json
import time
import hashlib
import urllib.request
import urllib.parse

api_url = "http://api.xfyun.cn/v1/service/v1/tts"
API_KEY = "xxxxxxxxxx"
APP_ID = "xxxxxxxxxx"

#合成音频输出文件路径
OUTPUT_FILE = "music_messy/said/alexa_said.wav"

# 构造输出音频配置参数
Param = {
	"auf": "audio/L16;rate=16000",    #音频采样率
	"aue": "raw",    #音频编码，raw(生成wav)或lame(生成mp3)
	"voice_name": "xiaoyan",
	"speed": "50",    #语速[0,100]
	"volume": "77",    #音量[0,100]
	"pitch": "50",    #音高[0,100]
	"engine_type": "aisound"    #引擎类型。aisound（普通效果），intp65（中文），intp65_en（英文）
}

# 配置参数编码为base64字符串，过程：字典→明文字符串→utf8编码→base64(bytes)→base64字符串
Param_str = json.dumps(Param)    #得到明文字符串
Param_utf8 = Param_str.encode('utf8')    #得到utf8编码(bytes类型)
Param_b64 = base64.b64encode(Param_utf8)    #得到base64编码(bytes类型)
Param_b64str = Param_b64.decode('utf8')    #得到base64字符串

# 构造HTTP请求的头部
time_now = str(int(time.time()))
checksum = (API_KEY + time_now + Param_b64str).encode('utf8')
checksum_md5 = hashlib.md5(checksum).hexdigest()
header = {
	"X-Appid": APP_ID,
	"X-CurTime": time_now,
	"X-Param": Param_b64str,
	"X-CheckSum": checksum_md5
}

# 发送HTTP POST请求
def hecheng(text):
	# 构造HTTP请求Body
	body = {
		"text": text
	}
	body_urlencode = urllib.parse.urlencode(body)
	body_utf8 = body_urlencode.encode('utf8')
	
	req = urllib.request.Request(api_url, data=body_utf8, headers=header)
	response = urllib.request.urlopen(req)
	
	# 读取结果
	response_head = response.headers['Content-Type']
	if(response_head == "audio/mpeg"):
		out_file = open(OUTPUT_FILE, 'wb')
		data = response.read() # a 'bytes' object
		out_file.write(data)
		out_file.close()
		return True
	else:
		hecheng = response.read().decode('utf8')
		print(hecheng)
		return False
