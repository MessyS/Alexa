import os,time,threading
import logs

send_433 = '/opt/MessyPi/led/433codesend'
send_315 = '/opt/MessyPi/led/315codesend'

code_433 = {
	'open':'xxxxxxxxxx',
	'down':'xxxxxxxxxx'
}

code_315_1 = {
	'open':'xxxxxxxxxx',
	'down':'xxxxxxxxxx'
}

code_315_2 = {
	'open':'xxxxxxxxxx',
	'down':'xxxxxxxxxx',
	'down_60s':'xxxxxxxxxx',
	'down_5min':'xxxxxxxxxx'
}

def light_433(text):
	if str(text).find('开灯') != -1:
		os.system(send_433 + ' ' + code_433['open'])
		logs.suc('    i_said:开灯')
		return 'light_ok'
	elif str(text).find('关灯') != -1:
		os.system(send_433 + ' ' + code_433['down'])
		logs.suc('    i_said:关灯')
		return 'light_ok'
	else:
		return True

def temperature(text):
	if str(text).find('温度') != -1:
		text = os.popen('python3 /opt/MessyPi/wendu/test_one.py').read()
		return text
	else:
		return True

def setTimeOut_down():
	time.sleep(360)
	os.system(send_433 + ' ' + code_433['down'])

def SE(text):
	if str(text).find('我回来了') != -1:
		print('       Messy，祝你有个愉快的一天！')
		logs.suc('    i_said:我回来了')
		return 'back'
	elif str(text).find('我走了') != -1:
		print('       将在五分钟后切断相应设备电源并开启监控模式，晚安！')
		logs.suc('    i_said:我走了')
		t = threading.Thread(target=setTimeOut_down)
		t.start()
		return 'go'
	else:
		return True
		
def check(text):
	check_list = [light_433(text),temperature(text),SE(text)]
	for i in check_list:
		if i != 1:
			return i
			os._exit()
	return True
