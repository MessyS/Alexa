import traceback
import time

err_file = 'logs/error.log'
suc_file = 'logs/success.log'
now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def err():
	text = traceback.format_exc()
	logs_text = '[ ' + now_time + ' ] \n' + str(text) + '\n'
	with open(err_file,'a') as f:
		f.write(logs_text)
	return text
	
def suc(text):
	logs_text = '[ ' + now_time + ' ] ' + str(text) + '\n\n'
	with open(suc_file,'a') as f:
		f.write(logs_text)
