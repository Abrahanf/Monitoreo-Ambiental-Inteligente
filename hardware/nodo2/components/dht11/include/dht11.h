#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include "driver/gpio.h"

/**
 * @brief Lee el DHT11
 * 
 * @param pin          GPIO del sensor
 * @param temperature  (salida) temperatura en °C
 * @param humidity     (salida) humedad en %
 * 
 * @return 0 si OK
 *        -1 si timeout o mala respuesta
 *        -2 si checksum inválido
 */
int dht11_read(gpio_num_t pin, int *temperature, int *humidity);

#ifdef __cplusplus
}
#endif
