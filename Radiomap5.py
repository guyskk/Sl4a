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

def write_to_csv(string):

    fh = open( '/sdcard/strength_Track.csv' ,'a') 
    fh.write(string)
    fh.close()

# Python interface to Android provided by SL4A.

import android
import time
droid = android.Android()

# Open the WebView GUI written in HTML/JavaScript.
droid.webViewShow('file:///sdcard/sl4a/scripts/Radiomap5.html')

#Start Services

droid.startLocating()
droid.startTrackingSignalStrengths()
droid.dialogCreateSpinnerProgress("Starting...", "Starting GPS Location \nInitiating Signal Strength Logging")
droid.dialogShow()
time.sleep(20)
droid.dialogDismiss()

# Define menu items 'About' and 'Quit', with events 'menu-about' and 'menu-quit'.
droid.addOptionsMenuItem('About','menu-about',None,"ic_menu_info_details")
droid.addOptionsMenuItem('Quit','menu-quit',None,"ic_lock_power_off")



salir = False
warning = False
use_only_gps = False
mode = "GPS"
result = "Initiating ..."
timer = 0
# Loop waiting for events.
while True:
    loc = droid.readLocation().result
    signal = droid.readSignalStrengths()
    
    if loc == {}:
        if warning == False:
            
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
                
                use_only_gps = gps_alert()
                warning = True
            n = loc['network']
            mode = "NET"
        
    la = n['latitude'] 
    lo = n['longitude']
    force = signal[1]['gsm_signal_strength']

    if use_only_gps == True and mode == "GPS" and timer == 10:

        result += "\nLat: "+ str(la) + "Lon: " + str(lo) + "Strength: " + str(force) + "Mode: " + mode
        # Send the event 'calculation-result' with the calculated result text to the webview.
        droid.eventPost('calculation-result',result)
        outstr = str(la) + "," + str(lo) + "," + str(force) + "," + mode + "," + time.strftime("%H:%M:%S") + ","+ time.strftime("%d-%m-%Y") + "\n" 
        write_to_csv(outstr)

    if use_only_gps == False and timer == 10:
        
        result += "\nLat: "+ str(la) + "Lon: " + str(lo) + "Strength: " + str(force) + "Mode: " + mode
        # Send the event 'calculation-result' with the calculated result text to the webview.
        droid.eventPost('calculation-result',result)
        outstr = str(la) + "," + str(lo) + "," + str(force) + "," + mode + "," + time.strftime("%H:%M:%S") + ","+ time.strftime("%d-%m-%Y") + "\n" 
        write_to_csv(outstr) 

    # Wait for an event.
    eventResult = droid.eventWait(10000).result
    if eventResult == None:
        continue
    # If 'menu-about' event happens, then a about dialog is shown using Python SL4A UIFacade.
    elif eventResult["name"] == "menu-about":
        droid.dialogCreateAlert('About Signal GeoLogging', 
            'Signal GeoLogging is a tool designed for the creation of coverage maps. \n' + \
            'It is based on the SL4A + Python plattform. \n' + \
            'Written by Sergio Maeso.\n(Universidad Carlos III , Madrid)\n'+ \
            'LGPLv3 (C) 2012 Sergio Maeso J.')
        droid.dialogSetNeutralButtonText('Ok')
        droid.dialogShow()
        droid.dialogGetResponse().result
        droid.dialogDismiss()
    # If 'menu-quit' event happens, then the program is closed.
    elif eventResult["name"] == "menu-quit":
        break
        droid.stopLocating()
        droid.stopTrackingSignalStrengths()

    time.sleep(0.1)
    timer = timer + 1
    if timer == 11:
        timer =0
