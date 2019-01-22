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
init_prompt = 'music_messy/prompt/how_can_i_help.wav'
none_prompt = 'music_messy/prompt/please_speak.wav'
play_shibie_failed = 'music_messy/prompt/shibie_failed.wav'
play_hecheng_failed = 'music_messy/prompt/hecheng_failed.wav'
i_said = 'music_messy/said/i_said.wav'
alexa_said = 'music_messy/said/alexa_said.wav'

def main(p,detector):
	detector.terminate()
	print('\033[1;32m     识别成功，随便说说吧! \033[0m')
	# 播放提示语
	volume.play_prompt_not_loop(init_prompt)
	# 录音
	volume_in = volume.volume(p)
	# 语音识别
	i_said_json = yuyinshibie.shibie(i_said)
	# 判断是否识别成功
	if int(i_said_json['code']) == 0:
		i_said_text = i_said_json['data']
		#print('      ' + i_said_text)
		# 判断有无声源输入
		if i_said_text == '':
			volume.play_prompt(none_prompt)
		else:
			keyword = isKeyword.main_1(i_said_text)
			hecheng_keyword = isKeyword.main_2(i_said_text)
			# 判断是否包含控制家具关键字
			if keyword==1 and hecheng_keyword==1:
				alexa_said_text = tuling.robot(i_said_text)
				print('      ' + alexa_said_text)
				# 把我和alexa的对话记录到日志
				logs.suc('i_said' + i_said_text + '\n    alexa_said:' + alexa_said_text)				
				# 语音合成阶段的错误处理
				hecheng = yuyinhecheng.hecheng(alexa_said_text)
				if hecheng == 1:
					volume.play_prompt(alexa_said)
				else:
					volume.play_prompt(play_hecheng_failed)
	else:
		print('语音识别发生了错误，错误码为:', i_said_json['code'], '错误原因为:', i_said_json['desc'])
		volume.play_prompt(play_shibie_failed)
