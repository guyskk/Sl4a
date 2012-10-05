import android
import time

 
def gps_alert():
	gps_switch = False
	title = 'GPS Alert'
	message = ('Impossible to find GPS Coordinates. Do you want to wait or could I start tracking by aproximation?')
	droid.dialogCreateAlert(title, message)
	droid.dialogSetPositiveButtonText('Start logging')
	droid.dialogSetNegativeButtonText('Wait for GPS')
	droid.dialogShow()
	response=droid.dialogGetResponse().result
	droid.dialogDismiss()
	if response.has_key("which"):   
		result=response["which"]   
		if result=="positive":     
			gps_switch = False
		elif result=="negative":     
			gps_switch = True
			droid.makeToast("Waiting for valid GPS Signal")
	return gps_switch 

droid = android.Android()

droid.startLocating()
droid.dialogCreateSpinnerProgress("GPS", "Initiating GPS")
droid.dialogShow()
time.sleep(10)
droid.dialogDismiss()

droid.startTrackingSignalStrengths()
droid.dialogCreateSpinnerProgress("Signal Strength", "Initiating Signal Strength Tracking")
droid.dialogShow()
time.sleep(5)
droid.dialogDismiss()


salir = False
warning = False
use_only_gps = False
mode = "GPS"
print "  LATITUDE     |   LONGITUDE   | GSM STRENGTH | MODE" 
while salir == False:

	loc = droid.readLocation().result
	signal = droid.readSignalStrengths()

	
	if loc == {}:
		if warning == False:
			#droid.makeToast('Impossible to find the position. \n  Showing the last known location.')
			use_only_gps = gps_alert()
			warning = True
		mode = "LAST"
		loc = getLastKnownLocation().result
	if loc != {}:
		try:
			n = loc['gps']
			mode = "GPS"
		except KeyError:
			if warning == False:
				#droid.makeToast('Impossible to find the GPS coordinates. \n Showing the coordinates of the nearest cell.')
				use_only_gps = gps_alert()
				warning = True
			n = loc['network']
			mode = "NET"
		

	la = n['latitude'] 
	lo = n['longitude']
	force = signal[1]['gsm_signal_strength']
	if use_only_gps == True:
		if mode == "GPS":
			print str(la) + " | " + str(lo) + " | " + str(force) + " | " + mode

			fh = open( '/sdcard/strength_Track.csv' ,'a') 
			outstr = str(la) + "," + str(lo) + "," + str(force) + "," + mode + "," + time.strftime("%H:%M:%S") + ","+ time.strftime("%d-%m-%Y") + "\n" 
			fh.write(outstr)
			fh.close() 
			time.sleep(10)
	else:
		print str(la) + " | " + str(lo) + " | " + str(force) + " | " + mode

		fh = open( '/sdcard/strength_Track.csv' ,'a') 
		outstr = str(la) + "," + str(lo) + "," + str(force) + "," + mode + "," + time.strftime("%H:%M:%S") + ","+ time.strftime("%d-%m-%Y") + "\n" 
		fh.write(outstr)
		fh.close() 
		time.sleep(10)	

droid.stopLocating()
droid.stopTrackingSignalStrengths()

