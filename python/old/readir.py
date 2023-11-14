import sys
import usb.core
import usb.util
import usb # 1.0 not 0.4
from time import sleep

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


    request_type = usb.util.build_request_type(usb.util.CTRL_IN,
                                               usb.util.CTRL_TYPE_CLASS,
                                               usb.util.CTRL_RECIPIENT_DEVICE)
 
    USBRQ_HID_GET_REPORT = 0x01
    USBRQ_HID_SET_REPORT = 0x09
    USB_HID_REPORT_TYPE_FEATURE = 0x03

    lastcount=0
    
    try:
        while True:
            response = device.ctrl_transfer(request_type,
                                            USBRQ_HID_GET_REPORT,
                                            (USB_HID_REPORT_TYPE_FEATURE << 8) | 0,
                                            0, # ignored
                                            128) # length

            code=response[0]
            count=response[1]+response[2] << 8;
            
            if lastcount != count:
                print "last read ir-code: 0x%02x (count %d)" % ( response[0], response[1] )
                lastcount=count
            sleep(1)
    except KeyboardInterrupt:
        print
        print "ctrl-c pressed. exiting"
    
    print
    sys.exit(0)
