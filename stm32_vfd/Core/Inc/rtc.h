#pragma once

#include "main.h"

uint8_t init_rtc();

void get_rtc(RTC_DateTypeDef *sdatestructureget,
             RTC_TimeTypeDef *stimestructureget);

uint8_t set_rtc(RTC_DateTypeDef *sdatestructure,
                RTC_TimeTypeDef *stimestructure);