import android
import datetime
import os


def writeToHtml(string):
	fh = open( '/sdcard/Backup_sms.html' ,'a')
	fh.write(string)
	fh.close

droid = android.Android()

sms_received = droid.smsGetMessages(False,'inbox').result
sms_sent = droid.smsGetMessages(False,'sent').result
#sms_list.extend(droid.smsGetMessages(False,'sent').result)

os.remove('/sdcard/Backup_sms.html')

print "SMS LIST:"

writeToHtml("<html>\n<head>\n<title>SMS Backup</title>\n</head>\n<body>\n<table border=1><td><b> From: </b></td><td><b> To: </b></td><td><b> Date: </b></td><td><b> Text: </b></td><tr>\n")

for message in sms_received:
	text = message['body']
	number = message['address']
	date_raw = datetime.datetime.fromtimestamp(int(message['date'])/1000)
	date = date_raw.strftime("%m/%d/%y %H:%M:%S")

	print "From: "+ number +" at: "+ date
	print "Text: "+ text
	print "---"

	outstr = "<td> "+ number +" </td><td> Me </td><td> "+ date +" </td><td> "+ text +" </td><tr>\n"
	writeToHtml(outstr)

for message in sms_sent:
	text = message['body']
	number = message['address']
	date_raw = datetime.datetime.fromtimestamp(int(message['date'])/1000)
	date = date_raw.strftime("%m/%d/%y %H:%M:%S")

	print "To: "+ number +" at: "+ date
	print "Text: "+ text
	print "---"

	outstr = "<td> Me </td><td> "+ number +" </td><td> "+ date +" </td><td> "+ text +" </td><tr>\n"
	writeToHtml(outstr)

writeToHtml("</table>\n</body>")

droid.webViewShow('file:///sdcard/Backup_sms.html')