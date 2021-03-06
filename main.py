# coding=utf-8
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

import datetime
import os
import time
import serial.tools.list_ports
from batch_page import BatchPage
from single_page import SinglePage
from record_page import RecordPage
from constant import AppConfig
from linptech.serial_communicator import LinptechSerial
import logging
import tkinter.font as tkFont

logging.getLogger().setLevel(logging.DEBUG)
class App(tk.Tk):

	def __init__(self):
		super().__init__()
		self.geometry(AppConfig.WINDOWS_SZIE.value)  
		# self.iconbitmap(default="kankan_01.ico")
		self.wm_title(AppConfig.TITLE.value)

		# default_font = tkFont.nametofont("TkDefaultFont")
		# default_font.configure(size=18)
		# self.option_add("*Font", default_font)

		# 多页面table设置
		table = ttk.Notebook(self)
		table.pack(expand=1, fill="both",side="top")
		self.record_page=RecordPage(table,self)
		table.add(self.record_page,text="生产记录")
		self.single_page = SinglePage(table,self)
		table.add(self.single_page,text="单个调试")
		self.batch_page = BatchPage(table,self)
		table.add(self.batch_page,text="批量调试")
		
		# 串口设置
		port=self.getPortList()[0]
		self.ser=LinptechSerial(port,receive=self.receive)
		self.ser.setDaemon(True)
		self.ser.start()
	
	def getPortList(self):
		portList = list(serial.tools.list_ports.comports())
		portNameList = []
		for port in portList:
			portNameList.append(str(port[0]))
		logging.debug("portNameList=%s",portNameList)
		return portNameList
	
	def send(self,data):
		self.ser.send(data)
	
	def receive(self,data,optional):
		logging.debug('data=%s,optional=%s' % (data,optional))
		if self.record_page.is_listen.get():
			self.record_page.listen(data,optional)
		if self.single_page.is_listen.get():
			self.single_page.listen(data,optional)


if __name__ == '__main__':
	app = App()
	def closeWindow():
		app.destroy()
	app.protocol('WM_DELETE_WINDOW', closeWindow) 
	app.mainloop()