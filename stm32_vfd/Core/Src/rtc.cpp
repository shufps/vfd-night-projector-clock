#include "main.h"

#include "rtc.h"

extern RTC_HandleTypeDef hrtc;

uint8_t init_rtc() {
  RTC_DateTypeDef sdatestructure;
  RTC_TimeTypeDef stimestructure;

  sdatestructure.Year = 0x14;
  sdatestructure.Month = RTC_MONTH_APRIL;
  sdatestructure.Date = 0x14;
  sdatestructure.WeekDay = RTC_WEEKDAY_MONDAY;

  if (HAL_RTC_SetDate(&hrtc, &sdatestructure, RTC_FORMAT_BIN) != HAL_OK) {
    /* Initialization Error */
    Error_Handler();
  }

  stimestructure.Hours = 0x08;
  stimestructure.Minutes = 0x10;
  stimestructure.Seconds = 0x00;
  stimestructure.TimeFormat = RTC_HOURFORMAT12_AM;
  stimestructure.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
  stimestructure.StoreOperation = RTC_STOREOPERATION_RESET;

  if (HAL_RTC_SetTime(&hrtc, &stimestructure, RTC_FORMAT_BIN) != HAL_OK) {
    /* Initialization Error */
    Error_Handler();
  }

  return 1;
}

void get_rtc(RTC_DateTypeDef *sdatestructureget,
             RTC_TimeTypeDef *stimestructureget) {

  /* Get the RTC current Time */
  HAL_RTC_GetTime(&hrtc, stimestructureget, RTC_FORMAT_BIN);
  /* Get the RTC current Date */
  HAL_RTC_GetDate(&hrtc, sdatestructureget, RTC_FORMAT_BIN);
#if 0
#ifdef DISPLAY_ON_DUBUGGER
  /* Display time Format : hh:mm:ss */
  sprintf((char*)aShowTime,"%.2d:%.2d:%.2d", stimestructureget.Hours, stimestructureget.Minutes, stimestructureget.Seconds);
  /* Display date Format : mm-dd-yy */
  sprintf((char*)aShowDate,"%.2d-%.2d-%.2d", sdatestructureget.Month, sdatestructureget.Date, 2000 + sdatestructureget.Year);
#endif
#endif
}

uint8_t set_rtc(RTC_DateTypeDef *sdatestructure,
                RTC_TimeTypeDef *stimestructure) {

  __HAL_RTC_WRITEPROTECTION_DISABLE(&hrtc);
  if (HAL_RTC_SetDate(&hrtc, sdatestructure, RTC_FORMAT_BIN) != HAL_OK) {
    return 0;
  }

  if (HAL_RTC_SetTime(&hrtc, stimestructure, RTC_FORMAT_BIN) != HAL_OK) {
    return 0;
  }
  return 1;
}
