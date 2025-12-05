#include "dht11.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "DHT11";

// parámetros
#define TIMEOUT_RESPONSE_US 200
#define TIMEOUT_PULSE_US    100
#define START_LOW_MS        20
#define START_PULLUP_US     40

int dht11_read(gpio_num_t pin, int *temperature, int *humidity)
{
    uint8_t data[5] = {0};

    // iniciar señal LOW por >=18 ms
    gpio_set_direction(pin, GPIO_MODE_OUTPUT);
    gpio_set_level(pin, 0);
    vTaskDelay(pdMS_TO_TICKS(START_LOW_MS));

    gpio_set_level(pin, 1);
    esp_rom_delay_us(START_PULLUP_US);
    gpio_set_direction(pin, GPIO_MODE_INPUT);

    int64_t start;

    // esperar respuesta LOW
    start = esp_timer_get_time();
    while (gpio_get_level(pin) == 1) {
        if (esp_timer_get_time() - start > TIMEOUT_RESPONSE_US)
            return -1;
    }

    // esperar HIGH
    start = esp_timer_get_time();
    while (gpio_get_level(pin) == 0) {
        if (esp_timer_get_time() - start > TIMEOUT_RESPONSE_US)
            return -1;
    }

    // leer 40 bits
    for (int i = 0; i < 40; i++) {

        // esperar LOW inicial
        start = esp_timer_get_time();
        while (gpio_get_level(pin) == 1) {
            if (esp_timer_get_time() - start > TIMEOUT_PULSE_US)
                return -1;
        }

        // esperar HIGH (inicio del bit)
        start = esp_timer_get_time();
        while (gpio_get_level(pin) == 0) {
            if (esp_timer_get_time() - start > TIMEOUT_PULSE_US)
                return -1;
        }

        int64_t t0 = esp_timer_get_time();
        while (gpio_get_level(pin) == 1) {
            if ((esp_timer_get_time() - t0) > 200)
                break;
        }
        int pulse_len = (int)(esp_timer_get_time() - t0);

        int bit = (pulse_len > 50) ? 1 : 0;
        data[i / 8] = (data[i / 8] << 1) | bit;
    }

    uint8_t checksum = (data[0] + data[1] + data[2] + data[3]) & 0xFF;

    if (checksum != data[4])
        return -2;

    *humidity = data[0];
    *temperature = data[2];
    return 0;
}
