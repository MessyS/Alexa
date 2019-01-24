import time
import household
import tuling
import volume
import yuyinhecheng
import yuyinshibie
import logs
import isKeyword

# 时间
now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 提示音频与对话音频的文件路径
init_prompt = '/opt/MessyPi/yuyin/alexa/music_messy/prompt/how_can_i_help.wav'
none_prompt = '/opt/MessyPi/yuyin/alexa/music_messy/prompt/please_speak.wav'
play_shibie_failed = '/opt/MessyPi/yuyin/alexa/music_messy/prompt/shibie_failed.wav'
play_hecheng_failed = '/opt/MessyPi/yuyin/alexa/music_messy/prompt/hecheng_failed.wav'
i_said = '/opt/MessyPi/yuyin/alexa/music_messy/said/i_said.wav'
alexa_said = '/opt/MessyPi/yuyin/alexa/music_messy/said/alexa_said.wav'

# 语音识别引擎（可选）
# 百度    baidu
# 讯飞    xunfei
shibie_tts = 'baidu'

# 语音合成引擎（可选）
# 百度    baidu
# 讯飞    xunfei
hecheng_tts = 'xunfei'

def main(p,detector):
	detector.terminate()
	print('\033[1;32m     识别成功，随便说说吧! \033[0m')
	# 播放提示语
	volume.play_prompt_not_loop(init_prompt)
	# 录音
	volume_in = volume.volume(p)
	# 语音识别
	i_said_json = eval('yuyinshibie.%s(i_said)' % shibie_tts)
	# 判断是否识别成功(这里我本来想直接用变量的，但不知道为什么第二个if的赋值赋不出来，就先用数组代替)
	shibie_suc = []
	if shibie_tts == 'baidu':
		if int(i_said_json['err_no']) == 0:
			shibie_suc.append('1')
	elif shibie_tts == 'xunfei':
		if int(i_said_json['code']) == 0:
			shibie_suc.append('1','2')
	if len(shibie_suc) == 1 or len(shibie_suc) == 2:
		# 判断有无声源输入
		if len(shibie_suc) == 1:
			i_said_text = i_said_json['result'][0]
		elif len(shibie_suc) == 2:
			i_said_text = i_said_json['data']
		if i_said_text == '':
				volume.play_prompt(none_prompt)
		else:
			keyword = isKeyword.main_1(i_said_text)
			hecheng_keyword = isKeyword.main_2(i_said_text,hecheng_tts)
			# 判断是否包含控制家具关键字
			if keyword==1 and hecheng_keyword==1:
				alexa_said_text = tuling.robot(i_said_text)
				print('      %s' % alexa_said_text)
				# 把我和alexa的对话记录到日志
				logs.suc('i_said%s\n    alexa_said:%s' % i_said_text,alexa_said_text)				
				# 语音合成阶段的错误处理
				hecheng = eval('yuyinhecheng.%s(alexa_said_text)' % hecheng_tts)
				if hecheng == 1:
					volume.play_prompt(alexa_said)
				else:
					logs.yuyin_err('语音合成发生了错误，以下是具体信息:\n%s' % hecheng)
					volume.play_prompt(play_hecheng_failed)
	else:
		logs.yuyin_err('语音识别发生了错误，以下是具体信息:\n%s' % i_said_json)
		volume.play_prompt(play_shibie_failed)
