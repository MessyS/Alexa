import traceback
import time

err_file = '/opt/MessyPi/yuyin/alexa/logs/error.log'
suc_file = '/opt/MessyPi/yuyin/alexa/logs/success.log'
sta_file = '/opt/MessyPi/yuyin/alexa/logs/start.log'
now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def err():
	text = traceback.format_exc()
	logs_text = '[ %s ] \n%s\n' % (now_time,text)
	with open(err_file,'a') as f:
		f.write(logs_text)
	return text

def yuyin_err(text):
	logs_text = '[ %s ] \n%s\n' % (now_time,text)
	with open(err_file,'a') as f:
		f.write(logs_text)
	return text
	
def suc(text):
	logs_text = '[ %s ] \n%s\n\n' % (now_time,text)
	with open(suc_file,'a') as f:
		f.write(logs_text)

def start():
	logs_text = '[ ' + now_time + ' ]   启动成功!\n'
	with open(sta_file,'a') as f:
		f.write(logs_text)