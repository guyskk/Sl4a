import android
import datetime
import os

droid = android.Android()

#Get The Messages
sms_received = droid.smsGetMessages(False,'inbox').result
sms_sent = droid.smsGetMessages(False,'sent').result
#sms_list.extend(droid.smsGetMessages(False,'sent').result)

#Remove Old Backup
os.remove('/sdcard/Backup_sms.html')

#Create and open new file
fh = open( '/sdcard/Backup_sms.html' ,'a')

print "SMS LIST:"

fh.write("<html>\n<head>\n<title>SMS Backup</title>\n</head>\n<body>\n<table border=1><td><b> From: </b></td><td><b> To: </b></td><td><b> Date: </b></td><td><b> Text: </b></td><tr>\n")

for message in sms_received:
	text = message['body']
	text = text.encode('ascii','replace')
	number = message['address']
	date_raw = datetime.datetime.fromtimestamp(int(message['date'])/1000)
	date = date_raw.strftime("%m/%d/%y %H:%M:%S")

	print "From: "+ number +" at: "+ date
	print "  -> "+ text

	outstr = "<td> "+ number +" </td><td> Me </td><td> "+ date +" </td><td> "+ text +" </td><tr>\n"
	fh.write(outstr)

for message in sms_sent:
	text = unicode(message['body'])
	text = text.encode('ascii','replace')
	number = message['address']
	date_raw = datetime.datetime.fromtimestamp(int(message['date'])/1000)
	date = date_raw.strftime("%m/%d/%y %H:%M:%S")

	print "To: "+ number +" at: "+ date
	print "  -> "+ text

	outstr = "<td> Me </td><td> "+ number +" </td><td> "+ date +" </td><td> "+ text +" </td><tr>\n"
	fh.write(outstr)

fh.write("</table>\n</body>")
fh.close()

droid.webViewShow('file:///sdcard/Backup_sms.html')