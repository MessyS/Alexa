import os,time,threading
import logs,volume

play_ok = 'music_messy/prompt/as_you_wish.wav'
play_go = 'music_messy/prompt/end.wav'
play_back = 'music_messy/prompt/start.wav'
play_read_temper = 'music_messy/prompt/read_temper.wav'

send_433 = '/opt/MessyPi/led/433codesend'
send_315 = '/opt/MessyPi/led/315codesend'

code_433 = {
	'open':'xxxxxxxx',
	'down':'xxxxxxxx'
}

code_315_1 = {
	'open':'xxxxxxxx',
	'down':'xxxxxxxx'
}

code_315_2 = {
	'open':'xxxxxxxx',
	'down':'xxxxxxxx',
	'down_60s':'xxxxxxxxx',
	'down_5min':'xxxxxxxx'
}

def light_433(action):
	print(action)
	os.system(send_433 + ' ' + code_433[action])
	volume.play_prompt(play_ok)
	return 'ok'

def temperature():
	volume.play_prompt(play_read_temper)
	text = os.popen('python3 /opt/MessyPi/wendu/test_one.py').read()
	return text

def setTimeOut_down():
	time.sleep(360)
	os.system(send_433 + ' ' + code_433['down'])

def SE(bool):
	if bool == 0:
		volume.play_prompt(play_back)
		print('       Messy，祝你有个愉快的一天！')
		logs.suc('i_said:我回来了')
	elif bool == 1:
		volume.play_prompt(play_go)
		print('       将在五分钟后切断相应设备电源并开启监控模式，晚安！')
		logs.suc('i_said:我走了')
		t = threading.Thread(target=setTimeOut_down)
		t.start()
