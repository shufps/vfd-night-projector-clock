/*
 * json.h
 *
 *  Created on: 03.09.2017
 *      Author: thomas
 */

#ifndef JSON_H_
#define JSON_H_

#include <stdint.h>

typedef struct {
    int state;
    int hour_on;
    int minute_on;
    int hour_off;
    int minute_off;
} control_t;

uint8_t process_json_c(char* rxbuf);
uint8_t process_json(char* rxbuf);



#endif /* JSON_H_ */