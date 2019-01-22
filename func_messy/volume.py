'''
##########################     Messy音量检测     ##############################
#                                                                             #
#                               Python3编写                                   #
#                                                                             #
#  文件说明：                                                                 #
#     1.先用'volume.py'检测一下当前环境不说话的音量值,这里默认为300，如需修改 #
#        ，修改变量 fazhi 即可。                                              #
#                                                                             #
#     2.volume.py的测试速度是由CHUNK和RATE决定的。                            #
#                                                                             #
#     3.RATE设置为48000是为了快速检测，16000的采样率为语音识别的最佳成功率，  #
#       但是就是会牺牲掉快速的反应能力.....但这里可以通过调小CHUNK来增强反应  #
#        能力，经测试，190的CHUNK反应速度最佳                                 #
#                                                                             #
###############################################################################
'''
import pyaudio
import wave
import numpy as np
import time
import pygame

# 阈值
YUZHI = 400

# 保存音频文件的配置
CHUNK = 200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "music_messy/said/i_said.wav"

def volume(p):
	# 睡0.5s防止杂音
	time.sleep(0.5)
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)
	# 音频流大小监听
	# print("      开始监听音频流大小...（5s无应答将结束进程）")
	frames = []
	timing = []
	while 1:
		# print('      持续监听中...')
		for i in range(0, 100):
			data = stream.read(CHUNK)
			frames.append(data)
		audio_data = np.fromstring(data, dtype=np.short)
		temp = np.max(audio_data)
			
		if temp > YUZHI:
			# print('      发现音源输入')
			panduan = []
			while 1:
				for i in range(0, 100):
					data = stream.read(CHUNK)
				audio_data = np.fromstring(data, dtype=np.short)
				temp_in = np.max(audio_data)
				
				if len(panduan) > 3:
					if temp_in < YUZHI:
						panduan.append('1')
				else:
					if temp_in < YUZHI:
						# print('      音源输入完毕！')
						stream.stop_stream()
						stream.close()
						break
			break
			
		timing.append('1')
		if len(timing) >= 4:
			break
			
	stream.stop_stream()
	stream.close()

	# 保存截取下来的音频
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	
def play_prompt_not_loop(file):
	pygame.mixer.music.load(file)
	pygame.mixer.music.play()
	while True:
		if pygame.mixer.music.get_busy() != 1:
			break
		else:
			time.sleep(0.05)
	
def play_prompt(file):
	pygame.mixer.music.load(file)
	pygame.mixer.music.play(loops=0)
	time.sleep(1)

