#include "MPU.hpp" //include MPU library main file. Declare MPU class.
#include "SPIbus.hpp" //include SPI library. 
#include "mpu/math.hpp"
#include "mpu/types.hpp"
#include "main.h"
void mpu_routine(MPU_t &MPU, mpu_data *global_send_data);

extern "C" struct mpu_data_MPU_t
{
 MPU_t * MPU;
 mpu_data *global_mpu_data;


};
typedef struct mpu_data_MPU_t mpu_data_MPU_t;
