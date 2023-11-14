/*
 * json.cpp
 *
 *  Created on: 03.09.2017
 *      Author: thomas
 */

#include <stdarg.h>
#include <stdio.h>

#include "ArduinoJson.h"
#include "main.h"

#include "json.h"
#include "rtc.h"

extern "C" void USB_TransmitString(char *msg);

// uint8_t buffer[PAGE_SIZE + 2];
// char buffer_base64[PAGE_SIZE_BASE64+2];

extern char txbuf[256];
static int txwrptr;

control_t control;

void add(const char *format, ...) {
  va_list args;
  va_start(args, format);
  int written =
      vsnprintf(&txbuf[txwrptr], sizeof(txbuf) - txwrptr, format, args);
  if (written < (int)sizeof(txbuf) - txwrptr && written > 0)
    txwrptr += written;
  va_end(args);
}

#define ERR_NONE 0
#define ERR_ID_MISSING 1
#define ERR_UNKNOWN_COMMAND 2
#define ERR_JSON_DECODING_FAILED 3
#define ERR_MISSING_PARAMS 4
#define ERR_INVALID_DATE_TIME 5

const char *error_string(int code) {
  switch (code) {
  case ERR_NONE:
    return (const char *)"ok";
    break;
  case ERR_ID_MISSING:
    return (const char *)"id missing";
    break;
  case ERR_UNKNOWN_COMMAND:
    return (const char *)"unknown command";
    break;
  case ERR_JSON_DECODING_FAILED:
    return (const char *)"json decoding failed";
    break;
  case ERR_MISSING_PARAMS:
    return (const char *)"missing params";
    break;
  case ERR_INVALID_DATE_TIME:
    return (const char *)"invalid date or time";
    break;
  default:
    return (const char *)"unknown error";
  }
}

void send_error(int error) {}

uint8_t process_json(char *rxbuf) {
  StaticJsonBuffer<512> jsonIn;

  JsonObject &root = jsonIn.parseObject(rxbuf);

  txwrptr = 0;
  memset(txbuf, 0, sizeof(txbuf));
  int error = ERR_NONE;
  do {
    add("{");
    add("\"jsonrpc\":\"2.0\",");

    if (!root.success()) {
      error = ERR_JSON_DECODING_FAILED;
      break;
    }

    if (!root.containsKey("id")) {
      error = ERR_ID_MISSING;
      break;
    }

    add("\"id\":\"");
    add(root["id"]);
    add("\",");

    do {
      if (root["method"] == "status") {
        add("\"result\":\"ok\"");
        error = ERR_NONE;
        break;
      }

      if (root["method"] == "get") {
        RTC_DateTypeDef date;
        RTC_TimeTypeDef time;
        get_rtc(&date, &time);
        add("\"result\":{\"year\":%d,\"month\":%d,\"day\":%d,\"hours\":%d,"
            "\"minutes\":%d,\"seconds\":%d}",
            date.Year + 2000, date.Month, date.Date, time.Hours, time.Minutes,
            time.Seconds);
        error = ERR_NONE;
        break;
      }
      if (root["method"] == "control") {
        if (!root.containsKey("params")) {
          error = ERR_MISSING_PARAMS;
          break;
        }
        auto params = root["params"];
        control.state = params["state"]; // 0 = off, 1 = on
        control.hour_on = params["hour-on"];
        control.minute_on = params["minute-on"];
        control.hour_off = params["hour-off"];
        control.minute_off = params["minute-off"];
        add("\"result\":\"ok\"");
        error = ERR_NONE;
        break;
      }
      if (root["method"] == "set") {
        if (!root.containsKey("params")) {
          error = ERR_MISSING_PARAMS;
          break;
        }
        RTC_DateTypeDef sdate;
        RTC_TimeTypeDef stime;
        get_rtc(&sdate, &stime);

        auto params = root["params"];

        int year = params["year"];
        int month = params["month"];
        int date = params["date"];
        int hours = params["hours"];
        int minutes = params["minutes"];
        int seconds = params["seconds"];

        sdate.Year = year - 2000;
        sdate.Month = month;
        sdate.Date = date;

        stime.Hours = hours;
        stime.Minutes = minutes;
        stime.Seconds = seconds;
        stime.TimeFormat = RTC_HOURFORMAT12_AM;
        stime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
        stime.StoreOperation = RTC_STOREOPERATION_RESET;

        if (set_rtc(&sdate, &stime)) {
          add("\"result\":\"ok\"");
          error = ERR_NONE;
        } else {
          error = ERR_INVALID_DATE_TIME;
          break;
        }
        break;
      }

      error = ERR_UNKNOWN_COMMAND;
    } while (0);

  } while (0);
  if (error != ERR_NONE) {
    add("\"error\":\"");
    add(error_string(error));
    add("\"");
  }
  add("}\r\n");
  USB_TransmitString(txbuf);

  return 1;
}

uint8_t process_json_c(char *rxbuf) { return process_json(rxbuf); }