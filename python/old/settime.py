import sys
import usb.core
import usb.util
import usb # 1.0 not 0.4
import datetime

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
       
    device = usb.core.find(idVendor=0x16c0, idProduct=0x05df)

    if not device:
        raise Exception("Device not found")

    print "0x%04x 0x%04x %s %s" % (device.idVendor, device.idProduct,
                             getStringDescriptor(device, device.iProduct),
                             getStringDescriptor(device, device.iManufacturer))

   

    request_type = usb.util.build_request_type(usb.util.CTRL_OUT,
                                               usb.util.CTRL_TYPE_CLASS,
                                               usb.util.CTRL_RECIPIENT_DEVICE)
    
    now = datetime.datetime.now()
    
    # command 0x01 set time followed by hours, minutes, seconds
    sendToDevice(device, [0x00, 0x00, 0x00, 0x01, now.hour, now.minute, now.second])
       
    sys.exit(0)
