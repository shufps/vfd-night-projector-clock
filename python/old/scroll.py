import sys
import usb.core
import usb.util
import usb # 1.0 not 0.4
from time import sleep

USBRQ_HID_GET_REPORT = 0x01
USBRQ_HID_SET_REPORT = 0x09
USB_HID_REPORT_TYPE_FEATURE = 0x03
    
    
# sends data to the usb device
def sendToDevice(dev, data):
# build request for sending to usb    
    request_type = usb.util.build_request_type(usb.util.CTRL_OUT,
                                               usb.util.CTRL_TYPE_CLASS,
                                               usb.util.CTRL_RECIPIENT_DEVICE)
    
   
# zero pad data to 128    
    for i in range(0, 128-len(data)):
        data.append(0)
 
 # send to device
    device.ctrl_transfer(   request_type,
                            USBRQ_HID_SET_REPORT,
                            (USB_HID_REPORT_TYPE_FEATURE << 8) | 0,
                            0, data) 
    
    
    
    
def getStringDescriptor(device, index):
    """
    """
    response = device.ctrl_transfer(usb.util.ENDPOINT_IN,
                                    usb.legacy.REQ_GET_DESCRIPTOR,
                                    (usb.util.DESC_TYPE_STRING << 8) | index,
                                    0, # language id
                                    255) # length

    return response[2:].tostring().decode('utf-16')




if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "usage: "+sys.argv[0]+" msg"
        sys.exit(1)
        
        
    device = usb.core.find(idVendor=0x16c0, idProduct=0x05df)

    if not device:
        raise Exception("Device not found")

    print "0x%04x 0x%04x %s %s" % (device.idVendor, device.idProduct,
                             getStringDescriptor(device, device.iProduct),
                             getStringDescriptor(device, device.iManufacturer))

# define patterns for raw segment data
    pattern = {
        'a':'---.---.','b':'..-----.','c':'-..---..','d':'.----.-.',
        'e':'-..----.','f':'-...---.','g':'----.--.','h':'.--.---.',
        'i':'....--..','j':'.----...','k':'.--.---.','l':'...---..',
        'm':'-.-.-...','n':'..-.-.-.','o':'------..','p':'--..---.',
        'q':'---..--.','r':'....-.-.','s':'-.--.--.','t':'...----.', 
        'u':'.-----..','v':'..---...','w':'.-.-.-..','x':'.--.---.',
        'y':'.---.--.','z':'--.--.-.','0':'------..','1':'.--.....',
        '2':'--.--.-.','3':'----..-.','4':'.--..--.','5':'-.--.--.',
        '6':'-.-----.','7':'---.....','8':'-------.', 
        '9':'------..','.':'.......-'
    }

    msg=sys.argv[1].lower()
    rawdata=[]
    
# for each character in msg calculate the numerical value    
    for c in msg:
        if c in pattern:
            pat = pattern[c].replace('-','1').replace('.','0')[::-1]
            rawdata.append(eval("0b"+pat))
        else:
            print c+" not found. skipping"
    
    count=len(rawdata)


# scroll data    
    for i in range(-8,count+1):
# prepare data for displaying raw segment data
# command 0x02 (set clock mode) with param 0x01 (display raw segment data)
        data=[  0x00,0x00,0x00,0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00,
                0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        for j in range(0, 8):
            index=i+j
            if index >= 0 and index < count:
                data.append(rawdata[index])
            else:
                data.append(0x00)
	
        sendToDevice(device, data)
        sleep(0.25)

# switch back to time display; command 0x02 with mode 0x00 (time display)
    sendToDevice(device, [0x00, 0x00, 0x00, 0x02, 0x00])
        
    sys.exit(0)

