// main/dht11_fixed.c
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_timer.h"

static const char *TAG = "DHT11";
#define DHT_PIN GPIO_NUM_4

// timeouts (microsegundos)
#define TIMEOUT_RESPONSE_US 200   // espera la respuesta inicial del sensor
#define TIMEOUT_PULSE_US    100   // espera cada transición dentro de un bit
#define START_LOW_MS        20    // pull-down >= 18 ms
#define START_PULLUP_US     40    // pull-up ~20-40 us

// lee 40 bits y devuelve 0 si OK, -1 si timeout/respuesta, -2 si checksum
static int dht_read_data(int *temperature, int *humidity)
{
    uint8_t data[5] = {0};

    // 1) Iniciar secuencia: pull low >=18ms
    gpio_set_direction(DHT_PIN, GPIO_MODE_OUTPUT);
    gpio_set_level(DHT_PIN, 0);
    vTaskDelay(pdMS_TO_TICKS(START_LOW_MS));

    // pull-up 20-40us y pasar a entrada
    gpio_set_level(DHT_PIN, 1);
    esp_rom_delay_us(START_PULLUP_US);
    gpio_set_direction(DHT_PIN, GPIO_MODE_INPUT);

    // 2) Esperar respuesta: sensor debe tirar linea a LOW (~80us), luego HIGH (~80us)
    int64_t start = esp_timer_get_time();
    // esperar LOW
    while (gpio_get_level(DHT_PIN) == 1) {
        if ((esp_timer_get_time() - start) > TIMEOUT_RESPONSE_US) {
            ESP_LOGW(TAG, "Timeout esperando respuesta LOW");
            return -1;
        }
    }
    // esperar HIGH
    start = esp_timer_get_time();
    while (gpio_get_level(DHT_PIN) == 0) {
        if ((esp_timer_get_time() - start) > TIMEOUT_RESPONSE_US) {
            ESP_LOGW(TAG, "Timeout esperando respuesta HIGH");
            return -1;
        }
    }
    // ahora la transmisión de datos está por comenzar

    // 3) Leer 40 bits
    for (int i = 0; i < 40; i++) {
        // cada bit comienza con ~50us LOW
        start = esp_timer_get_time();
        while (gpio_get_level(DHT_PIN) == 1) { // si todavía está en HIGH (antes de la bajada), espera
            if ((esp_timer_get_time() - start) > TIMEOUT_PULSE_US) {
                ESP_LOGW(TAG, "Timeout esperando inicio de bit (fallo en baja)");
                return -1;
            }
        }
        // esperar a que suba (inicio del pulso que determina 0/1)
        start = esp_timer_get_time();
        while (gpio_get_level(DHT_PIN) == 0) {
            if ((esp_timer_get_time() - start) > TIMEOUT_PULSE_US) {
                ESP_LOGW(TAG, "Timeout esperando subida de bit");
                return -1;
            }
        }
        // medir duración del pulso HIGH
        int64_t t0 = esp_timer_get_time();
        while (gpio_get_level(DHT_PIN) == 1) {
            if ((esp_timer_get_time() - t0) > 200) { // pulso anormalmente largo
                break;
            }
        }
        int pulse_len = (int)(esp_timer_get_time() - t0); // us

        // bit = 1 si pulso > ~50us (DHT11: ≈70us para 1, ≈26-28us para 0)
        int bit = (pulse_len > 50) ? 1 : 0;
        data[i/8] = (data[i/8] << 1) | bit;
    }

    // 4) checksum
    uint8_t checksum = (data[0] + data[1] + data[2] + data[3]) & 0xFF;
    if (checksum != data[4]) {
        ESP_LOGW(TAG, "Checksum fallo: calc=0x%02X recv=0x%02X", checksum, data[4]);
        return -2;
    }

    // DHT11: humedad entera en data[0], temperatura entera en data[2]
    *humidity = data[0];
    *temperature = data[2];
    return 0;
}

void app_main(void)
{
    int temp=0, hum=0;
    gpio_reset_pin(DHT_PIN);
    gpio_set_pull_mode(DHT_PIN, GPIO_FLOATING);

    while (1) {
        int res = dht_read_data(&temp, &hum);
        if (res == 0) {
            ESP_LOGI(TAG, "Temperatura: %d°C  Humedad: %d%%", temp, hum);
        } else if (res == -1) {
            ESP_LOGW(TAG, "Error lectura: sin respuesta (código -1)");
        } else if (res == -2) {
            ESP_LOGW(TAG, "Error lectura: checksum inválido (código -2)");
        }
        vTaskDelay(pdMS_TO_TICKS(2000)); // DHT11 máximo ~1 lectura/2s
    }
}
