import os,sys,time,ssl,wave
import signal
import pyaudio,pygame
import speech_recognition as sr

#引入自定义库路径(sys的引入必须要用绝对路径，所以这里自己换一下)
sys.path.append("/opt/MessyPi/yuyin/alexa/func_alexa")
sys.path.append("/opt/MessyPi/yuyin/alexa/func_messy")

import copyright
import logs
import main
import volume
import snowboydecoder

play_goodbye = 'music_messy/prompt/good_by_messy.wav'
play_bug = 'music_messy/prompt/warning_bug.wav'

#关闭系统的报错
os.close(sys.stderr.fileno())

if __name__ == '__main__':
	try:	
		# 打印版权信息，注释这条前大家加下群吧，或收藏一下我的博客也可以，谢谢大家(〃'▽'〃)
		copyright.main()
		# 各项准备工作检查
		try:
			p = pyaudio.PyAudio()
			print('\033[1;32m     ##################   声卡驱动加载成功！  ################### \033[0m')
		except:
			err = logs.err()
			print('\033[1;31m     ############  声卡驱动加载失败！请检查声卡驱动 ############# \033[0m')
			exit()		
		try:
			# 普通情况下直接init就可以了
			# 但我的声卡播放出来声卡有些怪异，所以这里调下频率来解决问题
			pygame.mixer.init(frequency=15500, size=-16, channels=4)
			print('\033[1;32m     ##################   播放功能加载成功！  ################### \033[0m')
		except:
			err = logs.err()
			print('\033[1;31m     ############  播放功能加载失败！请检查声卡驱动 ############# \033[0m')
			exit()
		try:
			model = sys.argv[1]
			print('\033[1;32m     ##############   snowboy唤醒模型加载成功！  ################ \033[0m')
		except:
			err = logs.err()
			print('\033[1;31m     #########   snowboy唤醒模型加载失败！请检查模型  ########### \033[0m')
			exit()
			
		detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
		print('\033[1;35m     ##############   唤醒监听开始，Ctrl+C即可结束...   #########\n \033[0m')
		
		while 1:	
			detector.start(detected_callback=lambda: main.main(p,detector),sleep_time=0.03)
	except KeyboardInterrupt:
		print('\n———————————————————————————————————————————————————————————————————————————————————————')
		print('\n     用户自主终止，唤醒监听结束！')
	except:
		print('\n———————————————————————————————————————————————————————————————————————————————————————\n')
		print('\033[1;31m程序似乎有bug诶..... \n \033[0m')
		err = logs.err()
		print(err)
		print('\n     更多信息请查阅logs/error.log')
		print('\n———————————————————————————————————————————————————————————————————————————————————————\n')
	finally:
		p.terminate()
		print('\n \033[1;35m     PyAudio已关闭！ \033[0m')
		detector.terminate()
		print('\n \033[1;35m     snowboy模块已关闭！ \033[0m')
		print('\n \033[1;34m     程序主循环退出! \033[0m \n')