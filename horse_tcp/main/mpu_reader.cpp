#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "esp_err.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/portmacro.h"
#include "freertos/task.h"
#include "sdkconfig.h"
#include "blue_data.h"
#include "mpu_reader.hpp"
static void mpu_reader_task(void *pvParameters);
void debug_vec(int8_t *v, int len){
    for (int i=0;i<len;i++){
        printf ("%hhd, ",v[i]);
    }
    printf("\n");
}
extern "C" {

void start_mpu_data(mpu_data *global_mpu_data){
    global_mpu_data->pos_spi=0;
    global_mpu_data->pos_tcp=0;
    global_mpu_data->overflow=0;
}

void increment_pos_spi(mpu_data *global_mpu_data){
    global_mpu_data->pos_spi = (global_mpu_data->pos_spi+1)%LENBUFFER;
    if (global_mpu_data->pos_spi == global_mpu_data->pos_tcp){
        global_mpu_data->overflow+=1;
    }
}
int increment_pos_tcp(mpu_data *global_mpu_data, char *wr_buffer){
    if (global_mpu_data->pos_tcp==global_mpu_data->pos_spi){
        return 0;
    }
    memcpy(wr_buffer,global_mpu_data->send_data[global_mpu_data->pos_tcp],global_mpu_data->len);
    global_mpu_data->pos_tcp = (global_mpu_data->pos_tcp+1)%LENBUFFER;
    return 1;

}

void reset_overflow (mpu_data *global_mpu_data){
    global_mpu_data->overflow=0;
    global_mpu_data->pos_tcp = (global_mpu_data->pos_spi+2)%LENBUFFER;// garante que pegue os dados mais atrasados
}
}



void mpu_routine(MPU_t &MPU, mpu_data *global_mpu_data) {
    const char* TAG = "SPI"; 
    

    // Great! Let's verify the communication
    // (this also check if the connected MPU supports the implementation of chip selected in the component menu)
    printf("6\n");
    while (esp_err_t err = MPU.testConnection()) {
        ESP_LOGE(TAG, "Failed to connect to the MPU, error=%#X", err);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
    ESP_LOGI(TAG, "MPU connection successful!");

    // Initialize
    ESP_ERROR_CHECK(MPU.initialize());  // initialize the chip and set initial configurations
    //Setup with your configurations
    //ESP_ERROR_CHECK(MPU.setSampleRate(50));  // set sample rate to 50 Hz
    ESP_ERROR_CHECK(MPU.setGyroFullScale(mpud::GYRO_FS_500DPS));
    ESP_ERROR_CHECK(MPU.setAccelFullScale(mpud::ACCEL_FS_2G));
    ESP_ERROR_CHECK(MPU.compassSetSensitivity(mpud::MAG_SENSITIVITY_0_15_uT));

    // Reading sensor data
    printf("Reading sensor data:\n");

    MPU.setSampleRate(1000);
    mpu_data_MPU_t serial_data;
    serial_data.global_mpu_data=global_mpu_data;
    serial_data.MPU=&MPU;
    
    xTaskCreatePinnedToCore(mpu_reader_task, "mpu_reader_task", 4096, (void*)&serial_data, 5, NULL,1);
    vTaskDelay(100000000);
    
}
static void mpu_reader_task(void *pvParameters){
    int8_t send_data[WINDOWDATA];
    mpud::raw_axes_t accelRaw;   // x, y, z axes as int16
    mpud::raw_axes_t gyroRaw;    // x, y, z axes as int16
    mpud::raw_axes_t magRaw;    // x, y, z axes as int16
    mpu_data_MPU_t *serial_data = (mpu_data_MPU_t*)pvParameters;
    mpu_data *global_mpu_data = serial_data->global_mpu_data;
    MPU_t *MPU = serial_data->MPU;
    uint8_t j=0;
    global_mpu_data->len=WINDOWDATA;
    int index;
    while (true) {
        index=0;
        int i;
        for (i=0;i<MAXITERATIONS;i++){
            
            if(j==0){
               
                MPU->motion(&accelRaw,&gyroRaw,&magRaw);         
                set_bytes_mag(&send_data[index], accelRaw.x,accelRaw.y,accelRaw.z,gyroRaw.x,gyroRaw.y,gyroRaw.z,magRaw.x,magRaw.y,magRaw.z);
                index+=STEPMAG;   
            }
            else{
                
                MPU->motion(&accelRaw,&gyroRaw);         
                set_bytes(&send_data[index], accelRaw.x,accelRaw.y,accelRaw.z,gyroRaw.x,gyroRaw.y,gyroRaw.z);
                
                index+=STEP;
            }
            j=(j+1)%10;
            vTaskDelay(1/portTICK_PERIOD_MS);
            
        }
        
        memcpy(global_mpu_data->send_data[global_mpu_data->pos_spi],send_data,WINDOWDATA);//TODO tornar thread safe
        increment_pos_spi(global_mpu_data);
    }

}
