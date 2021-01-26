#define ESP_INTR_FLAG_DEFAULT 0
#define BUTTON_1 (gpio_num_t)4
#define GPIO_INPUT_PIN_SEL (1ULL << BUTTON_1)

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "driver/gpio.h"
#include "driver/rtc_io.h"
#include "esp_sleep.h"
#include "gpio_things.h"
#define LED_1 (gpio_num_t)16 //ou GPIO_NUM_16
#define LED_2 (gpio_num_t)17 //ou GPIO_NUM_17
#define GPIO_OUTPUT_PIN_SEL ((1ULL << LED_1) | (1ULL << LED_2))

RTC_DATA_ATTR bool is_wakeup = false;

void wifi_led_on()
{
    gpio_set_level(LED_1, 1);
}

void wifi_led_off()
{

    gpio_set_level(LED_1, 0);
}

void main_led_on()
{
    gpio_set_level(LED_2, 1);
}

void main_led_off()
{
    gpio_set_level(LED_2, 0);
}

static int is_sleeping = 0;
void IRAM_ATTR gpio_isr_handler(void *arg)
{

    gpio_uninstall_isr_service();
    is_sleeping = 1;
}
void loop_gpio(void *args)
{

    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    gpio_isr_handler_add(BUTTON_1, gpio_isr_handler, (void *)BUTTON_1);

    for (;;)
    {
        vTaskDelay(100 / portTICK_PERIOD_MS);
        if (is_sleeping)
        {
            vTaskDelay(1000 / portTICK_PERIOD_MS);
            esp_sleep_enable_ext1_wakeup(GPIO_INPUT_PIN_SEL, ESP_EXT1_WAKEUP_ANY_HIGH);
            esp_deep_sleep_start();
        }
    }
}

void config_gpio()
{

    if (!is_wakeup)
    {
        is_wakeup = true;
        esp_sleep_enable_ext1_wakeup(GPIO_INPUT_PIN_SEL, ESP_EXT1_WAKEUP_ANY_HIGH);
        esp_deep_sleep_start();
    }

    //Configura o descritor das Inputs (botões)
    gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_NEGEDGE,
        .mode = GPIO_MODE_INPUT,
        .pin_bit_mask = GPIO_INPUT_PIN_SEL,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE};

    gpio_config_t led_conf = {
        .intr_type = GPIO_PIN_INTR_DISABLE,
        .mode = GPIO_MODE_OUTPUT,
        .pin_bit_mask = GPIO_OUTPUT_PIN_SEL};
    gpio_config(&io_conf);
    gpio_config(&led_conf);

    main_led_on();
    xTaskCreate(loop_gpio, "loop_gpio", 2048, NULL, 2, NULL);
}