import android
import time

droid = android.Android()

droid.startLocating()
droid.dialogCreateSpinnerProgress("GPS", "Initiating GPS")
droid.dialogShow()
time.sleep(20)
droid.dialogDismiss()

droid.startTrackingSignalStrengths()
droid.dialogCreateSpinnerProgress("Signal Strength", "Initiating Signal Strength Tracking")
droid.dialogShow()
time.sleep(20)
droid.dialogDismiss()


salir = False
warning = False
mode = "GPS"
print "  LATITUDE     |   LONGITUDE   | GSM STRENGTH | MODE" 
while salir == False:

	loc = droid.readLocation().result
	signal = droid.readSignalStrengths()

	
	if loc == {}:
		if warning == False:
			droid.makeToast('Impossible to find the position. \n  Showing the last known location.')
			warning = True
		mode = "LAST"
		loc = getLastKnownLocation().result
	if loc != {}:
		try:
			n = loc['gps']
			mode = "GPS"
		except KeyError:
			if warning == False:
				droid.makeToast('Impossible to find the GPS coordinates. \n Showing the coordinates of the nearest cell.')
				warning = True
			n = loc['network']
			mode = "NET"
		

	la = n['latitude'] 
	lo = n['longitude']
	force = signal[1]['gsm_signal_strength']

	
	print str(la) + " | " + str(lo) + " | " + str(force) + " | " + mode

	fh = open( '/sdcard/strength_Track.csv' ,'a') 
	outstr = str(la) + "," + str(lo) + "," + str(force) + "," + mode + "," + time.strftime("%H:%M:%S") + ","+ time.strftime("%d-%m-%Y") + "\n" 
	fh.write(outstr)
	fh.close() 
	time.sleep(10)

droid.stopLocating()
droid.stopTrackingSignalStrengths()

