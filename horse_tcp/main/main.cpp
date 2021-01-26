#include "tcp_server.h"
#include "mpu_reader.hpp"
#include "freertos/task.h"
#include "gpio_things.h"

extern "C" void app_main()
{

    config_gpio();
    constexpr int MOSI = 13;
    constexpr int MISO = 12;
    constexpr int SCLK = 14;
    constexpr int CS = 15;

    constexpr uint32_t CLOCK_SPEED = 1000000; // up to 1MHz for all registers

    printf("$ MPU Driver: MPU-SPI\n");
    fflush(stdout);

    spi_device_handle_t mpu_spi_handle; //Handle(identificador) for a device on a SPI bus "spi_master.h"
                                        // Initialize SPI on HSPI host through SPIbus interface:
    hspi.begin(MOSI, MISO, SCLK);
    hspi.addDevice(0, CLOCK_SPEED, CS, &mpu_spi_handle);
    MPU_t MPU;                   // create a default MPU object
    MPU.setBus(hspi);            // set bus port, not really needed here since default is HSPI
    MPU.setAddr(mpu_spi_handle); // set spi_device_handle, always needed!

    mpu_data *global_mpu_data = (mpu_data *)malloc(sizeof(mpu_data));
    start_mpu_data(global_mpu_data);
    tcp_main(global_mpu_data);         //start ble server
    mpu_routine(MPU, global_mpu_data); //start reading sensor routine

    for (;;)
    {

        vTaskDelay(100000000);
    }
}
