import time
import household
import tuling
import volume
import yuyinhecheng
import yuyinshibie
import logs

# 时间
now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 提示音频与对话音频的文件路径
init_prompt = 'music_messy/prompt/how_can_i_help.wav'
none_prompt = 'music_messy/prompt/please_speak.wav'
i_said = 'music_messy/said/i_said.wav'
alexa_said = 'music_messy/said/alexa_said.wav'
# 家居设备识别后的音频
play_go = 'music_messy/prompt/end.wav'
play_back = 'music_messy/prompt/start.wav'
play_ok = 'music_messy/prompt/as_you_wish.wav'

def main(p,detector):
	# 该条代码很重要
	# 因为snowboy已经在内部使用pyaudio库获取了MIC的权限
	# 如果这时在手动调用pyaudio，会造成三种情况
	#
        # 一：录下来的文件没有声音
        # 二：系统直接提示未知的媒体设备（Device unavailable）
        # 三：snowboy程序被挤掉，系统提示无媒体设备（No available audio device）
	#
	# 这个函数是在snowboydecoder.py文件中定义的，
	# 是官方的结束程序占用媒体设备的函数，
	# 我们在finally的最后也可以看到这一条语句，
	# 这样就能确保媒体资源正常使用
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
			# 判断是否包含控制家具关键字
			house = household.check(i_said_text)
			if house == True:
				alexa_said_text = tuling.robot(i_said_text)
				print('      ' + alexa_said_text)
				# 把我和alexa的对话记录到日志
				logs.suc('\n    i_said' + i_said_text + '\n    alexa_said:' + alexa_said_text)
				yuyinhecheng.hecheng(alexa_said_text)
				volume.play_prompt(alexa_said)
			elif house == 'light_ok':
				volume.play_prompt(play_ok)
			elif house.find('当前室内温度') != -1:
				yuyinhecheng.hecheng(house)
				volume.play_prompt(alexa_said)
			elif house == 'go':
				volume.play_prompt(play_go)
			elif house == 'back':
				volume.play_prompt(play_back)
	else:
		print('语音识别发生了错误，错误码为:', i_said_json['code'], '错误原因为:', i_said_json['desc'])
