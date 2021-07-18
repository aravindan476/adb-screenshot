import os
from datetime import datetime 
from datetime import date
import time

def devices_connected():
	os.system("adb devices>devices_list.txt")
	device_ls = open("devices_list.txt","r")
	deviceList = device_ls.readlines()
	device_ls.close()
	os.system("rm devices_list.txt")
	print(deviceList)
	global deviceDSN
	deviceDSN = []
	for device in deviceList:
		deviceDSN.append(device.split('\t')[0])
	del deviceDSN[0] # list of devices attached element
	del deviceDSN[-1] # last \n element

	#print(deviceDSN)		
	#Headless Check
	
	length=len(deviceDSN)
	if length==0:
		print ("No Head devices attached")
	elif length==1:
		os.system("adb shell ls system/bin/screencap>headless_check.txt")
		headlessck = open("headless_check.txt","r")
		headless_chck = headlessck.readlines()
		headlessck.close()
		os.system("rm headless_check.txt")
		#print(headless_chck)
		if "No" in headless_chck[0]:
			deviceDSN.remove(deviceDSN[0])
	elif length>1:
		for t in range(0,length-1):
			os.system("adb -s "+deviceDSN[t]+" shell ls system/bin/screencap>headless_check.txt")
			headlessck = open("headless_check.txt","r")
			headless_chck = headlessck.readlines()
			headlessck.close()
			os.system("rm headless_check.txt")
			#print(headless_chck)
			if "No" in headless_chck[0]:
				deviceDSN.remove(deviceDSN[t])

def screen_shot_connected():
	devices_connected()
	if (len(deviceDSN)==0):
		print ("No Head devices attached")
	elif (len(deviceDSN)==1):
		screen_shot_dsn(0)
	elif (len(deviceDSN)>1):
		print("You have connected some devices.Pls select the one to take screenshot..")
		for x in range(0,len(deviceDSN)):
			print(deviceDSN[x]+"     "+str(x+1))
		usersel="wrong"
		while usersel not in range(0,len(deviceDSN)):	
			usersel=int(input("Enter the selection :"))-1
		screen_shot_dsn(usersel)
	
	
def get_filename(i):
	os.system("adb -s "+deviceDSN[i]+" shell getprop ro.product.device>device_name.txt")
	deviceName = open("device_name.txt","r")
	device_name = deviceName.readlines()
	deviceName.close()
	os.system("rm device_name.txt")
	print(deviceDSN[i])
	now = datetime.now()
	current_time = now.strftime("%H%M%S")
	today = date.today()
	date_today=today.strftime("%b%d")
	filename=device_name[0][:-1]+"_"+deviceDSN[i]+"_"+date_today+"_"+current_time
	return filename

def screen_shot_dsn(i):
	file_name=get_filename(i)
	os.system("adb -s "+deviceDSN[i]+" shell screencap /sdcard/Scrshot_"+file_name+".png")
	os.system("adb -s "+deviceDSN[i]+" pull /sdcard/Scrshot_"+file_name+".png")


screen_shot_connected()
