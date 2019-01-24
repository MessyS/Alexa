

### Alexa——定制化自己的智能家居控制中心
>所需环境

* swig3.0(pip)
* sox pyaudio libatlas-base-dev(apt)

>支持的语言引擎

* 讯飞
	* 语音识别
	* 语音合成
* 百度
	* 语音识别
	* 语音合成（目前合成的音频播放有点问题，会尽快修复）

**注：**
* 启动命令：`python3 alexa.py music_messy/model/alea.umdl`
* 如需把程序加到自启文件,需手动把`func_messy`目录下py文件里的所有音频文件的路径改为绝对路径

若有兴趣获知我是如何开发的：详细教程位于[CSDN -- Messy的小博客~~~](https://blog.csdn.net/qq_41082014/article/details/86568114)
