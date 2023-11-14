#include "main.h"
#include "usb_device.h"
#include "json.h"

#define VIRTUAL_COM_PORT_DATA_SIZE 64

#define RXBUFSIZE 256
#define TXBUFSIZE 256
#define min(a, b) ((a < b) ? (a) : (b))

uint8_t rxbuf[RXBUFSIZE];
uint8_t txbuf[TXBUFSIZE];
uint32_t rxbufrdptr = 0;
uint32_t rxbufwrptr = 0;
char usbrxbuf[TXBUFSIZE];
char *usbwrptr = &usbrxbuf[0];


extern "C" void USB_CDC_ReceiveCallback(uint8_t *Receive_Buffer, uint32_t Receive_length) {
  for (uint32_t i = 0; i < Receive_length; i++) {
    rxbuf[rxbufwrptr % RXBUFSIZE] = Receive_Buffer[i];
    rxbufwrptr++;
  }
}

extern "C" uint8_t CDC_Transmit_FS(uint8_t *Buf, uint16_t Len);

// TODO move to json and make it better
extern "C" void USB_TransmitString(const char *msg) {
  uint32_t tosend = strlen(msg);
  uint8_t *cptr = (uint8_t *)msg;
  uint32_t maxsize = VIRTUAL_COM_PORT_DATA_SIZE - 1;
  while (tosend) {
    int chunklen = min(maxsize, tosend);
    // if data not sent yet, it returns USBD_BUSY
    while (CDC_Transmit_FS(cptr, chunklen) == USBD_BUSY)
      ;
    cptr += chunklen;
    tosend -= chunklen;
  }
}


uint8_t parseCmd(char *rxbuf) { return process_json(rxbuf); }

void usb_loop() {
  for (; rxbufrdptr < rxbufwrptr; rxbufrdptr++) {
    *usbwrptr = rxbuf[rxbufrdptr % RXBUFSIZE];
    if (*usbwrptr == '\n')
      continue;
    if (*usbwrptr == '\r') {
      *usbwrptr = 0;
      if (!parseCmd(usbrxbuf))
        USB_TransmitString("error");
      usbwrptr = &usbrxbuf[0];
    } else {
      usbwrptr++;
      if ((int)usbwrptr - (int)&usbrxbuf > (int)sizeof(usbrxbuf) - 2) {
        memset(usbrxbuf, 0, sizeof(usbrxbuf));
        usbwrptr = &usbrxbuf[0];
        USB_TransmitString("error");
      }
    }
  }
}